from flask import jsonify, request
from flask_jwt_extended import decode_token, jwt_required
from auth import auth_bp
from db import revoked_token_collection


# Define route for user logout
@auth_bp.route("/logout", methods=["POST"])
# Require JWT token for accessing this route
@jwt_required()
def logout():
    """
    Log out a user by revoking the JWT access token.

    This function receives a JWT access token from the request headers, decodes it
    to extract the token ID (jti), and adds the token ID to the database of revoked tokens.
    This effectively logs out the user by marking the token as revoked.

    Returns:
    - If the logout process is successful, returns a JSON response with a success message
      indicating that the user has been successfully logged out, with a status code of 200 (OK).
    - If an unexpected error occurs during the logout process, returns an error message
      with a status code of 500 (Internal Server Error).

    Raises:
    - Exception: If an unexpected error occurs during the logout process.
    """
    try:
        # Get the JWT token from the request headers
        jwt_token = request.headers.get("Authorization").split("Bearer ")[-1]

        # Decode the JWT token to extract the token ID (jti)
        jwt_data = decode_token(jwt_token)

        # Extract the token ID (jti)
        jti = jwt_data["jti"]

        # Add the token to the database of revoked tokens
        revoked_token_collection.insert_one({"token": jti})

        # Return a success message
        return jsonify(message="Successfully logged out"), 200

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": "An unexpected error occurred"}), 500
