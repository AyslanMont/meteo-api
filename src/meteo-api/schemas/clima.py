from pydantic import BaseModel

class Clima(BaseModel):
    temperatura: float
    umidade: float
    vento: float
    chuva: float