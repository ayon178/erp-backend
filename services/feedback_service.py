from datetime import datetime
from bson import ObjectId
from database.connection import feedback_collection, meals_collection

def create_feedback(feedback_data: dict) -> dict:
    """
    Create a new feedback document in the database.

    :param feedback_data: The feedback data containing comment, rating, userId, and mealId.
    :return: A dictionary containing the inserted feedback details.
    """
    # Validate mealId exists in the meals_collection
    meal_id = feedback_data.get("mealId")
    if not ObjectId.is_valid(meal_id):
        raise ValueError("Invalid mealId. Must be a valid ObjectId.")

    meal = meals_collection.find_one({"_id": ObjectId(meal_id)})
    if not meal:
        raise ValueError("Meal with the given mealId does not exist.")

    # Add createdAt timestamp to feedback_data
    feedback_data["createdAt"] = datetime.now().isoformat()

    # Insert feedback into the feedback_collection
    response = feedback_collection.insert_one(feedback_data)

    # Return the inserted feedback details
    return {
        "_id": str(response.inserted_id),
        "comment": feedback_data.get("comment"),
        "rating": feedback_data["rating"],
        "userId": feedback_data["userId"],
        "mealId": feedback_data["mealId"],
        "createdAt": feedback_data["createdAt"]
    }
