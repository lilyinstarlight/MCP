class NoServerError(Exception):
	pass

class InvalidServerError(Exception):
	pass

class ServerExistsError(Exception):
	pass

class ServerRunningError(Exception):
	pass

class ServerStoppedError(Exception):
	pass

class NoServerCreationError(Exception):
	pass

class NoSourceError(Exception):
	pass

class InvalidSourceError(Exception):
	pass

class SourceExistsError(Exception):
	pass

class BuildError(Exception):
	pass

class ConfigError(Exception):
	pass

class BzrError(Exception):
	pass

class NoUserError(Exception):
	pass

class InvalidUserError(Exception):
	pass

class UserExistsError(Exception):
	pass
