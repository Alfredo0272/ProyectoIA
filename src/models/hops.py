from pydantic import BaseModel, Field
from typing import Optional, Literal


class Amount(BaseModel):
    value: float = Field(..., ge=0.0, title="Cantidad numérica")
    unit: Literal["g", "kg", "oz", "lb"] = Field(..., title="Unidad de medida")


class HopFlavorProfile(BaseModel):
    citrus: Optional[float] = Field(None, ge=0.0, title="Notas cítricas")
    floral: Optional[float] = Field(None, ge=0.0, title="Notas florales")
    pine: Optional[float] = Field(None, ge=0.0, title="Notas a pino")
    earthy: Optional[float] = Field(None, ge=0.0, title="Notas terrosas")
    spicy: Optional[float] = Field(None, ge=0.0, title="Notas especiadas")
    herbal: Optional[float] = Field(None, ge=0.0, title="Notas herbales")
    fruity: Optional[float] = Field(None, ge=0.0, title="Notas afrutadas")


class Hop(BaseModel):
    name: str = Field(..., title="Nombre del lúpulo")
    amount: Amount
    add: Optional[Literal["mash", "boil", "whirlpool", "dryhop"]] = Field(
        "boil", title="Momento de adición"
    )
    manufacturer: Optional[str] = Field(None, title="Fabricante")
    alpha_acid: Optional[float] = Field(None, ge=0, le=25, title="Alpha acids (%)")
    beta_acid: Optional[float] = Field(None, ge=0, le=25, title="Beta acids (%)")
    flavor_profile: Optional[HopFlavorProfile] = Field(
        None, title="Perfil aromático"
    )
    usage_percentage: Optional[float] = Field(
        None, ge=0, le=100, title="Porcentaje de uso"
    )
    use: Optional[str] = Field("brewing", title="Uso habitual")
    time: Optional[float] = Field(
        None, ge=0, title="Tiempo de hervido (minutos)"
    )
    notes: Optional[str] = Field(
        None, title="Notas adicionales del cervecero"
    )
    origin: Optional[str] = Field(None, title="Origen del lúpulo")
    substitutes: Optional[list[str]] = Field(None, title="Lúpulos sustitutos")
    humulene: Optional[float] = Field(None, ge=0.0, le=100.0, title="Humulene (%)")

