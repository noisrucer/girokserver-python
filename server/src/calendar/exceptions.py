from fastapi import HTTPException, status


class CategoryAlreadyExistsException(HTTPException):
    def __init__(self, sup, sub):
        self.status_code = status.HTTP_400_BAD_REQUEST
        if sup == "":
            self.detail = f"There already exists a category named '{sub}'."
        else:
            self.detail = f"'{sup}' already has a subcategory named '{sub}'"
        

class CategoryNotExistException(HTTPException):
    def __init__(self, name):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = f"Category '{name}' does not exist."
        
        
class SubcategoryNotExistException(HTTPException):
    def __init__(self, sup, sub):
        self.status_code = status.HTTP_400_BAD_REQUEST
        if sup == "":
            self.detail = f"There is no category named {sub}."
        else:
            self.detail = f"'{sup}' does not have a subcategory named '{sub}'"