from flask import Blueprint
from flask_restful import Api

from project.mod_api.resources import CategoriesRes, ProductsRes, UsersRes, LoginRes, FiltersRes

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_blueprint)

api.add_resource(LoginRes, '/users/login')
api.add_resource(UsersRes, '/users/current')
api.add_resource(CategoriesRes, '/categories')
api.add_resource(ProductsRes, '/products')
api.add_resource(FiltersRes, '/filters')
