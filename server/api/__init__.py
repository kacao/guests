from sanic import Blueprint
from .vouchers import blueprint as vouchers_bp

blueprint = Blueprint.group(vouchers_bp, url_prefix='/api')
