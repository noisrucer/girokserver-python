from fastapi import HTTPException, status

class InvalidPriorityWindowException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "Minimum priority must be less than or equal to maximum priority."
        
    
class InvalidDateWindowException(HTTPException):
    def __init__(self, start, end):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = f"Start date {start} must be before or equal to end date {end}."
        
        
class InvalidPriorityPairException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = f"Min and max priority must be both present or all None."
        
class TaskNotFoundException(HTTPException):
    def __init__(self, task_id):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = f"Task id {task_id} is not found."

