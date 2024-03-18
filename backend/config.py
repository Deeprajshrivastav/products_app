from pydantic import BaseModel

class Setting(BaseModel):
    database_hostname: str = 'localhost'
    database_password: str = '12345'
    database_port: str = '5432'
    database_name: str = 'products'
    database_username: str = 'postgres'
    secret_key: str = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
    algorithm: str = 'HS256'
    access_token_expire_minutes: int =  300000