from fastapi import FastAPI, Depends
from .routers import users, auth, products
from .database import SessionLocal, engine, get_db
from . import models
from . import oath2 


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(products.router)


@app.get("/")
def greet(current_user:str=Depends(oath2.get_current_user)):
    print(current_user)
    return {"message": current_user}