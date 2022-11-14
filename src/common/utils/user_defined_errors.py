class UserErrors(Exception):
    def _init_(self, message=None, response_code=None):
        self.message = message if message else "Internal Server Error"
        self.response_code = response_code if response_code else 500
        self.type = "UserErrors"


class PermissionDeniedError(UserErrors):
    def _init_(self, message=None, response_code=None):
        self.message = message if message else "Could not validate credentials"
        self.response_code = response_code if response_code else 401
        self.type = "PermissionDeniedError"


class PayloadLargeError(UserErrors):
    def _init_(self, message=None, response_code=None):
        self.message = message if message else " Payload is too large to Process"
        self.response_code = response_code if response_code else 413
        self.type = "PayloadLargeError"