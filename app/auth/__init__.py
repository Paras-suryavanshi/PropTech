from flask import Blueprint
# 'auth' is the name of the blueprint.
auth_bp = Blueprint('auth', __name__)
from . import routes