from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import sechma, utils, oath2
from fastapi import Depends
from ..database import SessionLocal, engine, get_db
from .. import models
from datetime import datetime, timedelta
import uuid

router = APIRouter(
    tags=['login']
)


@router.post('/login')
def login_user(user: OAuth2PasswordRequestForm=Depends(), db:SessionLocal = Depends(get_db)):
    user_login = db.query(models.User).filter(
        models.User.email == user.username or
        models.User.username == user.username).first()
    if not user_login:
        raise HTTPException(detail="Invalid username or password", status_code=403)
    if not utils.verify(user.password, user_login.password):
        raise HTTPException(detail="Invalid username or password", status_code=403)
    access_token = oath2.create_access_token({"user_id": user_login.id})
    return {'access_token': access_token, "token_type": "bearer"}


@router.post('/forgot-password')
async def forgot_password(forgot_password: sechma.ForgotPassword, db:SessionLocal = Depends(get_db), background_tasks: BackgroundTasks=None):
    user_login = db.query(models.User).filter(
        models.User.email == forgot_password.email).first()
    if not user_login:
        raise HTTPException(detail="User not found", status_code=404)
    reset_code = str(uuid.uuid1())
    reset_data = models.ResetCode(email=forgot_password.email, reset_code=reset_code)
    background_tasks.add_task(utils.send_reset_code, {'email':[forgot_password.email]}, reset_code)
    db.add(reset_data)
    db.commit()
    db.refresh(reset_data)  
    return reset_data


@router.post('/reset_password/{reset_token}')
async def reset_password(reset_token: str, reset_pswd: sechma.ResetPassword, db:SessionLocal = Depends(get_db)):
    reset_code_query = db.query(models.ResetCode).filter(
    models.ResetCode.reset_code == reset_token,
    models.ResetCode.created_at > datetime.now() - timedelta(minutes=5),
    models.ResetCode.status == False
    )
    if not reset_code_query.first():
       raise HTTPException(detail="Link is expired", status_code=403)
    reset_code = reset_code_query.first()
    
    user_login_query = db.query(models.User).filter(
        models.User.email == reset_code.email)
    user_login = user_login_query.first()
    
    reset_code.status = True
    user_login.password = utils.hashed_password(reset_pswd.new_password)
    db.commit()
    return {"msg": "password changed"}
   
   
    
