from flask import jsonify, request
from flask_jwt_extended import jwt_required
from api import api_bp
from db import url_collection
import hashlib
import random
import string
import base64


# Define a function to generate a short URL based on the given long URL
def generate_short_url(long_url):
    """
    Generate a short URL based on the given long URL.

    Args:
    - long_url (str): The long URL to be encoded.

    Returns:
    - str: The encoded short URL.
    """
    # Calculate SHA-256 hash of the long URL
    hash_obj = hashlib.sha256(long_url.encode())
    # Get the hexadecimal representation of the hash and take the first 16 characters
    hash_str = hash_obj.hexdigest()[:16]
    # Generate a random alphanumeric string of length 4
    random_str = "".join(random.choices(string.ascii_letters + string.digits, k=4))
    # Combine the hash and random string
    combined_str = hash_str + random_str
    # Encode the combined string using base64 and take the first 8 characters
    encoded_str = base64.b64encode(combined_str.encode()).decode()[:8]
    return encoded_str


# Define route for encoding long url
@api_bp.route("/encode", methods=["POST"])
# Require JWT token for accessing this route
@jwt_required()
def encode_url():
    """
    Encode a long URL into a short URL.

    This function receives a long URL from the request body, generates a short URL
    based on it, and stores the mapping between the long URL and short URL in the database.

    JSON Request Body:
    {
        "long_url": "example_long_url"
    }

    Returns:
    - If encoding is successful and the short URL is generated, returns a JSON response
      containing the short URL with a status code of 201 (Created).
    - If the long URL already exists in the database, returns the existing short URL
      associated with it with a status code of 200 (OK).
    - If the short URL already exists in the database, returns the existing short URL
      with a status code of 200 (OK).
    - If the long URL provided is invalid (does not start with 'http://' or 'https://'),
      returns an error message with a status code of 400 (Bad Request).
    - If the long URL is not provided in the request body, returns an error message
      indicating that the long URL was not provided with a status code of 400 (Bad Request).
    - If an unexpected error occurs during the encoding process, returns an error message
      with a status code of 500 (Internal Server Error).

    Raises:
    - ValueError: If the long URL is not provided in the request body.
    - Exception: If an unexpected error occurs during the encoding process.
    """
    try:
        # Get JSON data from the request
        data = request.get_json()
        # Extract the long URL from the JSON data
        long_url = data.get("long_url")

        # Check if long URL is provided
        if not long_url:
            raise ValueError("Long URL not provided")

        # Check if the URL starts with either "http://" or "https://"
        if not long_url.startswith(("http://", "https://")):
            return (
                jsonify(
                    {"error": "Only URLs starting with http:// or https:// are allowed"}
                ),
                400,
            )

        # Check if the long URL or its short form already exists in the database
        existing_long_url_mapping = url_collection.find_one({"long_url": long_url})
        existing_short_url_mapping = url_collection.find_one(
            {"short_url": long_url.split("/")[-1]}
        )

        if existing_long_url_mapping:
            # If the long_url already exists, return the associated short_url
            short_url = existing_long_url_mapping["short_url"]

        elif existing_short_url_mapping:
            # If the short URL already exists, return it
            short_url = existing_short_url_mapping["short_url"]

        else:
            # Generate a new short URL for the long URL
            short_url = generate_short_url(long_url)
            # Insert the mapping of short URL to long URL into the database
            url_collection.insert_one({"short_url": short_url, "long_url": long_url})
            # Return the short URL in the response
            return jsonify({"short_url": f"https://short.est/{short_url}"}), 201

        # Return the existing short URL in the response
        return jsonify({"short_url": f"https://short.est/{short_url}"}), 200

    except ValueError as ve:
        # Return an error message if long URL is not provided with status code 400
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        # Return error message with status code 500 if an unexpected error occurs
        return jsonify({"error": "An unexpected error occurred"}), 500
