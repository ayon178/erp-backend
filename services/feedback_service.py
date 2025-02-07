from datetime import datetime
from bson import ObjectId
from database.connection import feedback_collection, users_collection

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
        "comment": feedback_data.get("comment"),
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