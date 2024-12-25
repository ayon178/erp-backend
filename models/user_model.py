from pydantic import BaseModel
from typing import Optional

class UserModel(BaseModel):
    name: str
    address: str
    phone: str
    role: str
    password: str
    email: str
    department: str 
    category: Optional[str] = None