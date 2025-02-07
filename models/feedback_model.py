from pydantic import BaseModel
from typing import Optional, Union, List

class FeedbackModel(BaseModel):
    userId: Optional[str] = None
    additionalFeedback: Optional[str] = None
    avoidBadQualityFeedback: Optional[str] = None
    badFoodAdditionalComment: Optional[str] = None
    badFoodFrequency: Optional[str] = None
    badQualityFrequency: Optional[List[str]] = None  # List of strings (e.g., ['Breakfast', 'Lunch'])
    canteedFoodSatisfaction: Optional[Union[int, float]] = None  # Allows both int and float
    canteedFoodSatisfactionReview: Optional[str] = None
    canteenService: Optional[Union[int, float]] = None  # Allows both int and float
    canteenServiceReview: Optional[str] = None
    feedback: Optional[str] = None
    foodIssuesFaced: Optional[List[str]] = None  # List of strings (e.g., ['Bad Taste', 'Bad Meal Planning'])
    foodQualityComment: Optional[str] = None
    foodQualityImprovementFrequency: Optional[str] = None
    rating_cooking_quality: Optional[int] = None
    rating_dine_in_environment_hygiene: Optional[int] = None
    rating_food_taste: Optional[int] = None
    rating_meal_planning: Optional[int] = None
    rating_service_quality: Optional[int] = None
    review: Optional[str] = None
    serviceRating: Optional[int] = None
    source: Optional[List[str]] = None  # List of strings (e.g., ['Fresh Food', 'Variety of Items'])
    terms: Optional[bool] = None  # Boolean value (e.g., False)
