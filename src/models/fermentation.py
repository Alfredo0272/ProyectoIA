from pydantic import BaseModel, Field
from typing import Optional, List


class FermentationStep(BaseModel):
    name: str = Field(..., title="Nombre del paso", description="Ej: fermentación primaria")
    temperature: float = Field(..., ge=0, le=35, title="Temperatura (°C)")
    duration: float = Field(..., ge=1, le=60, title="Duración (días)")
    pressure: Optional[float] = Field(
        None, ge=0, le=2.0, title="Presión (bar)", description="Para fermentación presurizada"
    )
    notes: Optional[str] = Field(None)


class FermentationProfile(BaseModel):
    primary: FermentationStep
    secondary: Optional[FermentationStep] = None
    cold_crash_temperature: Optional[float] = Field(
        None, ge=-2, le=10, title="Temperatura de cold crash (°C)"
    )
    cold_crash_duration: Optional[float] = Field(
        None, ge=1, le=10, title="Duración del cold crash (días)"
    )
    dry_hopping: Optional[List[str]] = Field(
        None, description="Listado de lúpulos usados en dry hop"
    )
  