class AuthException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class InvalidCredentialsException(AuthException):
    def __init__(self):
        super().__init__("Invalid email or password.")

class UserAlreadyExistsException(AuthException):
    def __init__(self):
        super().__init__("User with this email already exists.")
        