# 🛰️ Nexus | Cognitive Market Intelligence

**Nexus** is a high-fidelity, real-time financial intelligence terminal designed to synthesize raw market data into actionable cognitive insights. Optimized for 2026 standards, it merges live price action from **Finnhub.io** with neural sentiment analysis via **Gemini-3-Flash**.

![System Status](https://img.shields.io/badge/System_Status-Stable-00FFA3?style=for-the-badge)
![Engine](https://img.shields.io/badge/Neural_Engine-v3.4-58A6FF?style=for-the-badge)
![Database](https://img.shields.io/badge/Database-DuckDB-yellow?style=for-the-badge)

## 🚀 Core Features

* **Neural Sentiment Mapping:** Real-time AI scoring of news headlines on a -1.0 (Panic) to +1.0 (Euphoria) index.
* **Dynamic KPI Tracking:** Live deltas for Volume, Mood, and Risk Analysis with detailed hover-explainers.
* **Symmetric Visual Exploration:** A balanced analytical grid featuring:
    * **Risk Density:** Violin plots identifying volatility clusters across asset classes.
    * **Neural Narrative Mapping:** Scatter plots correlating news frequency with sentiment impact.
    * **Liquidity Leaders:** High-frequency trade ranking.
* **Infrastructure Health Monitor:** Sidebar diagnostic array tracking DB latency, stream saturation, and model status.
* **2026 Compliance:** Fully upgraded to modern UI standards, utilizing `width="stretch"` for adaptive rendering.

## 🏗️ Technical Stack

| Component | Technology |
| :--- | :--- |
| **Interface** | Streamlit (Nexus Quantum Layout) |
| **Data Engine** | DuckDB (High-performance OLAP) |
| **Intelligence** | Gemini-3-Flash |
| **Data Provider** | Finnhub.io API |
| **Visuals** | Plotly Express |

## 🛠️ Installation & Setup

### 1. Structure the Data Lake
Ensure your directory includes the `data/` folder where your scraper outputs the DuckDB file:
```text
nexus-terminal/
├── app.py                 # Core UI Script
└── data/
    └── market_data.duckdb # Active Database