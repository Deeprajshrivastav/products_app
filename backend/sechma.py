from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class UserBaseModel(BaseModel):
    username: str
    email: EmailStr
    fullname: Optional[str] = None
    address: Optional[str] = None
    super_user: Optional[bool] = False

class UserSingup(UserBaseModel):
    password: str    
    class ConfigDict:
        from_attributes = True 
        
class UserOut(UserBaseModel):
    created_at: datetime
    class ConfigDict:
        from_attributes = True 

class UserLogin(BaseModel):
    username: str = None
    email: EmailStr = None

class TokenData(BaseModel):
    id: Optional[str] = None
    class ConfigDict:
        from_attributes = True
        
class ForgotPassword(BaseModel):
    email: str = None
    class ConfigDict:
        from_attributes = True

class EmailSchema(BaseModel):
    email: List[EmailStr]
    class ConfigDict:
        from_attributes = True

class ResetPassword(BaseModel):
    password: str
    class ConfigDict:
        from_attributes = True

class ChangedPassword(BaseModel):
    current_password: str
    new_password: str
    class ConfigDict:
        from_attributes = True

class ProductTypeBaseModel(BaseModel):
    name: str
    desc: Optional[str] = None

class ProductType(ProductTypeBaseModel):
    class ConfigDict:
        from_attributes = True
        
class ProductTypeReturn(ProductTypeBaseModel):
    id: int
    class ConfigDict:
        from_attributes = True

class ProductBaseModel(BaseModel):
    name: str
    stock: int
    price: int
    product_type_id: int

class Product(ProductBaseModel):
    class ConfigDict:
        from_attributes = True

    
class ProductQuantity(BaseModel):
    product_id: int
    quantity: int

class OrderBaseModel(BaseModel):
    products: List[ProductQuantity]

class OrderCreate(OrderBaseModel):
    class ConfigDict:
        from_attributes = True

class OrderSave(OrderBaseModel):
    amount: int
    class ConfigDict:
        from_attributes = True

class AddToCart(BaseModel):
    product_id: int
    quantity: int

class Cart(BaseModel):
    item: List[AddToCart]
    class ConfigDict:
        from_attributes = True

class MyCart(ProductBaseModel):
    quantity: int
    class ConfigDict:
        from_attributes = True
    