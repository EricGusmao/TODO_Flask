from flask import Blueprint

bp = Blueprint('painel', __name__)

from app.painel import routes