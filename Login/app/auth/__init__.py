from flask import Blueprint

authentication = Blueprint("authentication", __name__, template_folder="templates")
from Login.app.auth import routes