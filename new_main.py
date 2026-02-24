from src.extract_data import coletar_dados
from src.transform_data import data_transformation
from src.load_data import salvar_dados
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def pipeline():
    inicio = datetime.now().strftime('%d/%m/%Y-%H%M')

    logging.info(f'Pipeline iniciado as {inicio}')

    logging.info(f'1º - Iniciando a coleta dos dados')

    lats = [-12.97, -19.81, -8.05, -25.42, -22.9, -30.03, -27.59, -23.66, -23.54]
    longs = [-38.51, -43.95, -34.88, -49.27, -43.2, -51.23, -48.54, -46.46, -46.63]

    coletar_dados(latitudes=lats,longitudes=longs)

    logging.info('2º - Iniciado a transformação dos dados')
    data = data_transformation(f'data/raw/{datetime.now().strftime('%d%m%Y')}.json')

    logging.info('3º - Iniciando o carregameto na pasta currated')
    salvar_dados(data)
    
    fim = datetime.now().strftime('%d/%m/%Y-%H%M')
    logging.info(f'Pipeline finalizado as {fim}')

pipeline()