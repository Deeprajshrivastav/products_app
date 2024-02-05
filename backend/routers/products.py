#from sqlalchemy.orm import SessionLocal
from ..database import get_db, SessionLocal
from fastapi import APIRouter, Depends, HTTPException, status
from .. import oath2, models, sechma


router = APIRouter()

@router.post('/product_types')
def add_product_type(product_type: sechma.ProductType,
                     current_user: str=Depends(oath2.get_current_user),
                     db:SessionLocal=Depends(get_db)):
    if current_user.super_user:
        raise HTTPException(detail="Unauthorised to add product type",
                            status_code=status.HTTP_401_UNAUTHORIZED)
    
    product = models.ProductType(**product_type.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.post('/product_items')
def add_product_item(product: sechma.Product,
                     current_user: str=Depends(oath2.get_current_user),
                     db:SessionLocal=Depends(get_db)):
    product = models.Product(**product.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

"""
def buy_product(product: sechma.Product,
                current_user: str=Depends(oath2.get_current_user),
                db:SessionLocal=Depends(get_db)): 
"""

@router.post('/buy_product')
def create_order(order_data: sechma.OrderCreate, db:SessionLocal=Depends(get_db)):
    try:
        amount = 0
        totoal_quantity = 0
        user = db.query(models.User).filter(models.User.id == order_data.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        new_order = models.Order(user_id=order_data.user_id, amount=amount, totoal_quantity=totoal_quantity)
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        i = 0
        for product_data in order_data.products:
            product_id = product_data.product_id
            quantity = product_data.quantity
            
            new_order.totoal_quantity += product_data.quantity
            
            product = db.query(models.Product).filter(models.Product.id == product_id).first()
            amount += product.price * quantity
            #product.quantity = quantity
            if not product:
                raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")
            #product.quantity = quantity
            new_order.products.append(product)
            #print(new_order.products[0].quantity)
            db.commit()
            
        new_order.amount = amount
        db.commit()
        db.refresh(new_order)
        return new_order.products
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))