from datetime import timedelta

from fastapi import APIRouter, status, Depends, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import EmailStr

from server.src.database import get_db
import server.src.auth.schemas as schemas
import server.src.auth.exceptions as exceptions
import server.src.auth.service as service
import server.src.auth.utils as utils
import server.src.dependencies as glob_dependencies
import server.src.utils as glob_utils
import server.src.user.models as user_models
import server.src.user.exceptions as user_exceptions
import server.src.user.service as user_service
from server.src.auth.config import get_jwt_settings

jwt_settings = get_jwt_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter(
    prefix="",
    tags=["auth"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreateOut)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_dict = user.dict()
        
    # Check if there's a duplicated email in the DB
    if service.get_user_by_email(db, email=user_dict['email']):
        raise exceptions.EmailAlreadyExistsException(email=user_dict['email'])
    
    # Hash password
    hashed_password = utils.hash_password(user_dict['password'])
    user_dict.update(password=hashed_password)

    # Save to DB
    new_user = user_models.User(**user_dict)
    db.add(new_user) 
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post('/login', response_model=schemas.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
    ):
    user = service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise exceptions.InvalidEmailOrPasswordException()
        
    access_token_expires = timedelta(minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/validate-access-token")
async def validate_jwt(current_user: user_models.User = Depends(glob_dependencies.get_current_user)):
    return {"current_user_email": current_user.email}