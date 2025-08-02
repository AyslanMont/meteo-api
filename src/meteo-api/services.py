import requests
from os import getenv
from dotenv import load_dotenv
from datetime import datetime
from schemas.previsao import Previsao, PrevisaoItem
from schemas.historico import RegistroClima

load_dotenv()
API_KEY = getenv("OPENWEATHER_API_KEY")

HISTORICO = []

def obter_clima_atual(cidade: str) -> dict:
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": cidade,
        "appid": API_KEY,
        "lang": "pt_br",
        "units": "metric"
    }
    resposta = requests.get(url, params=params)
    resposta.raise_for_status()
    return resposta.json()

def obter_previsao(cidade: str) -> Previsao:
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": cidade,
        "appid": API_KEY,
        "lang": "pt_br",
        "units": "metric"
    }
    resposta = requests.get(url, params=params)
    resposta.raise_for_status()
    dados = resposta.json()

    cidade_nome = dados["city"]["name"]
    previsoes = []

    for item in dados["list"][:10]:
        previsoes.append(PrevisaoItem(
            data=item["dt_txt"],
            temperatura=item["main"]["temp"],
            umidade=item["main"]["humidity"],
            descricao=item["weather"][0]["description"]
        ))
    
    return Previsao(cidade=cidade_nome, previsoes=previsoes)

def analisar_risco(dados_clima: dict) -> str:
    temperatura = dados_clima["main"]["temp"]
    umidade = dados_clima["main"]["humidity"]
    vento = dados_clima["wind"]["speed"]
    chuva = dados_clima.get("rain", {}).get("1h", 0.0)
    
    if temperatura > 30 and umidade > 70:
        return "Alto risco de calor extremo"
    elif vento > 20:
        return "Risco de ventos fortes"
    elif chuva > 10:
        return "Risco de chuvas intensas"
    else:
        return "Condições climáticas normais"

def salvar_em_historico(dados: dict):
    registro = RegistroClima(
        data=datetime.now(),
        cidade=dados.get("cidade", "Desconhecida"),
        temperatura=dados["temperatura"],
        umidade=dados["umidade"],
        vento=dados["vento"],
        chuva=dados["chuva"]
    )
    HISTORICO.append(registro)

def obter_historico() -> list:
    return HISTORICO
