from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal


class MashStep(BaseModel):
    type: Literal[
        "acid_rest",
        "protein_rest",
        "beta_amylase",
        "alpha_amylase",
        "mash_out",
        "custom"
    ] = Field(..., title="Tipo de paso del macerado")

    temperature: float = Field(
        ..., ge=30, le=80, title="Temperatura (°C)",
        description="Temperatura objetivo de la etapa"
    )

    duration: float = Field(
        ..., ge=1, le=120, title="Duración (minutos)"
    )

    water_to_grain_ratio: Optional[float] = Field(
        None, ge=1.5, le=5.0,
        title="Relación agua/grano (L/kg)"
    )

    notes: Optional[str] = Field(
        None, title="Notas del cervecero"
    )

    @model_validator(mode="after")
    def validate_temp_ranges(self):
        if self.type == "beta_amylase" and not (60 <= self.temperature <= 67):
            raise ValueError("Beta amylase rest debe estar entre 60–67 °C.")
        if self.type == "alpha_amylase" and not (67 <= self.temperature <= 72):
            raise ValueError("Alpha amylase rest debe estar entre 67–72 °C.")
        if self.type == "protein_rest" and not (45 <= self.temperature <= 55):
            raise ValueError("Protein rest debe estar entre 45–55 °C.")
        if self.type == "mash_out" and self.temperature < 72:
            raise ValueError("Mash-out debe estar ≥ 72 °C.")
        return self
