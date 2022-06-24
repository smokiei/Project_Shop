# # coding: utf-8
from flask_login import UserMixin
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

from project import db

ACCESS = {
    'guest': 0,
    'user': 1,
    'admin': 77
}

AccessLevelForAdmin = 77

db.metadata.clear()


class Attribute(db.Model):
    __tablename__ = 'Attributes'

    AttributeId = db.Column(db.Integer, primary_key=True)
    AttributeTitle = db.Column(db.Text, nullable=False, unique=True)


class AttributesByCategory(db.Model):
    __tablename__ = 'AttributesByCategories'
    __table_args__ = (
        db.UniqueConstraint('CategoryId', 'AttributeId'),
    )

    AttributeInCategoryId = db.Column(db.Integer, primary_key=True)
    AttributeId = db.Column(db.ForeignKey('Attributes.AttributeId'), nullable=False, index=True)
    CategoryId = db.Column(db.ForeignKey('Categories.CategoryId'), nullable=False, index=True)

    Attribute = db.relationship('Attribute', primaryjoin='AttributesByCategory.AttributeId == Attribute.AttributeId',
                                backref='attributes_by_categories')
    Category = db.relationship('Category', primaryjoin='AttributesByCategory.CategoryId == Category.CategoryId',
                               backref='attributes_by_categories')


class Category(db.Model):
    __tablename__ = 'Categories'

    CategoryId = db.Column(db.Integer, primary_key=True)
    CategoryName = db.Column(db.Text, nullable=False, unique=True)

    def __repr__(self):
        return f'{self.CategoryId}. {self.CategoryName}'


#
#
# class Compatibility(db.Model):
#     __tablename__ = 'Compatibilities'
#     __table_args__ = (
#         db.UniqueConstraint('ProductId1', 'ProductId2'),
#     )
#
#     CompatibilityId = db.Column(db.Integer, primary_key=True)
#     ProductId1 = db.Column(db.ForeignKey('Products.ProductId'), nullable=False, index=True)
#     ProductId2 = db.Column(db.ForeignKey('Products.ProductId'), nullable=False, index=True)
#
#     Product = db.relationship('Product', primaryjoin='Compatibility.ProductId1 == Product.ProductId',
#                               backref='product_compatibilities')
#     Product1 = db.relationship('Product', primaryjoin='Compatibility.ProductId2 == Product.ProductId',
#                                backref='product_compatibilities_0')


class Manufacturer(db.Model):
    __tablename__ = 'Manufacturers'

    ManufacturerId = db.Column(db.Integer, primary_key=True)
    CompanyName = db.Column(db.Text, nullable=False, unique=True)


class Order(db.Model):
    __tablename__ = 'Orders'

    OrderId = db.Column(db.Integer, primary_key=True)
    CreatedBy = db.Column(db.ForeignKey('Users.UserId'), nullable=False, index=True)
    CreatedWhen = db.Column(db.Text)

    CreatedByUser = db.relationship('User', primaryjoin='Order.CreatedBy == User.id', backref='orders')

    # select sum(products.price)
    #  FROM
    #  Products
    # inner JOIN
    # (SELECT ProductsInOrders.ProductId from ProductsInOrders WHERE ProductsInOrders.orderid= @CurrentOrderId) t2
    # on Products.ProductId = t2.ProductId

    def totalamount(self):
        qw = ProductsInOrder.query.filter(ProductsInOrder.OrderId == self.OrderId).subquery()
        qw1 = Product.query.join(qw, Product.ProductId == qw.c.ProductId).subquery()
        sum = Product.query.with_entities(func.sum(qw1.c.Price).label('total')).first().total

        return sum


class Photo(db.Model):
    __tablename__ = 'Photos'

    PhotoId = db.Column(db.Integer, primary_key=True)
    ProductId = db.Column(db.ForeignKey('Products.ProductId'), nullable=True, index=True)
    FileName = db.Column(db.Text, nullable=False)
    Product = db.relationship('Product', primaryjoin='Photo.ProductId == Product.ProductId', backref='photos')

    def file_path(self):
        return f'static/photos/{self.ProductId}/{self.FileName}'


class Product(db.Model):
    __tablename__ = 'Products'

    ProductId = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.Text, nullable=False, unique=True)
    CategoryId = db.Column(db.ForeignKey('Categories.CategoryId'), index=True)
    ManufacturerId = db.Column(db.ForeignKey('Manufacturers.ManufacturerId'), nullable=False, index=True)
    StockQuantity = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    Price = db.Column(db.Float, nullable=False)
    Category = db.relationship('Category', primaryjoin='Product.CategoryId == Category.CategoryId', backref='products')
    Manufacturer = db.relationship('Manufacturer', primaryjoin='Product.ManufacturerId == Manufacturer.ManufacturerId',
                                   backref='products')


class ProductsAttribute(db.Model):
    __tablename__ = 'ProductsAttributes'

    ProductAttributeId = db.Column(db.Integer, primary_key=True)
    ProductId = db.Column(db.ForeignKey('Products.ProductId'), nullable=False, index=True)
    AttributeId = db.Column(db.ForeignKey('Attributes.AttributeId'), nullable=False, index=True)
    AttributeValue = db.Column(db.Text, nullable=False)

    Attribute = db.relationship('Attribute', primaryjoin='ProductsAttribute.AttributeId == Attribute.AttributeId',
                                backref='products_attributes')
    Product = db.relationship('Product', primaryjoin='ProductsAttribute.ProductId == Product.ProductId',
                              backref='products_attributes')


class ProductsInOrder(db.Model):
    __tablename__ = 'ProductsInOrders'

    ProductOrderId = db.Column(db.Integer, primary_key=True)
    ProductId = db.Column(db.ForeignKey('Products.ProductId'), index=True)
    OrderId = db.Column(db.ForeignKey('Orders.OrderId'), index=True)

    Order = db.relationship('Order', primaryjoin='ProductsInOrder.OrderId == Order.OrderId',
                            backref='products_in_orders')
    Product = db.relationship('Product', primaryjoin='ProductsInOrder.ProductId == Product.ProductId',
                              backref='products_in_orders')


# Define a User model
class User(db.Model, UserMixin):
    __tablename__ = 'Users'

    id = db.Column('UserId', db.Integer, primary_key=True)
    UserName = db.Column(db.Text, nullable=False)
    Email = db.Column(db.Text, nullable=False)
    Password = db.Column(db.Text, nullable=False)
    Access = db.Column(db.Integer, nullable=False)

    @classmethod
    def from_signup(cls, name, password, email):
        return cls(
            UserName=name,
            Password=generate_password_hash(password, method='sha256'),
            Email=email,
            Access=1
        )

    def __repr__(self):
        return f'User {self.id} {self.UserName} {self.Email}'

    def is_admin(self):
        return self.Access >= AccessLevelForAdmin

    def hash_password(self, new_password):
        self.Password = generate_password_hash(new_password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.Password, password)
