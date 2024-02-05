from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from .. import sechma
from fastapi import Depends
from ..database import SessionLocal, engine, get_db
from .. import models, utils

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