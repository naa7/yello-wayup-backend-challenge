from flask import Blueprint

# Create a Blueprint for authentication-related routes
auth_bp = Blueprint("auth", __name__)

# Import login, logout, and signup routes from the auth module
from auth import login, logout, signup
