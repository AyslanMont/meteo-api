from pydantic import BaseModel
from typing import List


class PrevisaoItem(BaseModel):
    data: str
    temperatura: float
    umidade: float
    descricao: str


class Previsao(BaseModel):
    cidade: str
    previsoes: List[PrevisaoItem]
