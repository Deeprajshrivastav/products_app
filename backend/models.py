from sqlalchemy import Enum, create_engine, Column, Integer, String, ForeignKey, Table, TIMESTAMP, text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import PrimaryKeyConstraint

Base = declarative_base()

class OrderStatusEnum(Enum):
    pending = 'pending'
    success = 'success'
    cancelled = 'cancelled'

buy_product_association = Table(
    'buy_product_association',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id')),
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('quantity', Integer),
)

cart_association = Table(
    'cart_association',
    Base.metadata,
    Column('cart_id', Integer, ForeignKey('carts.id')),
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('quantity', Integer),
    PrimaryKeyConstraint('cart_id', 'product_id')
)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    fullname = Column(String)
    email = Column(String, nullable=False)
    password = Column(String)
    address = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
    super_user = Column(Boolean, default=False )
    orders = relationship('Order', back_populates='user')
    cart = relationship('Cart', back_populates='user')

class ResetCode(Base):
    __tablename__ = 'reset_codes'
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    reset_code = Column(String, nullable=False)
    status = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))


class ProductType(Base):
    __tablename__ = 'product_types'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, unique=True, nullable=True)
    desc = Column(String)


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    stock = Column(Integer)
    price = Column(Integer)
    product_type_id = Column(Integer, ForeignKey('product_types.id'))
    name = Column(String, index=True)
    description = Column(String)
    image_url = Column(String)
    product_type = relationship('ProductType')
    orders = relationship('Order', secondary=buy_product_association, back_populates='products')
    carts = relationship('Cart', secondary=cart_association, back_populates='items')


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    products = relationship('Product', secondary=buy_product_association, back_populates='orders')
    #status = Column(Enum(OrderStatusEnum, name='order_status_enum'))
    amount = Column(Integer)
    totoal_quantity = Column(Integer)
    user = relationship('User', back_populates='orders')



class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship('User', back_populates='cart')
    items = relationship('Product', secondary=cart_association, back_populates='carts')



# from sqlalchemy import create_engine, Column, Boolean, Integer, String, ForeignKey, Table, Enum, TIMESTAMP, text
# from sqlalchemy.orm import relationship
# from .database import Base


# class OrderStatusEnum(str, Enum):
#     pending = 'pending'
#     success = 'success'
#     cancelled = 'cancelled'
    
# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True, nullable=False)
#     username = Column(String, nullable=False)
#     fullname = Column(String)
#     email = Column(String, nullable=False)
#     password = Column(String)
#     address = Column(String, nullable=True)
#     created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
#     super_user = Column(Boolean, default=False )
#     #profile_pic = Column(String)  # Assuming a file path or URL for simplicity

#     orders = relationship('Order', back_populates='user')

# class ProductType(Base):
#     __tablename__ = 'product_types'
#     id = Column(Integer, primary_key=True, nullable=False)
#     name = Column(String, unique=True, nullable=True)
#     desc = Column(String)


# class Product(Base):
#     __tablename__ = 'products'

#     id = Column(Integer, primary_key=True, index=True)
#     stock = Column(Integer)
#     price = Column(Integer)
#     product_type_id = Column(Integer, ForeignKey('product_types.id'))
#     name = Column(String, index=True)
#     product_type = relationship('ProductType')

# # class BuyProduct(Base):
# #     product_id = Column(Integer)
# #     quantity = Column(Integer)

# buy_product_association = Table(
#     'buy_product_association',
#     Base.metadata,
#     Column('order_id', Integer, ForeignKey('orders.id')),
#     Column('product_id', Integer, ForeignKey('products.id')),
#     Column('quantity', Integer),
# )

# class Order(Base):
#     __tablename__ = 'orders'
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))    
#     products = relationship('Product', secondary=buy_product_association, back_populates='Order')
#     status = OrderStatusEnum
#     amount = Column(Integer)
#     user = relationship('User', back_populates='Order')

    # Establishing relationship with User





"""

class OrderStatusEnum(str, Enum):
    pending = 'pending'
    success = 'success'
    cancelled = 'cancelled'

order_product_association = Table(
    'order_product_association',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id')),
    Column('product_id', Integer, ForeignKey('products.id'))
)

class ProductType(Base):
    __tablename__ = 'product_types'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    number_quantity = Column(Integer)

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    stock = Column(Integer)
    price = Column(Integer)
    product_type_id = Column(Integer, ForeignKey('product_types.id'))
    name = Column(String, index=True)

    product_type = relationship('ProductType', back_populates='products')

    orders = relationship('Order', secondary=order_product_association, back_populates='products')

# User Model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    fullname = Column(String)
    email = Column(String, index=True)
    password = Column(String)
    address = Column(String)
    #profile_pic = Column(String)  # Assuming a file path or URL for simplicity

    #orders = relationship('Order', back_populates='user')

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))

    status = Column(Enum(OrderStatusEnum))
    amount = Column(Integer)
    user = relationship('User', back_populates='orders')

    products = relationship('Product', secondary=order_product_association, back_populates='orders')

class Transaction(Base):
    __tablename__ = 'transactions'

    order_id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(OrderStatusEnum))

ProductType.products = relationship('Product', back_populates='product_type')
Product.orders = relationship('Order', back_populates='products')
User.orders = relationship('Order', back_populates='user')

"""