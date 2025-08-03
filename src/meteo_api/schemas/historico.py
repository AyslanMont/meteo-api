from pydantic import BaseModel
from datetime import datetime


class RegistroClima(BaseModel):
    data: datetime
    cidade: str
    temperatura: float
    umidade: float
    vento: float
    chuva: float
