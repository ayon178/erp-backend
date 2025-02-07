from datetime import datetime
from bson import ObjectId
from database.connection import feedback_collection, users_collection
from typing import Optional, Dict
from pymongo import ASCENDING, DESCENDING

# def create_feedback(feedback_data: dict) -> dict:
#     """
#     Create a new feedback document in the database.

#     :param feedback_data: The feedback data containing comment, rating, userId, and mealId.
#     :return: A dictionary containing the inserted feedback details.
#     """
#     # Validate mealId exists in the meals_collection
#     meal_id = feedback_data.get("mealId")
#     if not ObjectId.is_valid(meal_id):
#         raise ValueError("Invalid mealId. Must be a valid ObjectId.")

#     meal = meals_collection.find_one({"_id": ObjectId(meal_id)})
#     if not meal:
#         raise ValueError("Meal with the given mealId does not exist.")

#     # Add createdAt timestamp to feedback_data
#     feedback_data["createdAt"] = datetime.now().isoformat()

#     # Insert feedback into the feedback_collection
#     response = feedback_collection.insert_one(feedback_data)

#     # Return the inserted feedback details
#     return {
    #     "_id": str(response.inserted_id),
    #     "comment": feedback_data.get("comment"),
    #     "rating": feedback_data["rating"],
    #     "userId": feedback_data["userId"],
    #     "mealId": feedback_data["mealId"],
    #     "createdAt": feedback_data["createdAt"]
    # }


def create_feedback(feedback_data: dict) -> dict:
    """
    Create a new feedback document in the database after validating the user.
    :param feedback_data: The feedback data containing various fields as per FeedbackModel.
    :return: A dictionary containing the inserted feedback details.
    """
    # Validate userId exists and is valid
    user_id = feedback_data.get("userId")
    if not user_id:
        raise ValueError("userId is required.")
    if not ObjectId.is_valid(user_id):
        raise ValueError("Invalid userId. Must be a valid ObjectId.")

    # Check if the user exists in the database
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise ValueError("User with the given userId does not exist.")

    # Add createdAt timestamp to feedback_data
    feedback_data["createdAt"] = datetime.now().isoformat()

    # Insert feedback into the feedback_collection
    response = feedback_collection.insert_one(feedback_data)

    # Return the inserted feedback details
    return {
        "_id": str(response.inserted_id),
        "userId": feedback_data.get("userId"),
        "additionalFeedback": feedback_data.get("additionalFeedback"),
        "avoidBadQualityFeedback": feedback_data.get("avoidBadQualityFeedback"),
        "badFoodAdditionalComment": feedback_data.get("badFoodAdditionalComment"),
        "badFoodFrequency": feedback_data.get("badFoodFrequency"),
        "badQualityFrequency": feedback_data.get("badQualityFrequency"),
        "canteedFoodSatisfaction": feedback_data.get("canteedFoodSatisfaction"),
        "canteedFoodSatisfactionReview": feedback_data.get("canteedFoodSatisfactionReview"),
        "canteenService": feedback_data.get("canteenService"),
        "canteenServiceReview": feedback_data.get("canteenServiceReview"),
        "feedback": feedback_data.get("feedback"),
        "foodIssuesFaced": feedback_data.get("foodIssuesFaced"),
        "foodQualityComment": feedback_data.get("foodQualityComment"),
        "foodQualityImprovementFrequency": feedback_data.get("foodQualityImprovementFrequency"),
        "rating_cooking_quality": feedback_data.get("rating_cooking_quality"),
        "rating_dine_in_environment_hygiene": feedback_data.get("rating_dine_in_environment_hygiene"),
        "rating_food_taste": feedback_data.get("rating_food_taste"),
        "rating_meal_planning": feedback_data.get("rating_meal_planning"),
        "rating_service_quality": feedback_data.get("rating_service_quality"),
        "review": feedback_data.get("review"),
        "serviceRating": feedback_data.get("serviceRating"),
        "source": feedback_data.get("source"),
        "terms": feedback_data.get("terms"),
        "createdAt": feedback_data.get("createdAt")
    }


def fetch_feedback(
    search_term: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "createdAt",
    sort_order: str = "desc",
    filters: Optional[Dict[str, str]] = None
) -> dict:
    """
    Fetch feedback data with filtering, sorting, and pagination.
    :param search_term: Optional search term to filter by badFoodFrequency, foodIssuesFaced, or badQualityFrequency.
    :param page: Page number for pagination (default: 1).
    :param limit: Number of items per page (default: 10).
    :param sort_by: Field to sort by (default: createdAt).
    :param sort_order: Sort order ("asc" or "desc", default: desc).
    :param filters: Dictionary of filters for fields like createdAt, canteenService, ratings, etc.
                     Supports date range filtering using 'start_date' and 'end_date'.
    :return: A dictionary containing metadata and feedback data.
    """
    # Pagination calculations
    skip = (page - 1) * limit

    # Search conditions
    search_conditions = []
    if search_term:
        # Fields to search by
        SEARCH_FIELDS = ["badFoodFrequency", "foodIssuesFaced", "badQualityFrequency"]
        search_conditions.append({
            "$or": [
                {field: {"$regex": search_term, "$options": "i"}}
                for field in SEARCH_FIELDS
            ]
        })

    # Additional filters
    if filters:
        FILTER_FIELDS = [
            "createdAt",
            "canteenService",
            "canteedFoodSatisfaction",
            "rating_cooking_quality",
            "rating_dine_in_environment_hygiene",
            "rating_food_taste",
            "rating_meal_planning",
            "rating_service_quality",
            "serviceRating"
        ]

        # Handle date range filtering
        start_date = filters.get("start_date")
        end_date = filters.get("end_date")
        if start_date or end_date:
            try:
                date_range_condition = {}
                if start_date:
                    start_date_parsed = datetime.strptime(start_date, "%m/%d/%Y")
                    date_range_condition["$gte"] = start_date_parsed.isoformat()
                if end_date:
                    end_date_parsed = datetime.strptime(end_date, "%m/%d/%Y").replace(hour=23, minute=59, second=59)
                    date_range_condition["$lte"] = end_date_parsed.isoformat()
                search_conditions.append({"createdAt": date_range_condition})
            except ValueError:
                raise ValueError("Invalid date format. Use mm/dd/yyyy.")

        # Handle other filters
        for field in FILTER_FIELDS:
            if field in filters:
                if field == "createdAt":
                    continue  # Skip createdAt since it's handled separately for date range
                try:
                    value = float(filters[field])  # Convert to float for numeric comparisons
                    search_conditions.append({field: value})
                except ValueError:
                    raise ValueError(f"Invalid value for {field}. Must be numeric.")

    # Combine all conditions
    where_condition = {"$and": search_conditions} if search_conditions else {}

    # Sorting condition
    order = ASCENDING if sort_order == "asc" else DESCENDING
    sort_condition = [(sort_by, order)]

    # Querying the database
    feedback_cursor = feedback_collection.find(where_condition).sort(sort_condition).skip(skip).limit(limit)
    feedback_list = list(feedback_cursor)

    # Convert ObjectId to string
    for item in feedback_list:
        item["_id"] = str(item["_id"])

    # Total count for pagination
    total = feedback_collection.count_documents(where_condition)

    return {
        "meta": {
            "page": page,
            "limit": limit,
            "total": total,
        },
        "data": feedback_list
    }