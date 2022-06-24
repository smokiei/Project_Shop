from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, current_user
from flask_restful import Resource
from sqlalchemy import and_

from project.mod_api.schemas import CategorySchema, ProductsAttributesSchema, FilterSchema, ProductSchema, \
     ProductRequestSchema
from project.models import Category, Product, User, Attribute, AttributesByCategory


class CategoriesRes(Resource):
    def get(self):
        cats = Category.query.all()
        cat_schema = CategorySchema(many=True)
        return cat_schema.dump(cats)


class ProductsRes(Resource):
    def get(self):
        request_schema = ProductRequestSchema()
        errors = request_schema.validate(request.args)
        if errors:
            return errors

        request_args = request_schema.load(request.args)
        filters = and_(Product.CategoryId == request_args.cat)
        if request_args.man > 0:
            filters = and_(filters, Product.ManufacturerId == request_args.man)

        data = Product.query.filter(filters).all()
        response_schema = ProductSchema(many=True)
        return response_schema.dump(data)

    @staticmethod
    def post():
        filter_schema = ProductsAttributesSchema(many=True, partial=True)
        errors = filter_schema.validate(request.get_json())
        example = filter_schema.load(request.get_json())

        prods = Product.query.all()
        # prod_schema = ProductSchema(many=True)
        # return prod_schema.dump(prods)


class LoginRes(Resource):
    def post(self):
        body = request.get_json()
        user = User.query.filter(User.UserName == body.get('login')).first()
        if user and user.check_password(body.get('pwd')):
            access_token = create_access_token(identity=str(user.id))
            return {'token': access_token}, 200
        return {'unauthorized', 401}


class UsersRes(Resource):
    @jwt_required()
    def get(self):
        return jsonify(
            id=current_user.id,
            name=current_user.UserName
        )


class FiltersRes(Resource):
    # @jwt_required()
    def get(self):
        filter_schema = FilterSchema(many=True, partial=True)
        filter_data = Attribute.query.where(AttributesByCategory.CategoryId == 1)

        # abc_data = db.session \
        # .query(Attribute.AttributeId,
        #        Attribute.AttributeTitle,
        #        ProductsAttribute.AttributeValue,
        #        func.count(ProductsAttribute.ProductAttributeId)
        #        ) \
        # .join(Attribute.attributes_by_categories) \
        # .join(Attribute.products_attributes) \
        # .group_by(Attribute.AttributeId,
        #           Attribute.AttributeTitle,
        #           ProductsAttribute.AttributeValue
        #           ) \
        # .order_by(Attribute.AttributeTitle) \
        # .where(AttributesByCategory.CategoryId == 1)

        dumped = filter_schema.dump(filter_data)
        return dumped
