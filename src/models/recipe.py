from typing import List
from pydantic import BaseModel, Field, model_validator

from models.boil import BoilAddition
from models.fermentation import FermentationProfile
from models.malt import Malt
from models.mash import MashStep
from models.water import WaterProfile
from models.yeast import Yeast


class Recipe(BaseModel):
    name: str = Field(..., title="Nombre de la receta")
    style: str = Field(..., title="Estilo cervecero")
    batch_size_l: float = Field(..., gt=0, title="Tamaño del lote (litros)")

    malts: List[Malt] = Field(..., description="Lista de maltas usadas")
    hops: List[BoilAddition] = Field(..., description="Adiciones de lúpulo en hervido")
    yeast: Yeast = Field(..., description="Levadura usada")
    water: WaterProfile = Field(..., description="Perfil de agua")
    mash: List[MashStep] = Field(..., description="Etapas de maceración")
    fermentation: FermentationProfile = Field(..., description="Perfil de fermentación")

    @model_validator(mode="after")
    def validate_recipe(self):
        if len(self.malts) == 0:
            raise ValueError("Una receta debe tener al menos una malta.")

        if len(self.hops) == 0:
            raise ValueError("Una receta debe tener al menos una adición de lúpulo.")

        if len(self.mash) == 0:
            raise ValueError("La receta debe tener al menos un paso de macerado.")

        return self
