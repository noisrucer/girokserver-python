from datetime import timedelta

from fastapi import APIRouter, status, Depends, BackgroundTasks, HTTPException
from email_validator import validate_email, EmailNotValidError
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import EmailStr


from server.src.database import get_db
import server.src.auth.schemas as schemas
import server.src.auth.exceptions as exceptions
import server.src.auth.service as service
import server.src.auth.utils as utils
import server.src.auth.models as models
import server.src.dependencies as glob_dependencies
import server.src.utils as glob_utils
import server.src.user.models as user_models
import server.src.user.schemas as user_schemas
from server.src.auth.config import get_jwt_settings


jwt_settings = get_jwt_settings()

router = APIRouter(
    prefix="",
    tags=["auth"]
)


@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreateOut)
async def register(user: schemas.UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user_dict = user.dict()
    
    # Check if there's a duplicated email in the DB
    if service.get_current_active_user(db ,email=user_dict['email'], is_activate=True):
        raise exceptions.EmailAlreadyExistsException(email=user_dict['email'])   
    
    if service.get_current_active_user(db ,email=user_dict['email'], is_activate=False):
        update_user = db.query(user_models.User).filter(user_models.User.email==user_dict['email']).first()
        db.delete(update_user)
        db.commit()
    
    # Send verification code
    verification_code = utils.generate_verification_code(len=6)
    recipient = user_dict['email']
    subject="[Girok] Please verify your email address"
    content = utils.read_html_content_and_replace(
        replacements={"__VERIFICATION_CODE__": verification_code},
        html_path="server/src/email/verification.html"
    )
    background_tasks.add_task(glob_utils.send_email, recipient, content, subject)
    
    # Hash verification code
    hashed_verification_code = utils.hash_verification_code(verification_code)
    user_dict.update(verification_code=hashed_verification_code)
    
    # Hash password
    hashed_password = utils.hash_password(user_dict['password'])
    user_dict.update(password=hashed_password)
    
    new_user = user_models.User(**user_dict)
    db.add(new_user) 
    db.commit()
    db.refresh(new_user)
    
    return new_user

# 코드가 틀렸거나 없는 이메일이라면 오류를 내는 방식을 바꿔야함
@router.post("/register/verification_code", status_code=status.HTTP_200_OK)
async def verify_email(user: schemas.VerificationCode, db: Session = Depends(get_db)):
    user_dict = user.dict()
    
    user = db.query(user_models.User).filter(user_models.User.email == user_dict['email']).first()
    
    if service.get_current_active_user(db ,email=user_dict['email'], is_activate=True):
        raise exceptions.EmailAlreadyExistsException(email=user_dict['email'])   
    
    if not utils.verify_code(user_dict['verification_code'], user.verification_code):
        return False

    user.is_activate = True
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return "Email authentication is complete."


@router.post('/login', response_model=schemas.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
    ):
    user = service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise exceptions.InvalidEmailOrPasswordException()
    
    refresh_token_check = db.query(models.RefreshToken).filter(models.RefreshToken.user_id==user.user_id)
    if refresh_token_check.first():
        refresh_token_check.delete()
        db.commit()
        
    access_token = utils.create_access_token(data={"sub": user.email})
    refresh_token = utils.create_refresh_token(data={"sub": user.email})
    
    refresh_token_dict = {
        "user_id": user.user_id,
        "refresh_token": refresh_token
    }
    
    refresh_token_db = models.RefreshToken(**refresh_token_dict)
    db.add(refresh_token_db)
    db.commit()
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token
        }


@router.get("/refresh", status_code=status.HTTP_200_OK, response_model=schemas.Token)
async def get_new_access_token(token: str):
    refresh_data = utils.verify_refresh_token(token)
    
    new_access_token = utils.create_access_token(refresh_data.dict())
    
    return {
        "access_token": new_access_token,
        "refresh_token": token,
        "token_type": "Bearer",
    }


@router.get("/validate-access-token", dependencies=[Depends(glob_dependencies.get_current_user)])
async def validate_jwt():
    return {"detail": "validated"}