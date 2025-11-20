
import requests
import pandas as pd
from datetime import date
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

class ColetorClima:
    def __init__(self) -> None: #Declaração das variaveis de latitude e longitude e chave da API da OpenWeather
        self.api_key = os.getenv('api_key')
        self.lat = [-12.97, -19.81, -8.05, -25.42, -22.9, -30.03, -27.59, -23.66, -23.54]
        self.lon = [-38.51, -43.95, -34.88, -49.27, -43.2, -51.23, -48.54, -46.46, -46.63]
        self.data_requisicao = date.today()

    def requisitar(self, latitude, longitude): 
        
        resposta = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={self.api_key}&units=metric')
        return resposta.json()
    
    def dados_dia(self) -> list:
        self.lista_dicionarios = []
        self.dia = f'{self.data_requisicao.day}.{self.data_requisicao.month}.{self.data_requisicao.year}'
        
        for coord in range(len(self.lat)):
            info = self.requisitar(self.lat[coord],self.lon[coord])
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
            self.lista_dicionarios.append(dados)
        return self.lista_dicionarios
        
    def salvar_dados(self) -> None:
        self.path = Path(f'data/{self.data_requisicao.day}.{self.data_requisicao.month}.{self.data_requisicao.year}.csv')
        self.destiny = self.path.parent
        self.destiny.mkdir(parents=True, exist_ok=True)
        self.df = pd.DataFrame(self.dados_dia())
        self.df.to_csv(self.path,index=False)

if __name__ == '__main__':
    bora = ColetorClima()
    bora.salvar_dados()