from pydantic import BaseModel, Field
from typing import Optional, Literal
from .hops import Hop  # Importas tu modelo Hop real


class BoilAddition(BaseModel):
    hop: Hop = Field(..., title="Lúpulo añadido")

    time: float = Field(
        ..., ge=0, le=120, title="Tiempo restante de hervor (min)"
    )

    use: Literal["bittering", "flavor", "aroma", "whirlpool"] = Field(
        ..., title="Propósito de la adición"
    )

    form: Literal["pellet", "whole", "extract"] = Field(
        "pellet", title="Forma física del lúpulo"
    )

    ibu_contribution: Optional[float] = Field(
        None, ge=0, title="IBUs estimados de esta adición"
    )
