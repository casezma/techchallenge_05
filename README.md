# 📊 Previsão de Fechamento da Ação PETR4 com Prophet + API

Este projeto prevê o fechamento da ação **PETR4.SA (Petrobras)** utilizando **modelos de séries temporais com Prophet**, expondo os resultados por meio de uma **API REST com FastAPI**.

---

## 📁 Estrutura do Projeto

```
├── app.py                 # API FastAPI para servir previsões
├── treina_modelo.py       # Script de captura de dados, treino e serialização do modelo
├── modelo.pkl             # Modelo Prophet serializado com pickle
├── date.YYYY-MM-DD        # Arquivo que armazena a última data dos dados
├── dados.csv              # Dados históricos (Date, Close)
├── requirements.txt       # Dependências do projeto
├── Dockerfile             # Dockerfile único para build
└── docker-compose.yml     # Orquestração dos serviços: treino + API
```

---

## 🚀 Como Executar

### ✅ 1. Com Docker Compose (recomendado)

```bash
docker compose up --build
```

> Esse comando:
> - Executa `treina_modelo.py` no serviço `treino`
> - Treina o modelo Prophet e salva como `modelo.pkl`
> - Em seguida inicia o serviço `api` na porta **80**, servindo sua API FastAPI

Acesse em:
```
http://localhost/docs
```

---

## 🔁 Re-treinar o modelo

```bash
docker compose run treino
```

---

## 🔌 API FastAPI

### Endpoint:
```http
POST /predict
```

### Request JSON:
```json
{
  "days": 7
}
```

### Response:
```json
{
  "resultado": [
    {
      "ds": "2025-07-14",
      "yhat": 38.12
    },
    ...
  ]
}
```

---

## ⚙️ Como funciona

- O modelo é treinado usando dados entre `2025-01-01` e `2025-06-30`.
- A última data real conhecida é salva em um arquivo `date.2025-06-30`.
- Quando a API recebe um `days = X`, ela calcula quantos dias de previsão precisa para alcançar a data futura desejada e retorna os `yhat` do Prophet.

---

## 📈 Avaliação do Modelo

Modelo avaliado nos últimos 120 dias com as métricas abaixo:

| Métrica | Valor |
|--------:|------:|
| **MSE**  | 12.98 |
| **MAE**  | 3.41  |
| **MAPE** | 10.3% |

> 🔎 Um MAPE de ~10% é considerado **muito bom** para séries temporais financeiras.

---

## 📦 `requirements.txt`

```txt
fastapi
uvicorn
pandas
prophet
yfinance
scikit-learn
loguru
```

---

## 🐳 `docker-compose.yml`

```yaml
version: "3.9"

services:
  treino:
    build:
      context: .
    container_name: prophet-treino
    command: python treina_modelo.py
    volumes:
      - .:/app
    restart: "no"

  api:
    build:
      context: .
    container_name: prophet-api
    command: uvicorn app:app --host 0.0.0.0 --port 8000
    ports:
      - "80:8000"
    volumes:
      - .:/app
    depends_on:
      - treino
    restart: unless-stopped
```

---

## 🐳 `Dockerfile`

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
```

---
