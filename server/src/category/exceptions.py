from fastapi import HTTPException, status
import server.src.category.constants as category_constants


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
            

class CannotMoveRootDirectoryException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "Cannot move the root directory!"
        
        
class CannotMoveToSameLocation(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "[Warning] Circular reference prohibited."
        
        
class CategoryColorException(HTTPException):
    def __init__(self, cat_path, color, parent_cat_path, parent_color):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = f"You have given {color} color for {cat_path}. However, {parent_cat_path} already has a color {parent_color}"
        
class CategoryColorNotExistException(HTTPException):
    def __init__(self, color):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = f"'{color}' is not a valid color. Please choose from {category_constants.CATEGORY_COLORS}."