# 🛰️ Nexus | Market Pulse Data Engineering Terminal

A real-time, end-to-end data engineering pipeline and intelligence terminal. This project demonstrates a **Modern Data Stack (MDS)** approach to financial analytics, combining high-frequency ingestion, dbt transformations, and a cognitive analytical dashboard.

![System Status](https://img.shields.io/badge/System_Status-Stable-00FFA3?style=for-the-badge)
![Database](https://img.shields.io/badge/Database-DuckDB-yellow?style=for-the-badge)
![Transformation](https://img.shields.io/badge/Transform-dbt_Core-orange?style=for-the-badge)
![UI](https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge)

## 🏗️ Architecture & Data Flow

The project follows a **Medallion Architecture** (Bronze → Silver → Gold) to ensure data integrity and performance:

1.  **Ingestion (Bronze):** Python-based streaming and news scrapers (`ingest/`) pulling raw JSON data from **Finnhub.io** into a local **DuckDB** lake.
2.  **Transformation (Silver/Gold):** A **dbt** project (`transform/`) handles automated SQL modeling.
    * **Staging:** Cleanses raw trades and news.
    * **Marts:** Produces `fct_volatility_sentiment`, calculating real-time risk-adjusted volatility and neural sentiment scores.
3.  **Visualization (Serving):** A **Streamlit** terminal (`dashboard.py`) provides a 2x2 cognitive analytical grid for pattern recognition.

## 📂 Project Structure

```text
market-pulse-de/
├── ingest/                # Python Ingestion Layer (News & Streamer)
├── transform/             # dbt Project (Transformation Layer)
│   ├── models/
│   │   ├── staging/       # SQL cleanup and casting
│   │   └── marts/         # Analytical Fact & Dimension tables
│   ├── dbt_project.yml    # dbt configuration
│   └── profiles.yml       # DuckDB connection profile
├── data/                  # DuckDB Storage (.duckdb files)
├── dashboard.py           # Streamlit Analytical UI
├── pipeline_manager.py    # Master Orchestration Script
├── Makefile               # CLI entry points for the terminal
├── config.yaml            # System configurations
└── requirements.txt       # Environment dependencies