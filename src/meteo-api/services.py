import requests
from os import getenv
from dotenv import load_dotenv

load_dotenv()
API_KEY = getenv("OPENWEATHER_API_KEY")

def obter_clima_atual(lat: float, lon: float) -> dict:
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "lang": "pt_br",
        "units": "metric"
    }
    resposta = requests.get(url, params=params)
    resposta.raise_for_status()
    dados = resposta.json()
    return dados

def analisar_risco(dados_clima: dict) -> str:
    temperatura = dados_clima["main"]["temp"]
    umidade = dados_clima["main"]["humidity"]
    vento = dados_clima["wind"]["speed"]
    chuva = dados_clima.get("rain", {}).get("1h", 0.0)

    if temperatura > 30 and umidade < 50:
        return "Risco de calor extremo"
    elif vento > 20:
        return "Risco de ventos fortes"
    elif chuva > 10:
        return "Risco de chuvas intensas"
    else:
        return "Condições climáticas normais"
    

