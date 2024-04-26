from flask import jsonify, request
from flask_jwt_extended import jwt_required
from api import api_bp
from db import url_collection


# Define route for decoding short url
@api_bp.route("/decode", methods=["POST"])
# Require JWT token for accessing this route
@jwt_required()
def decode_url():
    """
    Decode a short URL to its corresponding long URL.

    This function receives a short URL from the request body, extracts its identifier,
    and searches for the corresponding long URL in the database. If the short URL is found
    in the database, it returns the associated long URL; otherwise, it returns an error
    message indicating that the short URL was not found.

    JSON Request Body:
    {
        "short_url": "example_short_url"
    }

    Returns:
    - If decoding is successful and the long URL is found, returns a JSON response
      containing the long URL with a status code of 200 (OK).
    - If the short URL is not found in the database, returns an error message with a
      status code of 404 (Not Found).
    - If the short URL is not provided in the request body, returns an error message
      indicating that the short URL was not provided with a status code of 400 (Bad Request).
    - If an unexpected error occurs during the encoding process, returns an error message
      with a status code of 500 (Internal Server Error).

    Raises:
    - ValueError: If the short URL is not provided in the request body.
    - Exception: If an unexpected error occurs during the decoding process.
    """

    try:
        # Get JSON data from the request
        data = request.get_json()
        # Extract short URL from JSON data
        short_url = data.get("short_url")
        # Extract the short URL's identifier from the last part of the URL
        short_url = short_url.split("/")[-1]

        # Check if short URL is provided
        if not short_url:
            raise ValueError("Short URL not provided")

        # Find the URL mapping in the database using the short URL
        url_mapping = url_collection.find_one({"short_url": short_url})

        # Check if URL mapping is found
        if not url_mapping:
            # Return error message with status code 404 if short URL is not found
            return jsonify({"error": "Short URL not found"}), 404

        # Return the long URL associated with the short URL with status code 200
        return jsonify({"long_url": url_mapping["long_url"]}), 200

    except ValueError as ve:
        # Return an error message if short URL is not provided with status code 400
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        # Return error message with status code 500 if an unexpected error occurs
        return jsonify({"error": "An unexpected error occurred"}), 500
