# 🌦️ Pipeline ETL de Dados Climáticos

Um pipeline de extração, transformação e carregamento (ETL) de dados meteorológicos em tempo real da API [OpenWeatherMap](https://openweathermap.org/). O projeto coleta dados de múltiplas localizações, valida a qualidade dos dados e armazena em formato Parquet particionado por data e cidade.

## 📋 Visão Geral

Este projeto implementa um **pipeline robusto e escalável** para monitorar dados climáticos de cidades brasileiras. Os dados são:
- **Coletados** em lote via API OpenWeatherMap
- **Transformados** com validação de schema usando Pandera
- **Carregados** em Parquet particionado para análise e consultas eficientes

### 🔄 Pipeline ETL

```
[OpenWeatherMap API] 
         ↓
    [EXTRACT]  → Coleta dados brutos em JSON
         ↓
    [TRANSFORM] → Valida schema, normaliza e estrutura dados
         ↓
    [LOAD]     → Salva em Parquet particionado (date/city_id)
```

## 🚀 Funcionalidades

- ✅ **Coleta em Lote:** Consulta múltiplas coordenadas (latitude/longitude) de forma automatizada
- ✅ **Validação de Dados:** Schema validation com Pandera para garantir qualidade
- ✅ **Armazenamento Otimizado:** Dados salvos em Parquet com particionamento por data e city_id
- ✅ **Logging Detalhado:** Rastreamento completo do pipeline com timestamps
- ✅ **Segurança:** API Key protegida via variáveis de ambiente (.env)
- ✅ **Normalização:** Extrai dados aninhados do JSON da API em estrutura plana

## 📊 Estrutura de Dados

O pipeline coleta e estrutura os seguintes campos:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `city_id` | int | ID único da cidade |
| `city_name` | str | Nome da cidade |
| `country` | str | País |
| `latitude` | float | Coordenada latitude |
| `longitude` | float | Coordenada longitude |
| `temperature` | float | Temperatura (°C) |
| `feels_like` | float | Sensação térmica (°C) |
| `temp_min` / `temp_max` | float | Min/máx de temperatura |
| `humidity` | int | Umidade (%) |
| `pressure` | int | Pressão atmosférica |
| `wind_speed` | float | Velocidade do vento (m/s) |
| `wind_deg` | int | Direção do vento (graus) |
| `weather_main` | str | Condição geral (Clear, Clouds, Rain, etc) |
| `weather_description` | str | Descrição detalhada |
| `sunrise` / `sunset` | datetime | Horários de nascer/pôr do sol |
| `datetime` | datetime | Data/hora da coleta (TZ: America/Sao_Paulo) |

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Propósito |
|-----------|--------|----------|
| **Python** | ≥3.13 | Linguagem principal |
| [Pandas](https://pandas.pydata.org/) | ≥3.0.1 | Manipulação e análise de dados |
| [Requests](https://pypi.org/project/requests/) | ≥2.32.5 | requisições HTTP para API |
| [Pandera](https://pandera.readthedocs.io/) | ≥0.29.0 | Validação de schema |
| [PyArrow](https://arrow.apache.org/) | ≥23.0.1 | Formato Parquet |
| [Python-DotEnv](https://pypi.org/project/python-dotenv/) | ≥0.9.9 | Variáveis de ambiente |

## 📦 Pré-requisitos

1. **Python 3.13+** instalado
2. **Conta gratuita** em [OpenWeatherMap](https://home.openweathermap.org/users/sign_up)
3. **API Key** (gerada em "My API keys" no dashboard)

## 🔧 Instalação e Configuração

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/git_weather.git
cd git_weather
```

### 2. Crie um ambiente virtual (recomendado)
```bash
python -m venv venv

# No Windows
venv\Scripts\activate

# No Linux/macOS
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
# ou
pip install pandas requests python-dotenv pandera pyarrow
```

Alternativamente, com uv (se usando pyproject.toml):
```bash
pip install -e .
```

### 4. Configure a API Key
Crie um arquivo `.env` na raiz do projeto:
```env
api_key=sua_chave_da_openweathermap_aqui
```

**⚠️ Importante:** Adicione `.env` ao `.gitignore` para não versionar credenciais!

## 💻 Como Usar

### Executar o Pipeline Completo

```bash
python main.py
```

Este comando executa:
1. **Extract:** Coleta dados climáticos das 9 cidades configuradas
2. **Transform:** Valida e transforma os dados
3. **Load:** Salva em `data/currated/today=YYYY-MM-DD/city_id=XXX/`

### Monitorar a Execução

O pipeline gera logs detalhados:
```
2026-02-23 14:30:15,123 - INFO - Pipeline iniciado as 23/02/2026-1430
2026-02-23 14:30:15,456 - INFO - 1º - Iniciando a coleta dos dados
2026-02-23 14:30:16,789 - INFO - Dados Coletados das seguintes coordenadas - Lat:-12.97 | Lon:-38.51
...
2026-02-23 14:30:25,123 - INFO - Pipeline finalizado as 23/02/2026-1430
```

### Customizar Coordenadas

Edite `main.py` para adicionar/remover cidades:

```python
lats = [-12.97, -19.81, -8.05, ...]  # Latitudes
longs = [-38.51, -43.95, -34.88, ...]  # Longitudes
```

## 📁 Estrutura do Projeto

```
git_weather/
├── main.py                  # Pipeline principal
├── teste.py                 # Testes
├── pyproject.toml           # Dependências e metadados
├── .env                     # Variáveis de ambiente (não versionado)
├── .gitignore               # Arquivos ignorados pelo Git
│
├── src/
│   ├── extract_data.py      # Módulo de coleta (API OpenWeatherMap)
│   ├── transform_data.py    # Módulo de transformação (Pandera schema)
│   └── load_data.py         # Módulo de carregamento (Parquet particionado)
│
└── data/
    ├── raw/                 # Dados brutos em JSON (entrada)
    │   └── 23022026.json    # Exemplo: dados do dia 23/02/2026
    │
    └── currated/            # Dados processados em Parquet (saída particionada)
        └── today=2026-02-23/
            ├── city_id=3390760/  # São Gonçalo
            ├── city_id=3445334/  # Rio de Janeiro
            └── ... (outras cidades)
```

## 🔍 Descrição dos Módulos

### `src/extract_data.py`
- Função `requisitar()`: Realiza requisição HTTP à API OpenWeatherMap
- Função `coletar_dados()`: Itera sobre coordenadas e salva JSON bruto
- Tratamento de erros e logging de requisições

### `src/transform_data.py`
- `SchemaWeather`: Define schema Pandera com validações de tipo, valores nulos e ranges
- Normaliza dados JSON aninhados para estrutura plana
- Converte timestamps para timezone America/Sao_Paulo
- Renomeia colunas para nomes amigáveis

### `src/load_data.py`
- Converte DataFrame para PyArrow Table
- Particiona dados por `today` (data da coleta) e `city_id`
- Salva em formato Parquet otimizado

## 📝 Licença

Este projeto é de código aberto. Sinta-se livre para usar e modificar.

## 👥 Autor

Desenvolvido por [Alan Mota](https://www.linkedin.com/in/motalan/)

## 📧 Contato & Suporte

Para dúvidas ou problemas, abra uma issue no repositório.
