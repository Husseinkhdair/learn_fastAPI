class AuthException(Exception):
    def __init__(self,message:str):
        self.message = message
        super().__init__(self.message)

class InvalidCredentialsException(AuthException):
    def __init__(self,message:str = "Invalid email or password."):
        super().__init__(message)

class UserAlreadyExistsException(AuthException):
    def __init__(self,message:str = "User already exists"):
        super().__init__(message)

