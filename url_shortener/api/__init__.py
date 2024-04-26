from flask import Blueprint

# Create a Blueprint for authentication-related routes
api_bp = Blueprint("api", __name__)

# Import encode and decode routes from the api module
from api import encode, decode
