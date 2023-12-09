from dependency_injector import containers, providers

from girok.domain.category.models import Category
from girok.domain.category.repository import CategoryRepository
from girok.domain.category.service import CategoryService


class CategoryContainer(containers.DeclarativeContainer):
    category_repository = providers.Factory(CategoryRepository, model=Category)
    category_service = providers.Factory(CategoryService, category_repository=category_repository)
