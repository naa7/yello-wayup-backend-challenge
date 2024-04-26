from flask import jsonify, request
from auth import auth_bp
from flask_jwt_extended import create_access_token
from datetime import timedelta
from db import user_collection
import hashlib

# Define token expiry duration as 5 hours
TOKEN_EXPIRY_DURATION = timedelta(hours=5)


# Define route for user login
@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticate a user and generate a JWT access token for login.

    This function receives the username and password from the request body, checks
    if they are provided, searches for the user in the database by username, and
    verifies the provided password against the hashed password stored in the database.
    If authentication is successful, it generates a JWT access token for the user,
    which expires after a predefined duration, and returns it in the response.

    JSON Request Body:
    {
        "username": "example_user",
        "password": "example_password"
    }
    
    Returns:
    - If authentication is successful and a JWT access token is generated, returns
      a JSON response containing the access token with a status code of 200 (OK).
    - If the username or password is not provided in the request body, returns an
      error message indicating that they were not provided with a status code of
      400 (Bad Request).
    - If the provided username does not exist or the password is incorrect, returns
      an error message indicating invalid credentials with a status code of 401 (Unauthorized).
    - If an unexpected error occurs during the login process, returns an error message
      with a status code of 500 (Internal Server Error).

    Raises:
    - ValueError: If the username or password is not provided in the request body.
    - Exception: If an unexpected error occurs during the login process.
    """

    try:
        # Get JSON data from the request
        data = request.get_json()
        # Extract username from JSON data
        username = data.get("username")
        # Extract password from JSON data
        password = data.get("password")

        # Check if username or password is not provided
        if not username or not password:
            raise ValueError("Username or password not provided")

        # Find user by username in the database
        user = user_collection.find_one({"username": username})

        # Check if user doesn't exist or password is incorrect
        if (
            not user
            or user["password"] != hashlib.sha256(password.encode()).hexdigest()
        ):
            # Return error message with status code 401
            return jsonify({"error": "Invalid credentials"}), 401

        # Generate JWT access token for the authenticated user
        access_token = create_access_token(
            identity=username, expires_delta=TOKEN_EXPIRY_DURATION
        )
        # Return JWT access token with status code 200
        return jsonify(access_token=access_token), 200

    except ValueError as ve:
        # Return an error message if username or password is not provided with status code 400
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        # Return error message with status code 500 if an unexpected error occurs
        return jsonify({"error": "An unexpected error occurred"}), 500
