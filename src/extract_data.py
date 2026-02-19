import requests
from pathlib import Path
from dotenv import load_dotenv
import os
import logging
import pandas as pd
from datetime import datetime
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def requisitar(latitude, longitude) -> dict: #Metodo que faz a requisicao na API da OpenWeather e retorna um json com a resposta 
    load_dotenv()
    url = 'https://api.openweathermap.org/data/2.5/weather'
    api_key = os.getenv('api_key') 
    parametros = {
            'lat': latitude,
            'lon': longitude,
            'appid': api_key,
            'units': 'metric'
        }

    resposta = requests.get(url, params = parametros)
    
    if resposta.status_code != 200:
        logging.error('Erro de requisição')
        return []
    else:
        logging.info(f'Dados Coletados das seguintes coordenadas - Lat:{latitude} | Lon:{longitude}')

    return resposta.json()


def coletar_dados(latitudes: list[float],longitudes: list[float]) -> None: # Modulo para coletar os dados de uma lista de latitudes e longitudes
    hora_coleta = datetime.now()
    coordenadas = list(zip(latitudes, longitudes))
    weather_data = []

    # Looping para realizar a coleta da lista
    for lat, long in coordenadas:
        dado = requisitar(lat,long)
        weather_data.append(dado)

    logging.info(f'Total de dados coletados: {len(weather_data)} registros')
    
    # Normalizando o dataset
    weather_data = pd.json_normalize(weather_data)
    
    arquivo = Path(f'data/raw/{hora_coleta.strftime('%d%m%Y')}.json')
    pasta = Path(arquivo).parent
    pasta.mkdir(parents=True, exist_ok=True)
    weather_data.to_json(arquivo, indent=4)

    logging.info(f'Arquivo salvo em {pasta}')