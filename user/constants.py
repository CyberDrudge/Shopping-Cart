READ_METHODS = ["GET"]
WRITE_METHODS = ['POST', 'PUT', 'DELETE']

MOBILE_CODE_VALID_FOR_MINS = 5
MOBILE_VERIFICATION_CODE_LENGTH = 6


class UserStatusChoices:
	INACTIVE = "inactive"
	NEW = "new"
	RETURNING = "returning"
	BLACKLISTED = "blacklisted"


class UserIntentChoices:
	LOGIN = "login"
	REGISTER = "register"
