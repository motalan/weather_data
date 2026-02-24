import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def salvar_dados(df: pd.DataFrame):
    
    logging.info(f'Iniciando processo de salvamento e particionamento de {len(df)} dados')
    diretorio = Path('data/currated/')

    # Criando a coluna do dia da execução para partição
    data_hoje = datetime.now().strftime('%Y-%m-%d')
    df['today'] = data_hoje

    # Convertendo o DataFrame p/ tabela do pyarrow
    arrow = pa.Table.from_pandas(df)

    # Salvando os dados particionados
    pq.write_to_dataset(arrow,root_path=diretorio,partition_cols=['today','city_id'])

    logging.info(f'Dados salvos com sucesso nas partições do dia {data_hoje}')