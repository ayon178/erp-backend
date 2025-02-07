from fastapi import APIRouter, HTTPException
from models.feedback_model import FeedbackModel
from services.feedback_service import create_feedback, fetch_feedback
from utils.response import create_response
from typing import Optional, Dict
from fastapi import Query

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

@feedback_route.get("/feedback")
def get_feedback(
    search_term: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    sort_by: Optional[str] = "createdAt",
    sort_order: Optional[str] = "desc",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    canteenService: Optional[str] = None,
    canteedFoodSatisfaction: Optional[str] = None,
    rating_cooking_quality: Optional[str] = None,
    rating_dine_in_environment_hygiene: Optional[str] = None,
    rating_food_taste: Optional[str] = None,
    rating_meal_planning: Optional[str] = None,
    rating_service_quality: Optional[str] = None,
    serviceRating: Optional[str] = None
):
    """
    Route to fetch feedback data with filtering, sorting, and pagination.
    :param search_term: Optional search term to filter by badFoodFrequency, foodIssuesFaced, or badQualityFrequency.
    :param page: Page number for pagination (default: 1).
    :param limit: Number of items per page (default: 10).
    :param sort_by: Field to sort by (default: createdAt).
    :param sort_order: Sort order ("asc" or "desc", default: desc).
    :param start_date: Start date for filtering feedback by createdAt (format: mm/dd/yyyy).
    :param end_date: End date for filtering feedback by createdAt (format: mm/dd/yyyy).
    :param canteenService: Filter feedback by canteenService rating.
    :param canteedFoodSatisfaction: Filter feedback by canteedFoodSatisfaction rating.
    :param rating_cooking_quality: Filter feedback by cooking quality rating.
    :param rating_dine_in_environment_hygiene: Filter feedback by dine-in environment hygiene rating.
    :param rating_food_taste: Filter feedback by food taste rating.
    :param rating_meal_planning: Filter feedback by meal planning rating.
    :param rating_service_quality: Filter feedback by service quality rating.
    :param serviceRating: Filter feedback by overall service rating.
    :return: Standardized response with feedback data.
    """
    # Prepare filters dictionary
    filters: Dict[str, str] = {}
    if start_date:
        filters["start_date"] = start_date
    if end_date:
        filters["end_date"] = end_date
    if canteenService:
        filters["canteenService"] = canteenService
    if canteedFoodSatisfaction:
        filters["canteedFoodSatisfaction"] = canteedFoodSatisfaction
    if rating_cooking_quality:
        filters["rating_cooking_quality"] = rating_cooking_quality
    if rating_dine_in_environment_hygiene:
        filters["rating_dine_in_environment_hygiene"] = rating_dine_in_environment_hygiene
    if rating_food_taste:
        filters["rating_food_taste"] = rating_food_taste
    if rating_meal_planning:
        filters["rating_meal_planning"] = rating_meal_planning
    if rating_service_quality:
        filters["rating_service_quality"] = rating_service_quality
    if serviceRating:
        filters["serviceRating"] = serviceRating

    # Fetch feedback using the service function
    response_data = fetch_feedback(
        search_term=search_term,
        page=page,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
        filters=filters
    )

    # Return the standardized response
    return create_response(
        status="Ok",
        status_code=200,
        message="Feedback fetched successfully",
        data=response_data
    )