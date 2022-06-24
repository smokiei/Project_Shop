from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import join

from project.mod_main.forms import FilterProductsForm
from project.models import Order, Category, User, AttributesByCategory, Manufacturer

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
def index():
    return render_template('index.html')


@main_blueprint.route('/configurator')
@login_required
def configurator():
    filter_form = FilterProductsForm()
    filters = Category.query.all()
        #.outerjoin(Category.attributes_by_categories) \
        #.outerjoin(AttributesByCategory.Attribute) \
        #.all()
    manufacturers = Manufacturer.query.all()
    all_categories = Category.query.all()
    return render_template('main/configurator.html',
                           allCategories=all_categories,
                           filter_form=filter_form,
                           filters=filters,
                           manufacturers=manufacturers
                           )


@main_blueprint.route('/katalog')
@login_required
def katalog():
    return render_template('main.html')


@main_blueprint.route('/profile')
@login_required
def profile():
    return render_template('main/profile.html', current_user=current_user)


@main_blueprint.route('/myorders')
@login_required
def myorders():
    ###

    my_orders = Order.query. \
        join(User, User.id == Order.CreatedBy). \
        filter(User.id == current_user.id). \
        all()

    ### add check if there is no orders
    return render_template('main/myorders.html', my_orders=my_orders, current_user=current_user)

