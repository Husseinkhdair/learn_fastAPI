class AuthException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message

    def __eq__(self, other):
        if isinstance(other, str):
            return self.message == other
        if isinstance(other, AuthException):
            return type(self) is type(other) and self.message == other.message
        return False

class InvalidCredentialsException(AuthException):
    def __init__(self, message: str = "Invalid email or password."):
        super().__init__(message)

class UserAlreadyExistsException(AuthException):
    def __init__(self, message: str = "User already exists"):
        super().__init__(message)
        