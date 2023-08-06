from __future__ import absolute_import
from __future__ import unicode_literals

import os
import netrc
import platform
import requests

import six
from six.moves.urllib import parse

from .core import Task, Template, Tag, User, Group
from .drivers import DRIVERS
from .exceptions import TaskManagerValueError
from .exceptions import TaskManagerNoAuthError
from .exceptions import TaskManagerResponseError
from .exceptions import TaskManagerSSLError
from .exceptions import TaskManagerConnectionError


class TaskClient(object):
    CACHE_NAMES = {
        Task: '__tasks__',
        Template: '__templates__',
        Tag: '__tags__',
        User: '__users__',
        Group: '__groups__',
    }

    def __init__(self, server, user=None, password=None, session=None, logger=None,
                 user_agent=None, user_agent_prefix=None, debug=False, application_name=None):
        self._server = parse.urlparse(server)
        self.original_uri = server.rstrip()
        self._url_prefix = self.original_uri
        self._version_prefix = None
        self.application_name = application_name

        # Pre-set some variables
        self.api_version = None
        self.driver = None

        # Caching settings
        self._cache = {}
        self.clearcache()
        self.caching = True

        self.logger = logger

        # Requests session
        if session:
            self.interface = session
        else:
            self.interface = requests.Session()

        if user_agent is None:
            user_agent = "({platform}/{release}; python/{python}; requests/{requests})".format(
                platform=platform.system(),
                release=platform.release(),
                python=platform.python_version(),
                requests=requests.__version__
            )

            # Add user agent prefix if needed
            if user_agent_prefix:
                user_agent = "{user_agent_prefix} {user_agent}".format(
                    user_agent_prefix=user_agent_prefix,
                    user_agent=user_agent
                )

        # Set user agent and accept content type headers
        self.interface.headers.update({
            'User-Agent': user_agent,
            'Accept': 'application/json'
        })

        # Get auth
        if user is None and password is None:
            netrc_file = '~/_netrc' if os.name == 'nt' else '~/.netrc'
            netrc_file = os.path.abspath(os.path.expanduser(netrc_file))
            self.logger.info('Retrieving login info for {}'.format(self._server.netloc))
            try:
                user, _, password = netrc.netrc(netrc_file).authenticators(self._server.netloc)
            except IOError:
                self.logger.info('Could not load the netrc file ({}), it does not exist!'.format(netrc_file))
            except TypeError:
                self.logger.info('Could not retrieve login info for "{}" from the .netrc file!'.format(server))

        self.interface.auth = (user, password)

        # Set some connection properties
        self.debug = debug
        self.request_timeout = 20  # 10 seconds default
        self.accepted_status_get = [200]
        self.accepted_status_post = [200, 201]
        self.accepted_status_put = [200, 201]
        self.accepted_status_delete = [200]
        self.skip_response_check = False

        # Detect API version and load appropriate driver
        self.detect_api_version()

        try:
            response = self.get('/tags', accepted_status=[200, 401, 404], timeout=2)
        except Exception as exception:
            self.logger.error('Error in test tags request {}: {}'.format(self.original_uri, exception))
            raise

        self.logger.info('Response code on test tags request: {}'.format(response.status_code))
        if response.status_code == 401:
            payload = response.headers['www-authenticate'].split("=")[1].strip("\"")
            raise TaskManagerNoAuthError(payload, 'Could not authenticate for {}'.format(self.original_uri))

    def __del__(self):
        self.disconnect()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def disconnect(self):
        """
        Placeholder in case we ever need cleanup later
        """
        pass

    def detect_api_version(self):
        # Detect API version
        try:
            response = self.get('/-/versions', accepted_status=[200, 401, 404], timeout=2)
        except Exception as exception:
            message = 'Cannot create connection to {}'.format(self.original_uri)
            if self.debug:
                message = '{}: {}'.format(message, exception)
            self.logger.error(message)
            raise TaskManagerConnectionError(message)

        self.logger.info('Response code on initial try: {}'.format(response.status_code))
        if response.status_code == 401:
            payload = response.headers['www-authenticate'].split("=")[1].strip("\"")
            raise TaskManagerNoAuthError(payload, 'Could not authenticate for {}'.format(self.original_uri))

        if response.status_code == 200:
            versions = response.json().get('api_versions')
            if not versions:
                raise TaskManagerValueError('Could not get version from /-/versions endpoint data, found {}'.format(
                    response.json())
                )

            api_version = max(float(x) for x in versions)
            version_uri = versions[str(api_version)]
            server_uri = response.url[:-11]
        else:
            response = self.get('/data')
            self.logger.info('Response code on secondary try: {}'.format(response.status_code))
            server_data = response.json()
            api_version = server_data.get('api_version', 0)
            if api_version == 2:
                api_version = 0.5
            version_uri = '/data'
            server_uri = response.url[:-5]

        self._url_prefix = server_uri

        if self._url_prefix != self.original_uri:
            self.logger.warning('Detected a redirect from {0} to {1}, using {1} from now on'.format(
                self.original_uri, self._url_prefix
            ))

        self.logger.info('Found TaskManager server with API version {} at {}{}'.format(
            api_version,
            self._url_prefix.rstrip('/'),
            version_uri
        ))

        # Change server uri to be inside the server path
        self._server = parse.urlparse(self._url_prefix.rstrip('/') + version_uri)
        self._version_prefix = version_uri
        self.api_version = api_version

        # Select API Driver
        self.driver = DRIVERS[self.api_version](self)

    def _format_uri(self, path, query=None):
        if path[0] != '/':

            if self._url_prefix is not None and path.startswith(self._url_prefix):
                path = path[len(self._url_prefix):]  # Strip original uri

            if self.original_uri is not None and path.startswith(self.original_uri):
                path = path[len(self.original_uri):]  # Strip original uri

            if path[0] != '/':
                raise TaskManagerValueError('The requested URI path should start with a /, found {}'.format(path))

        if self._version_prefix is not None and path.startswith(self._version_prefix):
            path = path[len(self._version_prefix.rstrip('/')):]  # Strip version prefix

        if query is None:
            query = {}

        # Sanitize unicode in query
        query = {k: v.encode('utf-8', 'xmlcharrefreplace') if isinstance(v, six.text_type) else v for k, v in query.items()}

        # Create the query string
        if len(query) > 0:
            query_string = parse.urlencode(query, doseq=True)
        else:
            query_string = ''

        data = (self._server.scheme,
                self._server.netloc,
                self._server.path.rstrip('/') + path,
                '',
                query_string,
                '')

        return parse.urlunparse(data)

    def _check_response(self, response, accepted_status=None, uri=None):

        if self.debug:
            self.logger.debug('Received response with status code: {}'.format(response.status_code))

        if not self.skip_response_check:
            if accepted_status is None:
                accepted_status = [200, 201, 202, 203, 204, 205, 206]  # All successful responses of HTTP

            if response.status_code not in accepted_status:
                raise TaskManagerResponseError(uri, response.status_code, accepted_status)

    def get(self, path, query=None, accepted_status=None, timeout=None, headers=None):
        """
        Retrieve the content of a given REST directory.

        :param str path: the path of the uri to retrieve (e.g. "/data/archive/projects")
                         the remained for the uri is constructed automatically
        :param dict query: the values to be added to the query string in the uri
        :param list accepted_status: a list of the valid values for the return code, default [200]
        :param timeout: timeout in seconds, float or (connection timeout, read timeout)
        :type timeout: float or tuple
        :param dict headers: the HTTP headers to include
        :returns: the requests response
        :rtype: requests.Response
        """
        accepted_status = accepted_status or self.accepted_status_get
        uri = self._format_uri(path, query=query)
        timeout = timeout or self.request_timeout

        self.logger.debug('GET URI {}'.format(uri))

        try:
            response = self.interface.get(uri, timeout=timeout, headers=headers)
        except requests.exceptions.SSLError:
            raise TaskManagerSSLError('Encountered a problem with the SSL connection, are you sure the server is offering https?')
        except requests.ConnectionError:
            raise TaskManagerConnectionError('Could not connect to server for {}'.format(uri))
        self._check_response(response, accepted_status=accepted_status, uri=uri)  # Allow OK, as we want to get data
        return response

    def get_json(self, uri, query=None, accepted_status=None):
        """
        Helper function that perform a GET, but sets the format to JSON and
        parses the result as JSON

        :param str uri: the path of the uri to retrieve (e.g. "/data/archive/projects")
                         the remained for the uri is constructed automatically
        :param dict query: the values to be added to the query string in the uri
        """
        response = self.get(uri, query=query, accepted_status=accepted_status)
        return response.json()

    def change_lock(self, lock_uri, value):
        return self.driver.change_lock(lock_uri, value)

    def head(self, path, accepted_status=None, allow_redirects=False, timeout=None, headers=None):
        """
        Retrieve the header for a http request of a given REST directory.

        :param str path: the path of the uri to retrieve (e.g. "/data/archive/projects")
                         the remained for the uri is constructed automatically
        :param list accepted_status: a list of the valid values for the return code, default [200]
        :param bool allow_redirects: allow you request to be redirected
        :param timeout: timeout in seconds, float or (connection timeout, read timeout)
        :type timeout: float or tuple
        :param dict headers: the HTTP headers to include
        :returns: the requests reponse
        :rtype: requests.Response
        """
        accepted_status = accepted_status or self.accepted_status_get
        uri = self._format_uri(path)
        timeout = timeout or self.request_timeout

        self.logger.debug('GET URI {}'.format(uri))

        try:
            response = self.interface.head(uri, allow_redirects=allow_redirects, timeout=timeout, headers=headers)
        except requests.exceptions.SSLError:
            raise TaskManagerSSLError('Encountered a problem with the SSL connection, are you sure the server is offering https?')
        except requests.ConnectionError:
            raise TaskManagerConnectionError('Could not connect to server for {}'.format(uri))
        self._check_response(response, accepted_status=accepted_status, uri=uri)  # Allow OK, as we want to get data
        return response

    def post(self, path, data=None, json=None, query=None, accepted_status=None, timeout=None, headers=None):
        """
        Post data to a given REST directory.

        :param str path: the path of the uri to retrieve (e.g. "/data/archive/projects")
                         the remained for the uri is constructed automatically
        :param data: Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
        :param json: json data to send in the body of the :class:`Request`.
        :param dict query: the values to be added to the query string in the uri
        :param list accepted_status: a list of the valid values for the return code, default [200, 201]
        :param timeout: timeout in seconds, float or (connection timeout, read timeout)
        :type timeout: float or tuple
        :param dict headers: the HTTP headers to include
        :returns: the requests response
        :rtype: requests.Response
        """
        accepted_status = accepted_status or self.accepted_status_post
        uri = self._format_uri(path, query=query)
        timeout = timeout or self.request_timeout

        self.logger.debug('POST URI {}'.format(uri))
        if self.debug:
            self.logger.debug('POST DATA {}'.format(data))

        try:
            response = self.interface.post(uri, data=data, json=json, timeout=timeout, headers=headers)
        except requests.exceptions.SSLError:
            raise TaskManagerSSLError('Encountered a problem with the SSL connection, are you sure the server is offering https?')
        except requests.ConnectionError:
            raise TaskManagerConnectionError('Could not connect to server for {}'.format(uri))
        self._check_response(response, accepted_status=accepted_status, uri=uri)
        return response

    def put(self, path, data=None, files=None, json=None, query=None, accepted_status=None, timeout=None, headers=None):
        """
        Put the content of a given REST directory.

        :param str path: the path of the uri to retrieve (e.g. "/data/archive/projects")
                         the remained for the uri is constructed automatically
        :param data: Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
        :param json: json data to send in the body of the :class:`Request`.
        :param files: Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``) for multipart encoding upload.
                      ``file-tuple`` can be a 2-tuple ``('filename', fileobj)``, 3-tuple ``('filename', fileobj, 'content_type')``
                      or a 4-tuple ``('filename', fileobj, 'content_type', custom_headers)``, where ``'content-type'`` is a string
                      defining the content type of the given file and ``custom_headers`` a dict-like object containing additional headers
                      to add for the file.
        :param dict query: the values to be added to the query string in the uri
        :param list accepted_status: a list of the valid values for the return code, default [200, 201]
        :param timeout: timeout in seconds, float or (connection timeout, read timeout)
        :type timeout: float or tuple
        :param dict headers: the HTTP headers to include
        :returns: the requests response
        :rtype: requests.Response
        """
        self.logger.info('PUT {} WITH JSON: {}'.format(path, json))
        accepted_status = accepted_status or self.accepted_status_put
        uri = self._format_uri(path, query=query)
        timeout = timeout or self.request_timeout

        self.logger.debug('PUT URI {}'.format(uri))
        if self.debug:
            self.logger.debug('PUT DATA {}'.format(data))
            self.logger.debug('PUT FILES {}'.format(data))

        try:
            self.logger.info('CALL REQUESTS.PUT {} WITH DATA: {}  JSON: {}'.format(uri, data, json))
            response = self.interface.put(uri, data=data, files=files, json=json, timeout=timeout, headers=headers)
        except requests.exceptions.SSLError:
            raise TaskManagerSSLError('Encountered a problem with the SSL connection, are you sure the server is offering https?')
        except requests.ConnectionError:
            raise TaskManagerConnectionError('Could not connect to server for {}'.format(uri))
        self._check_response(response, accepted_status=accepted_status, uri=uri)  # Allow created OK or Create status (OK if already exists)
        return response

    def delete(self, path, headers=None, accepted_status=None, query=None, timeout=None):
        """
        Delete the content of a given REST directory.

        :param str path: the path of the uri to retrieve (e.g. "/data/archive/projects")
                         the remained for the uri is constructed automatically
        :param dict headers: the HTTP headers to include
        :param dict query: the values to be added to the query string in the uri
        :param list accepted_status: a list of the valid values for the return code, default [200]
        :param timeout: timeout in seconds, float or (connection timeout, read timeout)
        :type timeout: float or tuple
        :returns: the requests response
        :rtype: requests.Response
        """
        accepted_status = accepted_status or self.accepted_status_delete
        uri = self._format_uri(path, query=query)
        timeout = timeout or self.request_timeout

        self.logger.debug('DELETE URI {}'.format(uri))
        if self.debug:
            self.logger.debug('DELETE HEADERS {}'.format(headers))

        try:
            response = self.interface.delete(uri, headers=headers, timeout=timeout)
        except requests.exceptions.SSLError:
            raise TaskManagerSSLError('Encountered a problem with the SSL connection, are you sure the server is offering https?')
        except requests.ConnectionError:
            raise TaskManagerConnectionError('Could not connect to server for {}'.format(uri))
        self._check_response(response, accepted_status=accepted_status, uri=uri)
        return response

    def clearcache(self):
        """
        Clear the cache of the listings in the Session object
        """
        self._cache.clear()
        self._cache = {x: {} for x in self.CACHE_NAMES.values()}

    def create_object(self, type, data):
        if isinstance(data, six.text_type):
            uri = data
            data = {}
        else:
            # TODO: hack due to inconsistency in task-manager, needs to be fixed
            if 'uri' not in data and 'url' in data:
                data['uri'] = data.pop('url')

            uri = data['uri']

        type_name = self.CACHE_NAMES[type]

        try:
            return self._cache[type_name][uri]
        except KeyError:
            task = type(uri, self, data)
            self._cache[type_name][uri] = task
            return task

    def get_tasks(self,
                  project=None,
                  template=None,
                  user=None,
                  status=None,
                  tag=None,
                  application_name=None,
                  offset=None,
                  limit=None):

        # Use global application_name if set
        if not application_name:
            application_name = self.application_name

        # Make sure objects are replaced by the identifying properties
        if isinstance(user, User):
            user = user.username

        if isinstance(template, Template):
            template = template.label

        if isinstance(tag, Tag):
            tag = tag.name

        data = self.driver.get_tasks(
            project=project,
            template=template,
            user=user,
            status=status,
            tag=tag,
            application_name=application_name,
            offset=offset,
            limit=limit,
        )

        return data

    def get_tags(self):
        tags = self.get('/tags').json()['tags']
        return [self.create_object(Tag, x) for x in tags]

    def get_template(self, name):
        return self.create_object(Template, '/task_templates/{}'.format(name))
