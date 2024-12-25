from fastapi import APIRouter, HTTPException
from models.user_model import UserModel
from services.user_service import create_user
from utils.response import create_response

user_route = APIRouter()

@user_route.post("/new/user")
def new_user(doc: UserModel):
    """
    Route to create a new user.

    :param doc: UserModel instance containing the user details.
    :return: Standardized response with the created user's access token and role.
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
