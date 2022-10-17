from flask import render_template
from flask_login import current_user
import datetime

from .models.inventory import Inventory

from flask import Blueprint
bp = Blueprint('inventories', __name__)


@bp.route('/inventory', methods=['GET', 'POST'])
def inventory():
    seller_id = 0
    inv = Inventory.get(seller_id)
    return render_template('inventory.html',
                            sid = seller_id
                           inventory_products=inv)
    


