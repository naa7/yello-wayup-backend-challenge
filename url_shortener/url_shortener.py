import requests
import sys
from pymongo import MongoClient

# MongoDB connection settings
MONGODB_URI = "mongodb://localhost:27017/"

# Define the URL of the Flask server
flask_url = "http://localhost:5000"


def signup(username, password):
    """
    Register a new user using the Flask server.

    Args:
    - username (str): The username of the new user.
    - password (str): The password of the new user.

    Returns:
    - If signup is successful and a JWT access token is generated, returns a
      string representing the access token.
    - If the signup process fails, returns None.

    Raises:
    - Exception: If an unexpected error occurs during the signup process.
    """
    try:
        # Send a POST request to the /auth/signup endpoint
        response = requests.post(
            f"{flask_url}/auth/signup",
            json={"username": username, "password": password},
        )

        # Check if the request was successful
        if response.status_code == 201:
            print("Signup successful! Logging in...")
            # Extract and return the JWT token from the response
            return response.json().get("access_token")
        else:
            # Print error message if request was not successful
            print("Error:", response.text)
            return None

    except Exception as e:
        print("An error occurred:", str(e))
        return None


def login(username, password):
    """
    Authenticate user and obtain JWT token using the Flask server.

    Args:
    - username (str): The username of the user.
    - password (str): The password of the user.

    Returns:
    - If login is successful and a JWT access token is generated, returns a
      string representing the access token.
    - If the login process fails, returns None.

    Raises:
    - Exception: If an unexpected error occurs during the login process.
    """
    try:
        # Send a POST request to the /auth/login endpoint
        response = requests.post(
            f"{flask_url}/auth/login", json={"username": username, "password": password}
        )

        # Check if the request was successful
        if response.status_code == 200:
            # Extract and return the JWT token from the response
            return response.json().get("access_token")
        else:
            # Print error message if request was not successful
            print("Error:", response.text)
            return None

    except Exception as e:
        print("An error occurred:", str(e))
        return None


def logout(jwt_token):
    """
    Logout a user by invalidating the JWT token.

    Args:
    - jwt_token (str): The JWT token to be invalidated.

    Returns:
    - If logout is successful, returns True.
    - If logout fails, returns False.

    Raises:
    - Exception: If an unexpected error occurs during the logout process.
    """
    try:
        # Send a POST request to the /auth/logout endpoint with the JWT token in the headers
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = requests.post(f"{flask_url}/auth/logout", headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            print("Logout successful!")
            return True
        else:
            # Print error message if request was not successful
            print("Error:", response.text)
            return False

    except Exception as e:
        print("An error occurred:", str(e))
        return False


def shorten_url(long_url, jwt_token):
    """
    Encode a long URL using the Flask server with JWT token authentication.

    Args:
    - long_url (str): The long URL to be encoded.
    - jwt_token (str): The JWT token for authentication.

    Returns:
    - If encoding is successful and a short URL is generated, returns a string
      representing the short URL.
    - If the encoding process fails, returns None.

    Raises:
    - Exception: If an unexpected error occurs during the encoding process.
    """
    try:
        # Send a POST request to the /api/encode endpoint with JWT token in the headers
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = requests.post(
            f"{flask_url}/api/encode", json={"long_url": long_url}, headers=headers
        )

        # Check if the request was successful (status code 201 or 200)
        if response.status_code == 201 or response.status_code == 200:
            # Extract and return the shortened URL from the response
            return response.json().get("short_url")
        else:
            # Print error message if request was not successful
            print("Error:", response.text)
            return None

    except Exception as e:
        print("An error occurred:", str(e))
        return None


def expand_url(short_url, jwt_token):
    """
    Decode a shortened URL using the Flask server.

    Args:
    - short_url (str): The shortened URL to be decoded.
    - jwt_token (str): The JWT token for authentication.

    Returns:
    - If decoding is successful and the original URL is obtained, returns a
      string representing the original URL.
    - If the decoding process fails, returns None.

    Raises:
    - Exception: If an unexpected error occurs during the decoding process.
    """
    try:
        # Send a POST request to the /api/decode endpoint
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = requests.post(
            f"{flask_url}/api/decode", json={"short_url": short_url}, headers=headers
        )

        # Check if the request was successful
        if response.status_code == 200:
            # Extract and return the original URL from the response
            return response.json().get("long_url")
        else:
            # Print error message if request was not successful
            print("Error:", response.text)
            return None
    except Exception as e:
        print("An error occurred:", str(e))
        return None


def reset_database(jwt_token):
    """
    Reset the MongoDB database by dropping it.

    Args:
    - jwt_token (str): The JWT token for authentication.

    Raises:
    - Exception: If an unexpected error occurs during the database reset process.
    """
    try:
        # Connect to MongoDB
        client = MongoClient(MONGODB_URI)

        # Drop the existing database
        client.drop_database("url_shortener")

        # Close the MongoDB connection
        client.close()

        # Log user out
        logout(jwt_token)
        print_separator(30)
        print("Database reset successful")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def admin_login():
    """
    Authenticate an admin user.

    Returns:
    - If admin authentication is successful, returns True.
    - If admin authentication fails, returns False.
    """
    username = input("Admin username: ")
    password = input("Admin password: ")
    return username.lower() == "admin" and password == "Password"


def print_separator(num):
    """
    Print a separator line with the specified number of dashes.
    """
    print("-" * num)


def interactive_login_or_signup():
    """
    Perform interactive login or signup.

    Returns:
    - If login or signup is successful and a JWT access token is generated,
      returns a string representing the access token.
    - If login or signup fails, returns None.

    Raises:
    - KeyboardInterrupt: If the user interrupts the interactive process.
    """
    while True:
        print_separator(30)
        print("|        URL Shortener!      |")
        print_separator(30)
        print("1. Login")
        print("2. Signup")
        print_separator(30)
        choice = input("Choose an option or [q]uit: ")
        print_separator(30)

        if choice == "1":
            print("Login:")
            username = input("Username: ")

            if username.lower() == "q":
                sys.exit(0)
            password = input("Password: ")

            if password.lower() == "q":
                sys.exit(0)
            jwt_token = login(username, password)

            if jwt_token:
                return jwt_token
            else:
                print("Login failed. Please try again.")

        elif choice == "2":
            print("Signup:")
            username = input("Enter username: ")

            if username.lower() == "q":
                sys.exit(0)
            password = input("Enter password: ")

            if password.lower() == "q":
                sys.exit(0)
            print_separator(30)

            jwt_token = signup(username, password)

            if jwt_token:
                return jwt_token

        elif choice.lower() == "q":
            print("|          Goodbye!          |")
            print_separator(30)
            sys.exit(0)

        else:
            print("Invalid choice. Please choose 1, 2, or [q]uit.")


def interactive_menu(jwt_token):
    """
    Perform interactive operations after login.

    Args:
    - jwt_token (str): The JWT token for authentication.

    Raises:
    - KeyboardInterrupt: If the user interrupts the interactive process.
    """
    while True:
        print_separator(30)
        print("Menu:")
        print("-----")
        print("1. Shorten a URL")
        print("2. Expand a URL")
        print("3. Logout")
        print("4. Admin: Reset Database")
        print_separator(30)
        operation = input("Choose an option: ")
        print_separator(30)

        if operation == "1":
            long_url = input("Enter URL: ")
            short_url = shorten_url(long_url, jwt_token)

            if short_url:
                print_separator(30)
                print("Shortened URL:", short_url)

        elif operation == "2":
            short_url_to_expand = input("Enter shortened URL: ")
            original_url = expand_url(short_url_to_expand, jwt_token)

            if original_url:
                print_separator(30)
                print("Original URL:", original_url)

        elif operation == "3":
            if logout(jwt_token):
                print_separator(30)
                print("|          Goodbye!          |")
                print_separator(30)
                break

        elif operation == "4":
            if admin_login():
                reset_database(jwt_token)
                print_separator(30)
                print("|          Goodbye!          |")
                print_separator(30)
                break

            else:
                print_separator(30)
                print("Error: You are not an admin")

        else:
            print("Invalid choice. Please choose 1, 2, or 3.")


if __name__ == "__main__":
    try:
        # Interactive login or signup
        jwt_token = interactive_login_or_signup()

        if jwt_token:
            # Proceed to interactive menu after successful login/signup
            interactive_menu(jwt_token)
    except KeyboardInterrupt:
        print("Exiting. Goodbye!")
        sys.exit(0)
