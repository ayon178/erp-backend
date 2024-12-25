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
    # Check if the user already exists
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
        "role": user_data["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # Token expires in 24 hours
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    # Return the access token and user role
    return {
        "access_token": access_token,
        "role": user_data["role"]
    }