from datetime import timedelta
from pymongo import MongoClient
import os

# Get MongoDB URI from environment variable, default to localhost if not set
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/url_shortener")

# Connect to MongoDB
client = MongoClient(MONGODB_URI)

# Get the default database
db = client.get_default_database()

# Collection for storing user data
user_collection = db["users"]

# Collection for storing URL mappings
url_collection = db["urls"]

# Collection for storing revoked tokens
revoked_token_collection = db["revoked_tokens"]

# Expiry duration for JWT tokens
TOKEN_EXPIRY_DURATION = timedelta(hours=5)

# Convert expiry duration to seconds
expiry_seconds = TOKEN_EXPIRY_DURATION.total_seconds()

# Create index on 'created_at' field in revoked token collection for automatic expiration
revoked_token_collection.create_index("created_at", expireAfterSeconds=expiry_seconds)
