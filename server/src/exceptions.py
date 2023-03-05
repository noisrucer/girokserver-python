from fastapi import HTTPException, status


class EmailNotExistException(HTTPException):
    def __init__(self, email: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = f"Email: {email} does not exist."
        