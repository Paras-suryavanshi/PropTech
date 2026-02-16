from flask import Blueprint
# 'main' is the name of the blueprint.
main_bp = Blueprint('main', __name__)
from . import routes