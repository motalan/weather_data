import pandas as pd
import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

columns_drop = ['weather', 'weather_icon', 'sys.type']
columns_rename = {
    'dt': 'datetime',
    'id': 'city_id',
    'name': 'city_name',
    'cod': 'code',
    'coord.lon': 'longitude',
    'coord.lat': 'latitude',
    'main.temp': 'temperature',
    'main.feels_like': 'feels_like',
    'main.temp_min': 'temp_min',
    'main.temp_max': 'temp_max',
    'main.pressure': 'pressure',
    'main.humidity': 'humidity',
    'main.sea_level': 'sea_level',
    'main.grnd_level': 'sea_level',
    'wind.speed': 'wind_speed',
    'wind.deg': 'wind_deg',
    'wind.gust': 'wind_gust',
    'clouds.all': 'clouds',
    'sys.type': 'sys_type',
    'sys.id': 'sys_id',
    'sys.country': 'country',
    'sys.sunrise': 'sunrise',
    'sys.sunset': 'sunset'
}
normalize_datetime = ['datetime', 'sunrise', 'sunset']

# Criando o DataFrame
def create_dataframe(path_name: str) -> pd.DataFrame:
    path = Path(path_name)

    if not path.exists():
        raise FileNotFoundError(f'Arquivo não encontrado: {path}')
    
    data = pd.read_json(path)
    logging.info(f'DataFrame criado com {len(data)} linhas.')

    return data
    
# Normalizando a coluna weather
def normalize_weather_columns(df: pd.DataFrame) -> pd.DataFrame:
    df_weather = pd.json_normalize(df['weather'].apply(lambda x: x[0]))

    df_weather = df_weather.rename(columns={
        'id': 'weather_id',
        'main': 'weather_main',
        'description': 'weather_description',
        'icon': 'weather_icon'       
    })

    df = pd.concat([df,df_weather], axis=1)

    logging.info(f'Coluna weather normalizada - DataFrame com {len(df)} colunas')

    return df

# Dropando colunas que não serão necessarias
def drop_columns(df: pd.DataFrame, columns_name: list[str]) -> pd.DataFrame:
    logging.info(f'Removend colunas: {columns_name}')
    df = df.drop(columns=columns_name)
    logging.info(f'Colunas removidas - {len(df)} colunas restantes')

    return df

# Renomeando algumas colunas p/ padronização
def rename_columns(df: pd.DataFrame, columns_name: dict[str,str]) -> pd.DataFrame:
    logging.info(f'Renomeando {len(columns_name)} colunas...')
    df = df.rename(columns=columns_name)
    logging.info('Colunas renomeadas')
    
    return df

# Convertendo data e hora p/ o formato BR
def normalize_datetime_columns(df: pd.DataFrame, columns_name:list[str]) -> pd.DataFrame:
    logging.info(f'Convertendo colunas para datetime: {columns_name}')

    for name in columns_name:
        df[name] = pd.to_datetime(df[name],unit='s', utc=True).dt.tz_convert('America/Sao_Paulo')

    logging.info('Colunas convertidas para datetime')

    return df

# Executando todas as transformações criadas acima
def data_transformation(path_name: str) -> pd.DataFrame:
    print('Iniciando transformações...')
    df = create_dataframe(path_name)
    df = normalize_weather_columns(df)
    df = drop_columns(df, columns_drop)
    df = rename_columns(df, columns_rename)
    df = normalize_datetime_columns(df, normalize_datetime)
    logging.info('Transformações concluidas.')
    return df