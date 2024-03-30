#from sqlalchemy.orm import SessionLocal
from ..database import get_db, SessionLocal
from fastapi import APIRouter, Depends, HTTPException, status
from .. import oath2, models, sechma
from fuzzywuzzy import process


router = APIRouter()

@router.post('/product_types')
def add_product_type(product_type: sechma.ProductType,
                     current_user: str=Depends(oath2.get_current_user),
                     db:SessionLocal=Depends(get_db)):
    if not current_user.super_user:
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



@router.get('/products-category')
def get_products_category(db: SessionLocal = Depends(get_db)):
    return {'category': ['Casual Wear', 'Formal Attire', 'Sportswear', 'Business Casual', 'Uniforms']}


# @router.get('/products/category/{category}')
# def get_products_by_category(category: str, db: SessionLocal = Depends(get_db)):
#     product_type = db.query(models.ProductType).filter(models.ProductType.name == category).first()
#     if product_type is None:
#         return {"details": "Not found"}
#     products = db.query(models.Product).filter(models.Product.product_type_id == product_type.id).all()
#     return products 

@router.get('/products/category/{category}')
def get_products_by_category(category: str, db: SessionLocal = Depends(get_db)):
    all_categories = db.query(models.ProductType.name).all()
    all_categories = [cat[0] for cat in all_categories]
    closest_match, confidence = process.extractOne(category, all_categories)
    if confidence < 60:  
        return {"details": "Category not found"}
    product_type = db.query(models.ProductType).filter(models.ProductType.name == closest_match).first()
    products = db.query(models.Product).filter(models.Product.product_type_id == product_type.id).all()
    return products
    