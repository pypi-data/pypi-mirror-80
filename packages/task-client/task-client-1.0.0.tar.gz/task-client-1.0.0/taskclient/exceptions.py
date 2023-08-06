class TaskManagerError(Exception):
    pass


class TaskManagerValueError(TaskManagerError):
    pass


class TaskManagerResponseError(TaskManagerError):
    def __init__(self, uri, status_code, acceptable_status_codes):
        self.uri = uri
        self.status_code = status_code
        self.acceptable_status_codes = acceptable_status_codes

    def __str__(self):
        return 'Invalid response from TaskClient for url {}, got status {}, expected status {}'.format(
            self.uri,
            self.status_code,
            self.acceptable_status_codes,
        )


class TaskManagerConnectionError(TaskManagerError):
    pass


class TaskManagerNoAuthError(TaskManagerConnectionError):
    def __init__(self, payload, message):
        super(TaskManagerNoAuthError, self).__init__(message)
        self.payload = payload


class TaskManagerSSLError(TaskManagerConnectionError):
    pass


