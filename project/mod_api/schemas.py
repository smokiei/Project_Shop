from flask_marshmallow import Schema
from marshmallow import post_load, fields

from project import ma
from project.models import Category, Product, ProductsAttribute, AttributesByCategory, Attribute, Manufacturer, Photo


class ProductRequest:
    cat = None
    man = None

    def __init__(self, cat=None, man=None):
        self.cat = cat
        self.man = man


class ProductRequestSchema(Schema):
    cat = fields.Int(required=True)
    man = fields.Int()

    @post_load
    def make_pq(self, data, **kwargs):
        return ProductRequest(**data)


class AttributeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Attribute


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        include_fk = True


class AttributesByCategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AttributesByCategory
        include_fk = True


class ProductsAttributesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductsAttribute

    Attribute = fields.Nested(AttributeSchema())

    @post_load
    def make_pa(self, data, **kwargs):
        return ProductsAttribute(**data)


class ManufacturerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Manufacturer


class PhotosSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Photo


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        include_fk = True

    products_attributes = fields.Nested(ProductsAttributesSchema, many=True, partial=True)
    photos = fields.Nested(PhotosSchema, many=True)
    Manufacturer = fields.Nested(ManufacturerSchema)


class FilterSchema(ma.SQLAlchemyAutoSchema):
    products_attributes = fields.Nested(ProductsAttributesSchema, many=True, partial=True)

    class Meta:
        model = Attribute
        include_fk = True
