from pydantic import BaseModel
from typing import Optional, List

class FeedbackModel(BaseModel):
    userId: Optional[str] = None
    mealId: Optional[str] = None
    additionalFeedback: Optional[str] = None
    avoidBadQualityFeedback: Optional[str] = None
    badFoodAdditionalComment: Optional[str] = None
    badFoodFrequency: Optional[str] = None
    badQualityFrequency: Optional[List[str]] = None  # List of strings (e.g., ['Breakfast', 'Lunch'])
    canteedFoodSatisfaction: Optional[float] = None  # Float value (e.g., 0.5)
    canteedFoodSatisfactionReview: Optional[str] = None
    canteenService: Optional[float] = None  # Float value (e.g., 0.5)
    canteenServiceReview: Optional[str] = None
    comment: Optional[str] = None
    feedback: Optional[str] = None
    foodIssuesFaced: Optional[List[str]] = None  # List of strings (e.g., ['Bad Taste', 'Bad Meal Planning'])
    foodQualityComment: Optional[str] = None
    foodQualityImprovementFrequency: Optional[str] = None
    rating_cooking_quality: Optional[int] = None
    rating_dine_in_environment_hygiene: Optional[int] = None  # Renamed for clarity
    rating_food_taste: Optional[int] = None
    rating_meal_planning: Optional[int] = None
    rating_service_quality: Optional[int] = None
    review: Optional[str] = None
    serviceRating: Optional[int] = None
    source: Optional[List[str]] = None  # List of strings (e.g., ['Fresh Food', 'Variety of Items'])
    terms: Optional[bool] = None  # Boolean value (e.g., False)