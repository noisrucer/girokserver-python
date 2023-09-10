from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.orm import Session

import src.user.models as user_models

def get_user_id_by_email(db: Session, email: str):
    user = db.query(user_models.User).\
        filter(user_models.User.email == email).\
        first()
        
    if not user:
        return None
    return user.user_id