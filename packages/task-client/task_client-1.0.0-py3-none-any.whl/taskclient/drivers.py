import weakref
from .exceptions import TaskManagerError

from .core import Task

__all__ = ['DRIVERS']


class BaseDriver(object):
    def __init__(self, parent):
        self.parent = weakref.ref(parent)

    @property
    def session(self):
        return self.parent()

    @property
    def logger(self):
        return self.parent().logger


class DriverV0(BaseDriver):
    def get_tasks(self,
                  project=None,
                  template=None,
                  user=None,
                  status=None,
                  tag=None,
                  application_name=None,
                  offset=None,
                  limit=None):

        query = {}

        if user is not None:
            query['user'] = user

        if status is not None:
            query['status'] = status

        response = self.session.get('/tasks', query=query)

        data = response.json()

        # Create tasks objects
        data = [self.session.create_object(Task, x) for x in data]

        # Do client side filtering for non-supported fields
        if project is not None:
            data = [x for x in data if x.project == project]

        if template is not None:
            raise NotImplementedError('Template filtering is not implemented for v0 task-managers')

        if tag is not None:
            data = [x for x in data if tag in [t.name for t in x.tags]]

        if application_name is not None:
            raise NotImplementedError('Application name filtering is not implemented for v0 task-managers')

        # Apply offset and limit
        if offset is not None:
            data = data[offset:]

        if limit is not None:
            data = data[:limit]

        return data

    def change_lock(self, lock_uri, value):
        try:
            response = self.session.put(lock_uri,
                                        json={"lock": value},
                                        accepted_status=[200, 403, 404, 409])
        except TaskManagerError as exception:
            self.logger.warning('Encounted error during lock change: {}'.format(exception))
            return False

        if response.status_code != 200:
            self.logger.warning('Lock response: [{}] {}'.format(response.status_code, response.text))
            return False
        else:
            return True


class DriverV1(BaseDriver):
    def get_tasks(self,
                  project=None,
                  template=None,
                  user=None,
                  status=None,
                  tag=None,
                  application_name=None,
                  offset=None,
                  limit=None):

        # Build filtering query string
        query = {}

        if project is not None:
            query['project'] = project

        if template is not None:
            query['template'] = template

        if user is not None:
            query['user'] = user

        if status is not None:
            query['status'] = status

        if tag is not None:
            query['tag'] = tag

        if application_name is not None:
            query['application_name'] = application_name

        if offset is not None:
            query['offset'] = offset

        if limit is not None:
            query['limit'] = limit

        # Get data
        response = self.session.get('/tasks', query=query)

        # Return result as Task objects
        data = response.json()
        return [self.session.create_object(Task, x) for x in data['tasks']]

    def change_lock(self, lock_uri, value):
        self.logger.info('Change task lock {} to {}'.format(lock_uri, value))
        try:
            if value is None:
                response = self.session.delete(lock_uri,
                                               accepted_status=[200, 403, 404, 409])
            else:
                response = self.session.put(lock_uri,
                                            json={"lock": value},
                                            accepted_status=[200, 403, 404, 409])
        except TaskManagerError as exception:
            self.logger.warning('Encountered error during lock change: {}'.format(exception))
            return False

        if response.status_code != 200:
            self.logger.warning('Lock response: [{}] {}'.format(response.status_code, response.text))
            return False
        else:
            return True


DRIVERS = {
    0: DriverV0,
    0.5: DriverV1,
    1: DriverV1
}
