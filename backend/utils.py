from passlib.context import CryptContext
from .database import SessionLocal, engine, get_db
from . import models, config, sechma
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from starlette.responses import JSONResponse


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def hashed_password(password):
    return pwd_context.hash(password)


def verify(plain_password, hash_password):
    return pwd_context.verify(plain_password, hash_password)


async def send_reset_code(email: sechma.EmailSchema, reset_data: str):
    print(type(reset_data))
    html = """<p>Click on the below link to reset your password</p>
    <a href="http://localhost:3000/reset_password/{}"> click </a>""".format(reset_data)
    message = MessageSchema(
        subject="Reset your password",
        recipients=email.get("email"),
        body=html,
        subtype=MessageType.html)
    fm = FastMail(config.mailconfig)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"}) 