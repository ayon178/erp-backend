from pydantic import BaseModel
from typing import Optional

class RawItemModel(BaseModel):
    title: str
    details: Optional[str] = None
    price: int
    quantity: int
    addedBy: str