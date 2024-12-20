from fastapi import APIRouter, Query
from typing import Optional, Dict
from models.meals_model import MealsModel
from services.meals_service import create_meals, fetch_all_meals
from utils.response import create_response

meals_route = APIRouter()

@meals_route.post("/new/meals")
def new_meal(doc: MealsModel):
    response_data = create_meals(doc.dict())
    return create_response(
        status="Ok",
        status_code=201,
        message="Meal created successfully",
        data=response_data
    )

@meals_route.get("/meals")
def get_all_meals(
    search_term: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    sort_by: Optional[str] = "createdAt",
    sort_order: Optional[str] = "desc",
    rawItem: Optional[str] = None,
    created_at: Optional[str] = None
):
    """
    Route to fetch all meals with optional filters, search, and pagination.

    :param search_term: Text to search in meal names.
    :param page: Current page for pagination.
    :param limit: Number of items per page.
    :param sort_by: Field to sort by (default is "createdAt").
    :param sort_order: Sorting order ("asc" or "desc").
    :param rawItem: Filter by raw item ID.
    :param created_at: Filter by creation date in "mm/dd/yyyy" format.
    :return: A standardized response containing the meals list.
    """
    # Prepare filters dictionary
    filters: Dict[str, str] = {}
    if rawItem:
        filters["rawItem"] = rawItem
    if created_at:
        filters["createdAt"] = created_at

    # Fetch meals using the service function
    response_data = fetch_all_meals(search_term, page, limit, sort_by, sort_order, filters)

    # Return the standardized response
    return create_response(
        status="Ok",
        status_code=200,
        message="Meals fetched successfully",
        data=response_data
    )