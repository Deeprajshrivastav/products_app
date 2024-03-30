from ..database import get_db, SessionLocal
from fastapi import APIRouter, Depends, HTTPException, status
from .. import oath2, models, sechma


router = APIRouter()


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