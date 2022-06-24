import os

from flask import Blueprint, render_template, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from project.mod_admin.forms import ProductCreateForm
from project.models import Order

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@admin_blueprint.route('orders')
@login_required
def orders():
    all_orders = Order.query.all()
    return render_template('admin/orders.html', all_orders=all_orders, current_user=current_user)


@admin_blueprint.route('/products/create', methods=['GET', 'POST'])
@login_required
def products_create():
    form_products_create = ProductCreateForm()
    if form_products_create.validate_on_submit():
        filename = secure_filename(form_products_create.Photo.data.filename)
        path_to_uploads = os.path.join(current_app.config['BASE_DIR'], 'project', 'uploads', filename)
        form_products_create.Photo.data.save(path_to_uploads)
        flash('Товар додано. %s !' % form_products_create.Title)
    return render_template('admin/products-create.html', form_products_create=form_products_create)
