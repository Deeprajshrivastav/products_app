from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_
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
    user_login = db.query(models.User).filter(or_(
        models.User.email == user.username,
        models.User.username == user.username)).first()
    if not user_login:
        raise HTTPException(detail="Invalid username or password", status_code=403)
    if not utils.verify(user.password, user_login.password):
        raise HTTPException(detail="Invalid username or password", status_code=403)
    access_token = oath2.create_access_token({"user_id": user_login.id})
    return {'access_token': access_token, "token_type": "bearer"}



   
   
    
