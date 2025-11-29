from pydantic import BaseModel, Field
from typing import Optional, Literal


class Amount(BaseModel):
    value: float = Field(..., ge=0.0, title="Cantidad numérica", description="Cantidad total")
    unit: str = Field(..., title="Unidad de medida", description="Unidad (kg, g, lb, oz)")


class MaltFlavorProfile(BaseModel):
    biscuity: Optional[float] = Field(None, title="Sabor a galleta")
    caramel: Optional[float] = Field(None, title="Sabor a caramelo")
    chocolate: Optional[float] = Field(None, title="Sabor a chocolate")
    coffee: Optional[float] = Field(None, title="Sabor a café")
    nutty: Optional[float] = Field(None, title="Sabor a nuez")
    roasted: Optional[float] = Field(None, title="Sabor tostado")
    smoky: Optional[float] = Field(None, title="Sabor ahumado")
    sweet: Optional[float] = Field(None, title="Sabor dulce")


class Malt(BaseModel):
    name: str = Field(..., title="Nombre descriptivo de la malta")
    amount: Optional[Amount] = Field(None, title="Cantidad")
    add: Optional[Literal["mash", "boil"]] = Field(None, title="Etapa de adición")
    manufacturer: Optional[str] = Field(None, title="Fabricante")
    attribute: Optional[str] = Field(None, title="Atributo")
    extract_potential: Optional[float] = Field(
        None, ge=0.0, le=1.0, title="Potencial extracto"
    )
    deviation: Optional[float] = Field(
        None, ge=0.0, le=0.1, title="Desviación extracto"
    )
    minimum_diastatic_power: Optional[float] = Field(None, ge=0.0)
    maximum_diastatic_power: Optional[float] = Field(None, ge=0.0)
    minimum_color: Optional[float] = Field(None, ge=0.0)
    maximum_color: Optional[float] = Field(None, ge=0.0)
    flavor_profile: Optional[MaltFlavorProfile] = None
    sweetness: Optional[float] = None
    usage_percentage: Optional[float] = Field(None, ge=0.0, le=100.0)
    use: Optional[str] = None
