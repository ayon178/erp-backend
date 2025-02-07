from pydantic import BaseModel
from typing import Optional

class UserModel(BaseModel):
    member_serial_number: int 
    name: str                 
    designation: str          
    department: str            
    email: str                 
    phone1: str                
    phone2: Optional[str] = None  
    address: str               
    password: str             
    category: Optional[str] = None 