from pydantic import BaseModel, EmailStr
from typing import List, Optional

class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone: str

class CustomerCreate(CustomerBase):
    pass  # Used for POST requests

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class CustomerOut(CustomerBase):
    id: int
    orders: List[str] = [] # Related data

    class Config:
        from_attributes = True