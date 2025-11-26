from pydantic import BaseModel, Field, model_validator
from typing import Optional


class WaterProfile(BaseModel):
    name: Optional[str] = Field(
        None,
        title="Nombre del perfil de agua",
        description="Ejemplo: 'Pilsen', 'Burton', 'RO Water'"
    )

    calcium: Optional[float] = Field(
        None,
        ge=0,
        le=300,
        title="Calcio (ppm)",
        description=(
            "El calcio estabiliza enzimas del macerado, "
            "ayuda a reducir el pH, mejora la claridad y la floculación de la levadura. "
            "Valores típicos: 30–150 ppm."
        )
    )

    magnesium: Optional[float] = Field(
        None,
        ge=0,
        le=150,
        title="Magnesio (ppm)",
        description=(
            "Nutriente para la levadura en cantidades moderadas (5–30 ppm). "
            "A niveles altos (>50 ppm) puede aportar amargor áspero."
        )
    )

    sodium: Optional[float] = Field(
        None,
        ge=0,
        le=150,
        title="Sodio (ppm)",
        description=(
            "El sodio realza dulzor y cuerpo en bajas cantidades (<60 ppm). "
            "En concentraciones altas puede dar sabores salados o metálicos."
        )
    )

    chloride: Optional[float] = Field(
        None,
        ge=0,
        le=300,
        title="Cloruros (ppm)",
        description=(
            "Los cloruros aportan cuerpo, dulzor y suavidad al perfil de la cerveza. "
            "Altos niveles favorecen cervezas maltosas como NEIPAs o stouts."
        )
    )

    sulfate: Optional[float] = Field(
        None,
        ge=0,
        le=500,
        title="Sulfatos (ppm)",
        description=(
            "Los sulfatos intensifican la percepción de amargor y sequedad. "
            "Claves en IPAs y cervezas lupuladas. "
            "Altos niveles (>300 ppm) acentúan el carácter seco y amargo."
        )
    )

    bicarbonate: Optional[float] = Field(
        None,
        ge=0,
        le=400,
        title="Bicarbonatos (ppm)",
        description=(
            "Controlan la alcalinidad del agua y elevan el pH del macerado. "
            "Necesarios para cervezas oscuras con maltas ácidas. "
            "Niveles muy altos pueden causar astringencia."
        )
    )

    ph: Optional[float] = Field(
        None,
        ge=4.0,
        le=10.0,
        title="pH del agua",
        description=(
            "El pH natural del agua. Para macerado, el objetivo es 5.2–5.6 "
            "(ajustado mediante sales o ácido)."
        )
    )

    residual_alkalinity: Optional[float] = Field(
        None,
        title="Alcalinidad residual (RA)",
        description=(
            "Estimación del poder del agua para resistir cambios de pH. "
            "Aguas con RA alta favorecen cervezas oscuras; RA baja favorece cervezas claras."
        )
    )

    city: Optional[str] = Field(
        None, title="Ciudad asociada al perfil", description="Ej: Pilsen, Dublin, Burton-on-Trent"
    )

    notes: Optional[str] = Field(
        None, title="Notas adicionales", description="Cualquier comentario del cervecero."
    )

    @property
    def chloride_sulfate_ratio(self) -> Optional[float]:
        if self.chloride and self.sulfate and self.sulfate > 0:
            return self.chloride / self.sulfate
        return None

    @model_validator(mode="after")
    def validate_ions(self):
        if all(
            getattr(self, ion) is None
            for ion in ["calcium", "magnesium", "sodium", "chloride", "sulfate", "bicarbonate"]
        ):
            raise ValueError("El perfil de agua no puede estar completamente vacío.")
        return self
