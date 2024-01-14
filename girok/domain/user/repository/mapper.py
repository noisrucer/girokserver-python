from girok.domain.user.entity.user import User
from girok.domain.user.model.user import User as UserModel


def map_user_entity_to_model(user: User) -> UserModel:
    return UserModel(email=user.email, password=user.password)
