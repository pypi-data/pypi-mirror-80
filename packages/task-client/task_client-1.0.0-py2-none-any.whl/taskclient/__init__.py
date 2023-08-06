import hashlib
import logging
import time
from .connection import TaskClient

__version__ = '1.0.0'


def connect(uri, user=None, password=None, logger=None, loglevel=None, debug=False, user_agent_prefix=None):
    # Generate a hash for the connection
    hasher = hashlib.md5()
    hasher.update(uri.encode('utf-8'))
    hasher.update(str(time.time()).encode('utf-8'))
    connection_id = hasher.hexdigest()

    # Setup the logger for this connection
    if logger is None:
        logger = logging.getLogger('task-client-{}'.format(connection_id))
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)

        # create formatter
        if debug:
            formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(module)s:%(lineno)d >> %(message)s')
        else:
            formatter = logging.Formatter('[%(levelname)s] %(message)s')
        handler.setFormatter(formatter)

        if loglevel is not None:
            logger.setLevel(loglevel)
        elif debug:
            logger.setLevel('DEBUG')
        else:
            logger.setLevel('WARNING')

    client = TaskClient(uri, user=user, password=password, logger=logger,
                        user_agent_prefix=user_agent_prefix, debug=debug)
    return client
