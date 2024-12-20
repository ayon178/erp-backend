from pydantic import BaseModel
from typing import Optional

class FeedbackModel(BaseModel):
    comment: Optional[str] = None
    rating: int
    userId: str
    mealId: str