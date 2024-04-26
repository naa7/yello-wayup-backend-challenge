# URL Shortener

URL Shortener is implemented using Flask, a Python web framework. It provides functionalities for shortening long URLs into shorter ones, decoding shortened URLs to their original form, user authentication, and more.

## Features

- **URL Shortening**: Convert long URLs into shorter, more manageable ones.
- **URL Decoding**: Retrieve the original URL from a shortened URL.
- **User Authentication**: Register new users, log in, and log out with JWT authentication.
- **Admin Functionality**: Admin users can reset the database.

## Installation

1. Clone the repository:

```
git clone https://github.com/naa7/yello-wayup-backend-challenge.git
cd yello-wayup-backend-challenge/url-shortener/
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Set up environment variables:

Create a `.env` file in the project root directory and add the following variables:

```
FLASK_APP=app.py
FLASK_ENV=development
JWT_SECRET_KEY=YourSecretKey
MONGODB_URI=mongodb://localhost:27017/url_shortener
```

Replace `YourSecretKey` with a secret key for JWT authentication and `mongodb://localhost:27017/url_shortener` with the URI of your MongoDB instance.

## Usage

1. Start the Flask server:

```
flask run
```

2. Access the API endpoints:

- **User Authentication**: `/auth/signup` (POST), `/auth/login` (POST), `/auth/logout` (POST)
- **URL Shortening**: `/api/encode` (POST)
- **URL Decoding**: `/api/decode` (POST)

3. Interact with the URL Shortener using the provided client script or by sending HTTP requests directly.

## API Endpoints

- `/auth/signup`: Register a new user.
- `/auth/login`: Authenticate a user and generate JWT token.
- `/auth/logout`: Logout a user by invalidating JWT token.
- `/api/encode`: Encode a long URL into a short URL.
- `/api/decode`: Decode a short URL into the original long URL.

## Client Script

The `url_shortener.py` script provides a command-line interface for interacting with the URL Shortener. Run the script and follow the prompts to perform various operations such as signup, login, URL shortening, URL decoding, logout, and database reset (admin only).

```
python url_shortener.py
```
