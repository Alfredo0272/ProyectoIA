from pydantic import BaseModel, Field, EmailStr, model_validator
from typing import List, Literal, Optional
from datetime import datetime

from models.recipe import Recipe  # IMPORT CORRECTO


class User(BaseModel):
    email: EmailStr
    password: Optional[str] = Field(None, min_length=6)

    name: Optional[str] = None
    surname: Optional[str] = None
    age: Optional[int] = Field(None, ge=0)
    country: Optional[str] = None
    id: Optional[str] = None

    hashed_password: Optional[str] = None

    roles: List[Literal["user", "editor", "admin"]] = Field(
        default_factory=lambda: ["user"]
    )
    recipes: List[Recipe] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=datetime.utcnow)

    @model_validator(mode="after")
    def check_password_if_present(self):
        if self.password is not None and len(self.password) < 6:
            raise ValueError("Password debe tener al menos 6 caracteres")
        return self

    class Config:
        extra = "ignore"
        json_encoders = {
            datetime: lambda d: d.isoformat()
        }
        fields = {
            "password": {"exclude": True},      # nunca se devuelve al cliente
            "hashed_password": {"exclude": True}
        }
