from fastapi import FastAPI, HTTPException
from .schemas.clima import Clima
from .schemas.previsao import Previsao
from .schemas.historico import RegistroClima
from os import getenv
from dotenv import load_dotenv
from .services import salvar_em_historico, obter_historico, obter_clima_atual, obter_previsao

app = FastAPI()

load_dotenv()
API_KEY = str(getenv("OPENWEATHER_API_KEY"))

@app.get("/clima", response_model=Clima)
def get_clima(cidade: str):
    try:
        dados = obter_clima_atual(cidade)

        temperatura = dados["main"]["temp"]
        umidade = dados["main"]["humidity"]
        vento = dados["wind"]["speed"]
        chuva = dados.get("rain", {}).get("1h", 0.0)
        cidade_nome = dados.get("name", "Desconhecida")

        salvar_em_historico({
            "cidade": cidade_nome,
            "temperatura": temperatura,
            "umidade": umidade,
            "vento": vento,
            "chuva": chuva
        })

        clima = Clima(
            temperatura=temperatura,
            umidade=umidade,
            vento=vento,
            chuva=chuva
        )
        return clima
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/previsao", response_model=Previsao)
def get_previsao(cidade: str):
    try:
        previsao = obter_previsao(cidade)
        return previsao
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/historico", response_model=list[RegistroClima])
def get_historico():
    return obter_historico()
