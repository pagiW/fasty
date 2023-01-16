from pydantic import BaseModel, Field
from typing import Optional

class Game(BaseModel):
    id: Optional[int] = Field(ge=1)
    name: str
    console: str
    realized: int = Field(le=2023)
    class Config:
        schema_extra = {
            'example': {
                'id': 1,
                'name': 'Crash Bandicoot 3',
                'console': 'Play Station',
                'realized': 1998
            }
        }
class ChangedGame(BaseModel):
    name: Optional[str]
    console: Optional[str]
    realized: Optional[int] = Field(le=2023)
    class Config:
        schema_extra = {
            'example': {
                'name': 'Crash Bandicoot 3',
                'console': 'Play Station',
                'realized': 1998
            }
        }

class User(BaseModel):
    email: str
    password: str
    class Config:
        schema_extra = {
            'example': {
                'email': 'Juan@gmail.com',
                'password': 'A xd'
            }
        }