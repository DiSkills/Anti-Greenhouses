class VerificationExists(Exception):
    pass


class UserWithEmailExists(Exception):
    pass


class UserWithUsernameExists(Exception):
    pass


class VerificationNotFound(Exception):
    pass


class BadVerificationUUID(Exception):
    pass


class InvalidUsernameOrPassword(Exception):
    pass
