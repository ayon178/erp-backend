from pydantic import BaseModel
from typing import List

class MealsModel(BaseModel):
    name:str
    rawItem: List[str]
    price: int