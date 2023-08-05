class ConfigError(ValueError):
    def __init__(self, exception):
        self.exception = exception
        super(ConfigError, self).__init__(exception)


class BackendError(ValueError):
    def __init__(self, exception):
        self.exception = exception
        super(BackendError, self).__init__(exception)
