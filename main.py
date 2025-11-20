
import requests
import pandas as pd
from datetime import date
from pathlib import Path
from dotenv import load_dotenv
import os

class ColetorClima:
    def __init__(self, api_key: str, latitudes: list, longitudes: list) -> None: #Declaração das variaveis de latitude e longitude e chave da API da OpenWeather
        self.api_key = api_key
        self.coordenadas = list(zip(latitudes, longitudes))
        self.data_requisicao = date.today()
        self.base_url = 'https://api.openweathermap.org/data/2.5/weather'

    def requisitar(self, latitude, longitude) -> dict: #Metodo que faz a requisicao na API da OpenWeather e retorna um json com a resposta 
        
        parametros = {
                    'lat': latitude,
                    'lon': longitude,
                    'appid': self.api_key,
                    'units': 'metric'
        }

        resposta = requests.get(self.base_url, params = parametros)
        return resposta.json()
    
    def coletar_dados_dia(self) -> list[dict]:
        self.dados_coletados = []
        self.dia = self.data_requisicao.strftime('%d.%m.%Y')
        
        for lat, lon in self.coordenadas:
            info = self.requisitar(lat, lon)
            dados = {'Data': self.dia,
                    'Lon': info['coord']['lon'],
                    'Lat': info['coord']['lat'],
                    'Weather': info['weather'][0]['main'],
                    'Temp': info['main']['temp'],
                    'Feels_like': info['main']['feels_like'],
                    'Temp_min': info['main']['temp_min'],
                    'Temp_max': info['main']['temp_max'],
                    'Wind_speed': info['wind']['speed'],
                    'City': info['name'],
                    'Country': info['sys']['country'],
                    }
            self.dados_coletados.append(dados)
        return self.dados_coletados
        
    def salvar_dados(self) -> None:
        #Nome do arquivo que será salvo
        arquivo = (f'{self.data_requisicao.strftime("%d.%m.%Y")}.csv')
        #Pasta onde o arquivo será salvo
        pasta = Path('data') / arquivo
        #Cria a pasta data caso ela não exista
        pasta.parent.mkdir(parents=True, exist_ok=True)
        #Cria o DataFrame e salva como csv
        df = pd.DataFrame(self.coletar_dados_dia())
        df.to_csv(pasta,index=False)
        print(f'Dados salvos com sucesso em: {pasta}')

if __name__ == '__main__':
    load_dotenv()
    api_key = os.getenv('api_key')
    latitudes = [-12.97, -19.81, -8.05, -25.42, -22.9, -30.03, -27.59, -23.66, -23.54]
    longitudes = [-38.51, -43.95, -34.88, -49.27, -43.2, -51.23, -48.54, -46.46, -46.63]
    bora = ColetorClima(api_key=api_key,latitudes=latitudes,longitudes=longitudes)
    bora.salvar_dados()
