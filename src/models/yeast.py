from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal, List


class TemperatureRange(BaseModel):
    min: float = Field(..., ge=0, title="Temperatura mínima de fermentación (°C)")
    max: float = Field(..., ge=0, title="Temperatura máxima de fermentación (°C)")

    @model_validator(mode="after")
    def check_temperature_range(self):
        if self.min > self.max:
            raise ValueError("La temperatura mínima no puede ser mayor que la máxima.")
        return self


class Yeast(BaseModel):
    name: str = Field(..., title="Nombre comercial de la levadura")
    laboratory: Optional[str] = Field(None, title="Laboratorio (Fermentis, Lallemand...)")

    type: Literal[
        "ale",
        "lager",
        "kveik",
        "wild",
        "brettanomyces",
        "mixed-culture"
    ] = Field(..., title="Tipo de levadura")
    form: Literal["dry", "liquid"] = Field(
        "dry", title="Forma de presentación"
    )
    attenuation: Optional[float] = Field(
        None, ge=50, le=95, title="Atenuación (%)"
    )
    flocculation: Optional[Literal["low", "medium", "high"]] = Field(
        None, title="Floculación"
    )
    alcohol_tolerance: Optional[float] = Field(
        None, ge=0, le=20, title="Tolerancia alcohólica (%)"
    )
    temperature_range: Optional[TemperatureRange] = Field(
        None, title="Rango de temperatura de fermentación (°C)"
    )
    flavor_profile: Optional[List[str]] = Field(
        None,
        title="Aromas o características aportadas",
        description="Ej: 'afrutado', 'especiado', 'limpio', 'fenólico'"
    )
    recommended_styles: Optional[List[str]] = Field(
        None, title="Estilos recomendados"
    )

    origin: Optional[str] = Field(None, title="Origen de la cepa")
    notes: Optional[str] = Field(None, title="Notas adicionales del cervecero")
    min_pitching_rate: Optional[float] = Field(
        None, ge=0, title="Tasa mínima de inoculación (millones de células/mL/°P)"
    )
    max_pitching_rate: Optional[float] = Field(
        None, ge=0, title="Tasa máxima de inoculación (millones de células/mL/°P)"
    )

    @model_validator(mode="after")
    def check_pitching_rates(self):
        if (
            self.min_pitching_rate is not None
            and self.max_pitching_rate is not None
            and self.min_pitching_rate > self.max_pitching_rate
        ):
            raise ValueError("La tasa mínima de inoculación no puede ser mayor que la máxima.")
        return self
