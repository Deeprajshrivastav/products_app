from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import Setting
from sqlalchemy.orm import declarative_base
setting  = Setting()

Base = declarative_base()

SQLALCHEMY_DATABASE_URL = (f"postgresql+psycopg2://{setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()    