# 🌦️ Coletor de Dados Climáticos (OpenWeatherMap)

Este projeto é um script em Python desenvolvido para coletar dados meteorológicos atuais de múltiplas localidades. Ele consome a API da [OpenWeatherMap](https://openweathermap.org/), estrutura os dados e os salva diariamente em arquivos CSV organizados.

## 🚀 Funcionalidades

* **Consulta em Lote:** Permite definir listas de latitudes e longitudes para consulta sequencial.
* **Estruturação de Dados:** Converte a resposta JSON da API em um formato tabular limpo (Pandas DataFrame).
* **Armazenamento Automático:** Salva os dados em arquivos `.csv` nomeados com a data atual (ex: `20.11.2025.csv`).
* **Gestão de Diretórios:** Cria automaticamente a pasta `data/` se ela não existir.
* **Segurança:** Utiliza variáveis de ambiente para proteger a chave da API (API Key).

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* [Pandas](https://pandas.pydata.org/) (Manipulação de dados)
* [Requests](https://pypi.org/project/requests/) (Requisições HTTP)
* [Python-Dotenv](https://pypi.org/project/python-dotenv/) (Variáveis de ambiente)
* [Pathlib](https://docs.python.org/3/library/pathlib.html) (Manipulação de caminhos de arquivos)

## 📦 Pré-requisitos

Antes de começar, você precisará ter o Python instalado em sua máquina e uma chave de API da OpenWeatherMap.

1. Crie uma conta gratuita em [OpenWeatherMap](https://home.openweathermap.org/users/sign_up).
2. Gere uma API Key na seção "My API keys".

## 🔧 Instalação e Configuração

1. **Clone o repositório:**
   ```Bash
   git clone [https://github.com/seu-usuario/nome-do-projeto.git](https://github.com/seu-usuario/nome-do-projeto.git)
   cd nome-do-projeto

2. **Crie um ambiente virtual(opcional, mas recomendado):**
   ```Bash
   python -m venv venv
    # No Windows
    venv\Scripts\activate
    # No Linux/Mac
    source venv/bin/activate

3. **Instale as dependências:**
   ```Bash
    pip install pandas reuqests python-dotenv

4. **Configuração da API Key:**
   Crie um arquivo chamado `.env` na raiz do projeto e adicione sua chave:
   ```env
   api_key=SUA_CHAVE_DA_OPENWEATHER_AQUI

## ▶️ Como usar

1. Abra o arquivo do script (ex: `main.py`).
2. No bloco `if__name__ == '__main__':`, você pode editar as listas `latitude` e `longitude` com as coordenadas das cidades que deseja monitorar.
3. Execute o script:
   ```Bash
       python main.py

**Saída Esperada**
O script criará uma pasta `data/` e salvará um arquivo CSV com a data de hoje.

