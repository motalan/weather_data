from src.extract_data import coletar_dados
from src.transform_data import data_transformation
from src.load_data import salvar_dados
import logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def pipeline():
    start = datetime.now()
    inicio = start.strftime('%d/%m/%Y-%H:s%M')
    root = Path(__file__).parent.absolute()
    folder = Path(f'{root}/data/currated/today={start.strftime('%Y')}-{start.strftime('%m')}-{start.strftime('%d')}/')
    lats = [-12.97, -19.81, -8.05, -25.42, -22.9, -30.03, -27.59, -23.66, -23.54,-10.43,-7.69]
    longs = [-38.51, -43.95, -34.88, -49.27, -43.2, -51.23, -48.54, -46.46, -46.63,-39.33,-35.52]
    to_pop = []

    logging.info(f'Pipeline iniciado as {inicio}')

    if folder.is_dir():
        files = [f.name.split('=')[1].split('_') for f in folder.iterdir() if f.is_dir()]
        for n in range(0, len(lats)):
            if [str(lats[n]), str(longs[n])] in files:
                to_pop.append(n)
        
        for i in sorted(to_pop, reverse=True):
            del lats[i]
            del longs[i]

    if not lats:
        return logging.info('Nenhuma coordenada para coletar informacoes')
    logging.info(f'1º - Iniciando a coleta dos dados')

    coletar_dados(latitudes=lats,longitudes=longs)

    logging.info('2º - Iniciado a transformação dos dados')
    data = data_transformation(f'data/raw/{datetime.now().strftime('%d%m%Y')}.json')

    logging.info('3º - Iniciando o carregameto na pasta currated')
    salvar_dados(data)
    
    fim = datetime.now().strftime('%d/%m/%Y-%H:%M')
    logging.info(f'Pipeline finalizado as {fim}')

pipeline()