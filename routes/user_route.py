from fastapi import APIRouter, HTTPException, Header
from models.user_model import UserModel
from services.user_service import create_user, login_user, get_logged_in_user  # Import the login_user function
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
    

@user_route.get("/user/me")
def get_logged_in_user_route(
    authorization: str = Header(None)  # Extract the Authorization header
):
    """
    Route to fetch the logged-in user's details using their JWT token.
    :param authorization: The Authorization header containing the JWT token (e.g., "Bearer <JWT_TOKEN>").
    :return: Standardized response with the user's details.
    """
    try:
        # Validate the Authorization header
        if not authorization or not authorization.startswith("Bearer "):
            raise ValueError("Invalid Authorization header. Expected format: 'Bearer <JWT_TOKEN>'.")
        
        # Extract the token from the header
        token = authorization.split(" ")[1]
        
        # Fetch the logged-in user's details using the service
        user_details = get_logged_in_user(token)
        
        # Return the standardized response
        return create_response(
            status="Ok",
            status_code=200,
            message="User details fetched successfully",
            data=user_details
        )
    
    except ValueError as e:
        # Handle validation errors gracefully
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")