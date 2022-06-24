from flask import Blueprint, render_template
from project.models import Product


kat = Blueprint("kat", __name__)

@kat.route('/katalog')
def katalog():
    items = Product.query.order_by(Product.Price).all()
    return render_template('pricing.html', data=items)