from fastapi import APIRouter, HTTPException
from models.user_model import UserModel
from services.user_service import create_user, login_user  # Import the login_user function
from utils.response import create_response

# Define the router
user_route = APIRouter()

@user_route.post("/new/user")
def new_user(doc: UserModel):
    """
    Route to create a new user.
    :param doc: UserModel instance containing the user details.
    :return: Standardized response with the created user's access token and designation.
    """
    try:
        # Call the create_user service to insert the user
        response_data = create_user(doc.dict())
        return create_response(
            status="Ok",
            status_code=201,
            message="User created successfully",
            data=response_data
        )
    except ValueError as e:
        # Handle validation errors gracefully
        raise HTTPException(status_code=400, detail=str(e))


@user_route.post("/login")
def login(credentials: dict):
    """
    Route to authenticate a user and generate an access token.
    :param credentials: A dictionary containing the user's email and password.
    :return: Standardized response with the access token and designation.
    """
    try:
        # Call the login_user service to authenticate the user
        response_data = login_user(credentials)
        return create_response(
            status="Ok",
            status_code=200,
            message="Login successful",
            data=response_data
        )
    except ValueError as e:
        # Handle invalid credentials or other errors gracefully
        raise HTTPException(status_code=401, detail=str(e))