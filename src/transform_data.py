import pandas as pd
from pathlib import Path
import logging
import pandera as pa
from pandera.typing import Series

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SchemaWeather(pa.DataFrameModel):
    base: str
    visibility: int
    datetime: Series[pd.DatetimeTZDtype] = pa.Field(dtype_kwargs={'tz':'America/Sao_Paulo'})
    timezone: int
    city_id: int
    city_name: str
    code: int
    longitude: float
    latitude: float
    temperature: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    sea_level: int
    grnd_level: int
    wind_speed: float
    wind_deg: int
    wind_gust: float = pa.Field(nullable=True)
    clouds: int
    country: str
    sunrise: Series[pd.DatetimeTZDtype] = pa.Field(dtype_kwargs={'tz':'America/Sao_Paulo'})
    sunset: Series[pd.DatetimeTZDtype] = pa.Field(dtype_kwargs={'tz':'America/Sao_Paulo'})
    weather_id: int
    weather_main: str
    weather_description: str
    id_row: str

columns_drop = ['weather', 'weather_icon']
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
    'main.grnd_level': 'grnd_level',
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
columns_round = ['latitude','longitude']

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

    logging.info(f'Coluna weather normalizada - DataFrame com {len(df.columns)} colunas')

    return df

# Dropando colunas que não serão necessarias
def drop_columns(df: pd.DataFrame, columns_name: list[str]) -> pd.DataFrame:
    logging.info(f'Removend colunas: {columns_name}')
    df = df.drop(columns=columns_name)
    logging.info(f'Colunas removidas - {len(df.columns)} colunas restantes')

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
        df[name] = pd.to_datetime(df[name],unit='ns', utc=True).dt.tz_convert('America/Sao_Paulo')

    logging.info('Colunas convertidas para datetime')

    return df

# Adicionando um identificador p/ cada linha usando city_id e datetime
def idempotence(df: pd.DataFrame) -> pd.DataFrame:
    
    logging.info(f'Iniciando o processo de criacao de IDs para {len(df)} linhas')
    df['id_row'] = df['city_id'].astype(str) + '_' + df['datetime'].dt.strftime('%d%m%Y%H')

    logging.info('Inclusao de IDs para linhas concluidas')

    return df

# Método para arredondar as colunas do tipo float para 2 casas decimais
def round_float(df: pd.DataFrame, arredondar: list[str]) -> pd.DataFrame:

    logging.info(f'Iniciando o processo de arredondamento das colunas do tipo float')

    for i in arredondar:
        df[i] = df[i].round(2)

    logging.info(f'Processo concluido! {len(arredondar)} colunas alteradas')
    
    return df

# Executando todas as transformações criadas acima
def data_transformation(path_name: str) -> pd.DataFrame:
    print('Iniciando transformações...')
    df = create_dataframe(path_name)
    df = normalize_weather_columns(df)
    df = drop_columns(df, columns_drop)
    df = rename_columns(df, columns_rename)
    df = normalize_datetime_columns(df, normalize_datetime)
    df = round_float(df, columns_round)
    df = idempotence(df)
    df = SchemaWeather.validate(df)
    logging.info('Transformações concluidas.')
    return df