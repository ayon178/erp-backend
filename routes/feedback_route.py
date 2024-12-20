from fastapi import APIRouter, HTTPException
from models.feedback_model import FeedbackModel
from services.feedback_service import create_feedback
from utils.response import create_response

feedback_route = APIRouter()

@feedback_route.post("/new/feedback")
def new_feedback(doc: FeedbackModel):
    """
    Route to create a new feedback.

    :param doc: FeedbackModel instance containing the feedback details.
    :return: Standardized response with the created feedback details.
    """
    try:
        # Call the create_feedback service to insert the feedback
        response_data = create_feedback(doc.dict())
        return create_response(
            status="Ok",
            status_code=201,
            message="Feedback created successfully",
            data=response_data
        )
    except ValueError as e:
        # Handle validation errors gracefully
        raise HTTPException(status_code=400, detail=str(e))
