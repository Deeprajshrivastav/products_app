from ..database import get_db, SessionLocal
from fastapi import APIRouter, Depends, HTTPException, status
from .. import oath2, models, sechma

router = APIRouter()


@router.post('/cart')
def product_cart(cart: sechma.Cart, current_user: models.User = Depends(oath2.get_current_user),
                 db: SessionLocal = Depends(get_db)):
    
    user_cart = db.query(models.Cart).filter(models.Cart.user_id == current_user.id).first()
    if not user_cart:
        user_cart = models.Cart(user_id=current_user.id)
        db.add(user_cart)
        db.commit()
        db.refresh(user_cart)
    
    for item in cart.item:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id {item.product_id} not found")
        
        cart_item = db.query(models.cart_association).filter(
                models.cart_association.c.cart_id == user_cart.id,
                models.cart_association.c.product_id == item.product_id
            ).first()
        
        if not cart_item:
            db.execute(models.cart_association.insert().values(
                cart_id=user_cart.id, product_id=product.id, quantity=item.quantity))
        else:
            db.execute(
                models.cart_association.update()
                .where(models.cart_association.c.cart_id == user_cart.id)
                .where(models.cart_association.c.product_id == item.product_id)
                .values(quantity=models.cart_association.c.quantity + item.quantity)
            )
        db.commit()
    db.refresh(user_cart)
    return user_cart


#@router.delete('/cart', status_code=status.HTTP_204_NO_CONTENT)
@router.delete('/deletecart/{product_id}/{quantity}', status_code=status.HTTP_204_NO_CONTENT)
def product_cart(product_id: int, quantity:int, 
                 current_user: models.User = Depends(oath2.get_current_user),
                 db: SessionLocal = Depends(get_db)):
    user_cart = db.query(models.Cart).filter(models.Cart.user_id == current_user.id).first()
    
    cart_item = db.query(models.cart_association).filter_by(cart_id=user_cart.id, product_id=product_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found in the cart")

    if cart_item.quantity > quantity:
        db.execute(
            models.cart_association.update()
            .where(models.cart_association.c.cart_id == user_cart.id)
            .where(models.cart_association.c.product_id == product_id)
            .values(quantity=models.cart_association.c.quantity - quantity)
        )
    else:
         db.execute(
            models.cart_association.delete()
            .where(models.cart_association.c.cart_id == user_cart.id)
            .where(models.cart_association.c.product_id == product_id)
        )
    db.commit()
    db.refresh(user_cart)
