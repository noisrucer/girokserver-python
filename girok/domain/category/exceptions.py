from fastapi import status

from girok.core.exceptions.base import BaseCustomException


class CategoryEmptyPathError(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Category Empty Path Error: Category path cannot be empty."

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail)


class CategoryNotFoundError(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, super_category_path: str, category_name: str):
        super().__init__(
            status_code=self.status_code,
            detail=f"Category Not Found: '{super_category_path}' does not have a sub-category named '{category_name}'",  # noqa: E501
        )


class CategoryAlreadyExistsError(BaseCustomException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, super_category_path: str, category_name: str):
        super().__init__(
            status_code=self.status_code,
            detail=f"Category Already Exists: '{super_category_path}' already has a sub-category named '{category_name}'",  # noqa: E501
        )


# class CategoryEmptyPathError(BaseCustomException):
#     def __init__(self, detail: str | None = None):
#         super().__init__(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Category Path is Empty: Category path must contain at least one category name"
#             if detail is None
#             else detail,
#         )
