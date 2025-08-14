# tests/models.py
from pydantic.v1 import BaseModel

class UserData(BaseModel):
    email: str
    password: str
    name: str