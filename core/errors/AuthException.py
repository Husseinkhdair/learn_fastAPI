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

class InvalidTokenException(AuthException):
    def __init__(self,message:str ="Invalid Token"):
        super().__init__(message)

class AccessTokenCreationFailedException(AuthException):
    def __init__(self, message: str = "Failed to create access token"):
        super().__init__(message)

class RefreshTokenCreationFailedException(AuthException):
    def __init__(self, message: str = "Failed to create refresh token"):
        super().__init__(message)

class PasswordHashingFailedException(AuthException):
    def __init__(self, message: str = "Failed to hash user password"):
        super().__init__(message)

class PasswordVerificationFailedException(AuthException):
    def __init__(self, message: str = "Failed to verify user password"):
        super().__init__(message)
        
class ErrorDataBaseException(AuthException):
        def __init__(self, message: str = "Error In DataBase"):
            super().__init__(message)

class ErrorServerException(Exception):
    def __init__(self,message:str = "Error In Server"):
        self.message = message
        super().__init(message)