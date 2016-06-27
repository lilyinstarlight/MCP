class Error(Exception):
    def __init__(self, msg=None):
        self.msg = msg

class NoServerError(Error):
    pass

class InvalidServerError(Error):
    pass

class ServerRunningError(Error):
    pass

class ServerStoppedError(Error):
    pass

class ServerExistsError(Error):
    pass

class ServerNonexistentError(Error):
    pass

class ScriptNonexistentError(Error):
    pass

class NoServerCreationError(Error):
    pass

class BuildError(Error):
    pass

class ConfigError(Error):
    pass

class MergeError(Error):
    pass

class NoSourceError(Error):
    pass

class InvalidSourceError(Error):
    pass

class SourceExistsError(Error):
    pass

class BzrError(Error):
    pass

class NoPortError(Error):
    pass

class InvalidPortError(Error):
    pass

class PortExistsError(Error):
    pass

class NoUserError(Error):
    pass

class InvalidUserError(Error):
    pass

class UserExistsError(Error):
    pass
