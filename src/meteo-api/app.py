from fastapi import FastAPI
from fastapi import HTTPException
from .schemas.clima import Clima
from os import getenv
import requests
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()
API_KEY = str(getenv("OPENWEATHER_API_KEY"))


@app.get("/clima", response_model=Clima)
def get_clima(lat: float, lon: float):
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "lang": "pt_br",
        "units": "metric"
    }

    resposta = requests.get(url=url, params=params)

    if resposta.status_code == 200:

        dados = resposta.json()

        temperatura = dados["main"]["temp"]
        umidade = dados["main"]["humidity"]
        vento = dados["wind"]["speed"]
        chuva = dados.get("rain", {}).get("1h", 0.0)

        clima = Clima(
            temperatura=temperatura,
            umidade=umidade,
            vento=vento,
            chuva=chuva
        )

        return clima
    else:
        raise HTTPException(
            status_code=resposta.status_code, detail=resposta.text)
