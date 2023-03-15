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
import server.src.dependencies as glob_dependencies
import server.src.utils as glob_utils
import server.src.user.models as user_models
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
    if service.get_user_by_email(db, email=user_dict['email']) and service.get_current_active_user(db, is_activate=True):
        raise exceptions.EmailAlreadyExistsException(email=user_dict['email'])
    
    if service.get_user_by_email(db, email=user_dict['email']):
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
    user_dict.update(verification_code=verification_code)
    
    # Hash password
    hashed_password = utils.hash_password(user_dict['password'])
    user_dict.update(password=hashed_password)
    
    new_user = user_models.User(**user_dict)
    db.add(new_user) 
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/register/verification_code", status_code=status.HTTP_200_OK)
async def verify_code(code: schemas.VerificationCode, db: Session = Depends(get_db)):
    verification_code = code.dict()
    
    user = db.query(user_models.User).filter(user_models.User.verification_code==verification_code['verification_code']).first()
    
    if not service.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    if not service.check_code(db, verification_code=user.verification_code):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
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
        
    access_token_expires = timedelta(minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    # refresh_token_expires = timedelta(minutes=jwt_settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    # refresh_token = utils.create_refresh_token(
    #     data={"sub": user.email},
    #     expires_delta=refresh_token_expires
    # )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/validate-access-token", dependencies=[Depends(glob_dependencies.get_current_user)])
async def validate_jwt():
    return {"detail": "validated"}