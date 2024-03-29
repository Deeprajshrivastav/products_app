from fastapi import APIRouter, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from .. import sechma
from fastapi import Depends
from ..database import SessionLocal, engine, get_db
from .. import models, utils, oath2
from datetime import datetime, timedelta
import uuid


router = APIRouter(
    tags=['Authentication']
)


@router.post('/singup', response_model=sechma.UserOut, status_code=201)
def singup_user(userdata: sechma.UserSingup, db:SessionLocal = Depends(get_db)):
    email_username = db.query(models.User).filter(
        models.User.email==userdata.email or 
        models.User.username==userdata.username).first()
    if email_username is not None:
        raise HTTPException(detail="Email or Username is already registered", status_code=403)
    userdata.password = utils.hashed_password(userdata.password)
    user = models.User(**userdata.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)    
    return user

@router.patch('/changed-password')
def changed_password(changed_password: sechma.ChangedPassword,
                     db:SessionLocal = Depends(get_db),
                     current_user: models.User = Depends(oath2.get_current_user)):

    if not utils.verify(changed_password.current_password, current_user.password):
        print("passwords do not match")
        raise HTTPException(detail="Password does not matched", status_code=403)
    current_user.password = utils.hashed_password(changed_password.new_password)
    return {"details": "password changed successfully"}
    
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


@router.patch('/reset_password/{reset_token}')
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
    user_login.password = utils.hashed_password(reset_pswd.password)
    db.commit()
    return {"msg": "password changed"}

@router.get('/profile')
def view_profile(current_user: models.User = Depends(oath2.get_current_user)):
    return {"username": current_user.username}


@router.patch('/profile')
def view_profile(user_profile: sechma.UserProfileUpdate,
                 db:SessionLocal = Depends(get_db), 
                 current_user: models.User = Depends(oath2.get_current_user)):
    current_user.fullname = user_profile.fullname
    current_user.address = user_profile.address
    db.commit()
    return {"msg": "profile updated"}

# @router