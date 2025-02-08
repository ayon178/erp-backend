import jwt
import datetime
from typing import Dict
from bson import ObjectId
from database.connection import users_collection
from passlib.hash import bcrypt
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Secret key for JWT
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in the environment variables.")

# Function to create a new user
def create_user(user_data: Dict) -> Dict:
    # Validate required fields
    required_fields = [
        "member_serial_number", 
        "name", 
        "designation", 
        "department", 
        "email", 
        "phone1", 
        "address", 
        "password"
    ]
    for field in required_fields:
        if field not in user_data or not user_data[field]:
            raise ValueError(f"Missing or empty required field: {field}")

    # Check if the user already exists by email
    if users_collection.find_one({"email": user_data["email"]}):
        raise ValueError("A user with this email already exists.")

    # Hash the password
    user_data["password"] = bcrypt.hash(user_data["password"])

    # Add createdAt timestamp
    user_data["createdAt"] = datetime.datetime.now().isoformat()

    # Insert the user into the database
    response = users_collection.insert_one(user_data)

    # Generate JWT access token
    payload = {
        "user_id": str(response.inserted_id),
        "email": user_data["email"],
        "designation": user_data["designation"],  # Use 'designation' instead of 'role'
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # Token expires in 24 hours
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    # Return the access token and designation
    return {
        "access_token": access_token,
        "designation": user_data["designation"]  # Return 'designation' instead of 'role'
    }


# Function to login a user
def login_user(credentials: Dict) -> Dict:
    """
    Authenticate a user based on member_serial_number, email, phone1, or phone2 and password.
    :param credentials: A dictionary containing one of the identifiers (member_serial_number, email, phone1, phone2) and password.
    :return: A dictionary containing the access token and designation.
    """
    # Extract password from credentials
    password = credentials.get("password")
    if not password:
        raise ValueError("Password is required.")

    # Check which identifier is provided
    identifier_fields = ["member_serial_number", "email", "phone1", "phone2"]
    identifier = None
    identifier_value = None

    for field in identifier_fields:
        if field in credentials and credentials[field]:
            identifier = field
            identifier_value = credentials[field]
            break

    if not identifier:
        raise ValueError("One of the following fields is required: member_serial_number, email, phone1, phone2.")

    # Query the database based on the provided identifier
    query = {identifier: identifier_value}
    user = users_collection.find_one(query)

    if not user:
        raise ValueError("Invalid credentials.")

    # Verify the password
    if not bcrypt.verify(password, user["password"]):
        raise ValueError("Invalid credentials.")

    # Generate JWT access token
    payload = {
        "user_id": str(user["_id"]),
        "email": user.get("email"),  # Include email if available
        "designation": user["designation"],  # Include designation in the token
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # Token expires in 24 hours
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    # Return the access token and designation
    return {
        "access_token": access_token,
        "designation": user["designation"]
    }

