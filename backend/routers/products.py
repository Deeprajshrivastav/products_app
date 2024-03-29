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


@router.post('/buy_product')
def create_order(order_data: sechma.OrderCreate, 
                 current_user: models.User = Depends(oath2.get_current_user),
                 db: SessionLocal = Depends(get_db)):
    try:
        new_order = models.Order(user_id=current_user.id, amount=0, totoal_quantity=0)
        db.add(new_order)
        db.commit()

        for product_data in order_data.products:
            product_id = product_data.product_id
            quantity = product_data.quantity

            product = db.query(models.Product).filter(models.Product.id == product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")

            if product.stock < quantity:
                raise HTTPException(status_code=400, detail=f"Product {product.name} is out of stock")

            product.stock -= quantity
            new_order.amount += product.price * quantity
            new_order.totoal_quantity += quantity 

            db.execute(models.buy_product_association.insert().values(
                order_id=new_order.id, product_id=product.id, quantity=quantity))
        db.commit()
        db.refresh(new_order)
        return new_order.products
    
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Eror: {error}")

@router.get('/products-category')
def get_products_category(db: SessionLocal = Depends(get_db)):
    return {'category': ['Casual Wear', 'Formal Attire', 'Sportswear', 'Business Casual', 'Uniforms']}


@router.get('/products/category/{category}')
def get_products_by_category(category: str, db: SessionLocal = Depends(get_db)):
    product_type = db.query(models.ProductType).filter(models.ProductType.name == category).first()
    if product_type is None:
        return {"details": "Not found"}
    products = db.query(models.Product).filter(models.Product.product_type_id == product_type.id).all()
    return products 
    
    