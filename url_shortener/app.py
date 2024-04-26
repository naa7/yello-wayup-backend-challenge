import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from db import revoked_token_collection
from auth import auth_bp
from api import api_bp

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# Set the secret key for JWT
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "SecretKey")


# Initialize JWT extension with the Flask app
jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(_, jwt_data):
    """
    Check if a JWT access token is in the blacklist of revoked tokens.

    This function is a callback function registered as a token loader with
    Flask JWT Extended. It is invoked during token validation to check if
    the token is revoked by querying the database of revoked tokens.

    Args:
    - _: Placeholder for the JWT header (not used).
    - jwt_data (dict): The decrypted payload of the JWT token.

    Returns:
    - If the token is found in the database of revoked tokens, returns a JSON
      response with an error message indicating that the token has been revoked,
      with a status code of 401 (Unauthorized).
    - If the token is not found in the database of revoked tokens, returns None,
      indicating that the token is not revoked, and processing can continue.

    """

    # Get the JWT token ID (jti) from the decrypted token
    jti = jwt_data["jti"]

    # Check if the token's jti is in the database of revoked tokens
    if revoked_token_collection.find_one({"token": jti}):
        return jsonify({"error": "Token has been revoked"}), 401

    # Token not revoked, continue processing
    return None


# Register the API blueprint with URL prefix '/api'
app.register_blueprint(api_bp, url_prefix="/api")

# Register the authentication blueprint with URL prefix '/auth'
app.register_blueprint(auth_bp, url_prefix="/auth")

if __name__ == "__main__":
    app.run(debug=True)
