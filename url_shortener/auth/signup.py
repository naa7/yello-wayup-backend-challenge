from flask import jsonify, request
from auth import auth_bp
from flask_jwt_extended import create_access_token
from datetime import timedelta
from db import user_collection
import hashlib

# Set token expiry duration to 5 hours
TOKEN_EXPIRY_DURATION = timedelta(hours=5)

# Define route for user signup


@auth_bp.route("/signup", methods=["POST"])
def signup():
    """
    Register a new user.

    This function receives the username and password from the request body,
    checks if they are provided, verifies if the username is available, hashes
    the password using SHA-256, and inserts the new user into the database. If
    the signup process is successful, it generates a JWT access token for the
    new user, which expires after a predefined duration, and returns it in the
    response.

    JSON Request Body:
    {
        "username": "example_user",
        "password": "example_password"
    }
    
    Returns:
    - If signup is successful and a JWT access token is generated, returns a
      JSON response containing the access token with a status code of 201 (Created).
    - If the username or password is missing in the request body, returns an
      error message indicating that they were not provided with a status code
      of 400 (Bad Request).
    - If the provided username already exists in the database, returns an error
      message indicating that the username is already taken with a status code
      of 400 (Bad Request).
    - If an unexpected error occurs during the signup process, returns an error message
      with a status code of 500 (Internal Server Error).

    Raises:
    - ValueError: If the username or password is missing in the request body.
    - Exception: If an unexpected error occurs during the signup process.
    """

    try:
        # Get JSON data from request body
        data = request.get_json()
        # Extract username from JSON data
        username = data.get("username")
        # Extract password from JSON data
        password = data.get("password")

        # Check if username or password is missing
        if not username or not password:
            raise ValueError("Username or password not provided")

        # Check if username already exists in the database
        if user_collection.find_one({"username": username}):
            return jsonify({"error": "Username already exists"}), 400

        # Hash the password using SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Insert new user into the user collection
        user_collection.insert_one({"username": username, "password": hashed_password})

        # Create an access token for the new user
        access_token = create_access_token(
            identity=username, expires_delta=TOKEN_EXPIRY_DURATION
        )

        # Return the access token as JSON response
        return jsonify(access_token=access_token), 201

    except ValueError as ve:
        # Return an error message if username or password is missing
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        # Return an error message if an unexpected error occurs
        return jsonify({"error": "An unexpected error occurred"}), 500
