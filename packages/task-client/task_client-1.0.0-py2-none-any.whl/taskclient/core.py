class TaskClientBaseObject(object):
    def __init__(self, uri, session, data):
        self.uri = uri
        self.session = session
        self._data = dict(**data)  # Copy initial data in cache to avoid fetching when only summary is required
        self.caching = True

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '<{} {}>'.format(type(self).__name__, self.uri)

    @property
    def logger(self):
        return self.session.logger

    # Function for getting data in a lazy/cached way when possible
    def _update_data(self):
        object_data = self.session.get_json(self.uri)
        self._data = object_data

    def _put_vars(self, **kwargs):
        self.session.put(
            self.uri,
            json=kwargs,
        )

    def _get_data_field(self, name):
        if not self.caching or name not in self._data:
            self._update_data()

        return self._data[name]

    # Some cache management methods
    def clearcache(self):
        self._data.clear()

    @property
    def caching(self):
        if self._caching is not None:
            return self._caching
        else:
            return self.session.caching

    @caching.setter
    def caching(self, value):
        self._caching = value

    @caching.deleter
    def caching(self):
        self._caching = None


class Task(TaskClientBaseObject):
    @property
    def id(self):
        return int(self.uri.rsplit('/', 1)[1])

    @property
    def status(self):
        return self._get_data_field('status')

    @status.setter
    def status(self, value):
        self._put_vars(status=value)

    @property
    def project(self):
        return self._get_data_field('project')

    @property
    def template(self):
        return self.session.create_object(Template, self._get_data_field('template'))

    @property
    def lock(self):
        data = self.session.get_json(self._get_data_field('lock'))
        return data

    def change_lock(self, value):
        return self.session.change_lock(self._get_data_field('lock'), value)

    @property
    def tags(self):
        return [self.session.create_object(Tag, x) for x in self._get_data_field('tags')]

    @property
    def content(self):
        return self._get_data_field('content')

    @property
    def callback_url(self):
        return self._get_data_field('callback_url')

    @property
    def callback_content(self):
        return self._get_data_field('callback_content')

    @property
    def generator_url(self):
        return self._get_data_field('generator_url')

    @property
    def application_name(self):
        return self._get_data_field('application_name')

    @property
    def application_version(self):
        return self._get_data_field('application_version')

    @property
    def create_time(self):
        return self._get_data_field('create_time')

    @property
    def update_time(self):
        return self._get_data_field('update_time')

    @property
    def users(self):
        data = self._get_data_field('users')
        return [self.session.create_object(User, x) for x in data]

    @property
    def groups(self):
        data = self._get_data_field('groups')
        return [self.session.create_object(Group, x) for x in data]

    @property
    def users_via_group(self):
        data = self._get_data_field('users_via_group')
        return [self.session.create_object(User, x) for x in data]


class Template(TaskClientBaseObject):
    def __str__(self):
        return '<Template {}>'.format(self.label)

    @property
    def label(self):
        return self._get_data_field('label')

    @property
    def content(self):
        return self._get_data_field('content')


class User(TaskClientBaseObject):
    def __str__(self):
        return '<User {}>'.format(self.username)

    @property
    def username(self):
        return self._get_data_field('username')

    @property
    def name(self):
        return self._get_data_field('name')

    @property
    def active(self):
        return self._get_data_field('active')

    @property
    def email(self):
        return self._get_data_field('active')

    @property
    def create_time(self):
        return self._get_data_field('create_time')

    @property
    def assignment_weight(self):
        return self._get_data_field('assignment_weight')

    @property
    def tasks(self):
        data = self.session.get_json(self._get_data_field('tasks'))
        return [self.session.create_object(Task, x) for x in data['tasks']]

    @property
    def groups(self):
        data = self.session.get_json(self._get_data_field('groups'))
        return [self.session.create_object(Group, x) for x in data['groups']]


class Group(TaskClientBaseObject):
    def __str__(self):
        return '<Group {}>'.format(self.groupname)

    @property
    def groupname(self):
        return self._get_data_field('groupname')

    @property
    def name(self):
        return self._get_data_field('name')

    @property
    def create_time(self):
        return self._get_data_field('create_time')

    @property
    def tasks(self):
        raise NotImplementedError('This feature is not implemented server side!')

    @property
    def users(self):
        data = self.session.get_json(self._get_data_field('users'))
        return [self.session.create_object(User, x) for x in data['users']]


class Tag(TaskClientBaseObject):
    def __str__(self):
        return '<Tag {}>'.format(self.name)

    @property
    def name(self):
        return self._get_data_field('name')

    @property
    def tasks(self):
        data = self.session.get_json(self._get_data_field('tasks'))
        return [self.session.create_object(Task, x) for x in data['tasks']]
