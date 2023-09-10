from fastapi import HTTPException, status

class UserNotFoundException(HTTPException):
    def __init__(self, email: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = f"User {email} has not been found."
        
        
class WrongPasswordException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "Wrong password!"
        
class SameOldAndNewPassword(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "Please provide a new password!"