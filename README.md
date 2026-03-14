# 🛰️ Nexus: Cognitive Market Intelligence

Real-time market intelligence platform combining **streaming trade
data** with **AI-driven sentiment analysis**.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![DuckDB](https://img.shields.io/badge/DuckDB-Analytics_DB-FFF000?logo=duckdb&logoColor=black)
![dbt](https://img.shields.io/badge/dbt-Data_Build_Tool-FF694B?logo=dbt&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-NLP-EF4B28?logo=pytorch&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

------------------------------------------------------------------------

# 🚀 Overview

**Nexus** is a real-time market intelligence platform that harmonizes
**high-frequency trade streams** with **AI-driven financial news
sentiment analysis**.

The system ingests live market signals from **Finnhub APIs**, enriches
them using **FinBERT**, and transforms them through a **Medallion Data
Architecture** using **dbt + DuckDB**.

The result is a **lightweight analytics lakehouse** capable of powering
real-time dashboards and financial insight generation.

------------------------------------------------------------------------

# 🎥 Demo

![Dashboard Demo](docs/demo.gif)

Example dashboard showing:

-   real-time trade volume
-   aggregated market sentiment
-   volatility vs sentiment correlation

------------------------------------------------------------------------

# ✨ Key Features

### ⚡ Real-Time Trade Streaming

High-frequency trade ingestion via **Finnhub WebSocket API**.

### 🧠 AI Sentiment Analysis

Financial news processed using **FinBERT (ProsusAI)** transformer model.

### 🧱 Medallion Data Architecture

Structured pipeline using **Bronze → Silver → Gold** data layers managed
by **dbt**.

### ⚡ OLAP Query Performance

**DuckDB** enables sub-second analytics without external database
infrastructure.

### 🔒 Concurrency-Safe Analytics

Implements **database snapshotting (`shutil.copy2`)** to avoid file
locking during ingestion and dashboard reads.

------------------------------------------------------------------------

# 🛠️ Tech Stack

  Layer             Technology
  ----------------- ------------------------------------
  Language          Python 3.10+
  Streaming         Finnhub WebSocket API
  News Data         Finnhub REST API
  Database          DuckDB
  Transformations   dbt-core
  NLP               HuggingFace Transformers (FinBERT)
  ML Framework      PyTorch
  Visualization     Streamlit + Plotly
  Orchestration     Makefile

------------------------------------------------------------------------

# 📂 Project Structure

    market-pulse-de/

    ingest/
        streamer.py
        news.py
        sentiment.py

    transform/
        models/
        sources.yml
        schema.yml

    data/
        market.duckdb

    dashboard.py
    summary.py
    Makefile
    requirements.txt

------------------------------------------------------------------------

# ⚙️ Getting Started

## 1️⃣ Clone the Repository

``` bash
git clone https://github.com/linearsachin/market-pulse-de.git
cd market-pulse-de
```

## 2️⃣ Setup Environment

``` bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 3️⃣ Configure API Key

Create `.env` file:

    FINNHUB_API_KEY=your_api_key_here

## 4️⃣ Run the Data Pipeline

    make run_all

## 5️⃣ Launch Dashboard

    streamlit run dashboard.py

------------------------------------------------------------------------

# 📊 Data Quality & Lineage

The pipeline uses **dbt** to ensure data reliability.

### Freshness

Incremental models capture new trades and news without full table scans.

### Integrity

Schema tests validate:

-   sentiment score ranges
-   symbol mapping
-   null checks

### Observability

dbt automatically generates:

-   lineage graphs
-   model documentation
-   test reports

------------------------------------------------------------------------

# 🤝 Contributing

Pull requests and improvements are welcome.

1.  Fork the repo
2.  Create a branch
3.  Submit a PR

------------------------------------------------------------------------

# 📜 License

MIT License
