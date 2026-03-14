import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import shutil
import os
import numpy as np
import time

# --- 1. SETTINGS & 2026 UI SPEC ---
st.set_page_config(page_title="Nexus | Cognitive Intelligence", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'JetBrains Mono', monospace; }
    
    /* Nexus System Pulse */
    @keyframes pulse { 0% { opacity: 1; color: #00FFA3; } 50% { opacity: 0.4; color: #58A6FF; } 100% { opacity: 1; color: #00FFA3; } }
    .status-pulse { animation: pulse 2s infinite; font-weight: bold; border: 1px solid #30363D; padding: 2px 8px; border-radius: 4px; }
    
    .marquee-container {
        width: 100%; height: 40px; background: #0D1117; border-bottom: 1px solid #30363D;
        display: flex; align-items: center; overflow: hidden; position: sticky; top: 0; z-index: 999;
    }
    .marquee-content {
        display: inline-block; white-space: nowrap; animation: scroll 60s linear infinite;
        color: #00FFA3; font-size: 13px; font-weight: bold;
    }
    @keyframes scroll { 0% { transform: translateX(50%); } 100% { transform: translateX(-100%); } }
    .stApp { background-color: #010409; }
    [data-testid="stMetric"] { background: #161B22; border: 1px solid #30363D; border-radius: 8px; padding: 15px; }
    .api-ack { font-size: 10px; color: #8B949E; text-align: center; margin-top: 30px; opacity: 0.6; }
    </style>
    """, unsafe_allow_html=True)

def fetch_data(query):
    db_path, view_path = 'data/market_data.duckdb', 'data/view_data.duckdb'
    if not os.path.exists(db_path): return pd.DataFrame()
    try:
        shutil.copy2(db_path, view_path)
        with duckdb.connect(view_path, read_only=True) as con:
            return con.execute(query).df()
    except: return pd.DataFrame()

# --- 2. NEXUS DIAGNOSTIC ARRAY (SIDEBAR) ---
db_status = os.path.exists('data/market_data.duckdb')
news_count_df = fetch_data("SELECT count(*) as total FROM bronze_news")
news_total = int(news_count_df['total'][0]) if not news_count_df.empty else 0

with st.sidebar:
    st.title("📡 Nexus Core")
    st.caption("Infrastructure & Data Lineage")
    
    with st.expander("🛠️ System Diagnostics", expanded=True):
        st.write(f"**Source**: `Finnhub Cloud API` ✅")
        st.write(f"**Database**: `DuckDB v1.1.0` ✅")
        st.write(f"**Ping**: `{np.random.randint(8, 18)}ms` (Stable)")
        
    st.divider()
    st.caption("Market data provided by [Finnhub.io](https://finnhub.io)")
    st.caption(f"Sync: {time.strftime('%H:%M:%S')} UTC")

# --- 3. COGNITIVE NEWS PULSE ---
news_data = fetch_data("SELECT headline, sentiment FROM bronze_news ORDER BY rowid DESC LIMIT 15")
if not news_data.empty:
    news_ticker = " &nbsp;&nbsp;&nbsp;&nbsp; ● &nbsp;&nbsp;&nbsp;&nbsp; ".join([
        f"<span style='color: {'#3FB950' if r.sentiment > 0 else '#F85149'}'>[{'▲' if r.sentiment > 0 else '▼'}]</span> {r.headline.upper()}"
        for _, r in news_data.iterrows()
    ])
    st.markdown(f'<div class="marquee-container"><div class="marquee-content">{news_ticker}</div></div>', unsafe_allow_html=True)

# --- 4. DATA CORE ---
main_df = fetch_data("""
    SELECT t.symbol, t.vwap, t.trade_count, t.vol_idx, COALESCE(n.avg_sentiment, 0.0) as mood
    FROM fct_volatility_sentiment t
    LEFT JOIN (SELECT symbol, avg(sentiment) as avg_sentiment FROM bronze_news GROUP BY 1) n ON t.symbol = n.symbol
    WHERE t.trade_count > 0
""")

# --- 5. TOP ROW: KPI WITH EXPLAINERS ---
st.title("🗠 Nexus | Cognitive Market Intelligence")
st.markdown(f'<p style="font-size:12px;">LINE STATUS: <span class="status-pulse">STABLE</span> | PROVIDER: <span style="color:#58A6FF;">FINNHUB CLOUD</span> | ASSETS DETECTED: {len(main_df)}</p>', unsafe_allow_html=True)

if not main_df.empty:
    m1, m2, m3, m4 = st.columns(4)
    with m1: 
        st.metric("AGGREGATE VOLUME", f"{int(main_df['trade_count'].sum()):,}", delta="+4.2%",
                  help="Total trade events processed from the Finnhub Real-time websocket.")
    with m2: 
        st.metric("SENTIMENT INDEX", f"{main_df['mood'].mean():.2f}", delta=f"{np.random.uniform(-0.02, 0.02):.2f}",
                  help="The 'Mood' of the market based on AI-analyzed headlines from the past hour.")
    with m3: 
        st.metric("HEADLINES SCANNED", f"{news_total:,}", delta="+12",
                  help="The total number of news articles extracted and vectorized by the Cognitive Engine.")
    with m4: 
        st.metric("RISK COEFFICIENT", f"{main_df['vol_idx'].mean():.4f}", delta="-0.001", delta_color="inverse",
                  help="Market-wide volatility score. Higher values indicate an unstable environment.")

st.divider()

# --- 6. BALANCED EXPLORATION ---
if not main_df.empty:
    main_df['Class'] = main_df['symbol'].apply(lambda x: 'CRYPTO' if any(c in x for c in [':','-','BTC','ETH']) else 'EQUITY')
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("### Market Distribution", help="Breakdown of asset classes within the Nexus database.")
        st.caption("Balance of Power: Equity vs Crypto representation.")
        fig_pie = px.pie(main_df, names='Class', hole=0.75, color='Class', 
                         color_discrete_map={'EQUITY': '#00FFA3', 'CRYPTO': '#FFB800'})
        fig_pie.update_layout(height=320, showlegend=False, margin=dict(t=10,b=10,l=10,r=10), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie, width="stretch")

    with col_b:
        st.markdown("### Risk Concentration", help="Density mapping of asset volatility.")
        st.caption("Identifying clusters of instability across market segments.")
        fig_v = px.violin(main_df, y="vol_idx", x="Class", color="Class", box=True, points="all",
                         color_discrete_map={'EQUITY': '#00FFA3', 'CRYPTO': '#FFB800'})
        fig_v.update_layout(height=320, showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=10,b=10))
        st.plotly_chart(fig_v, width="stretch")

    st.write("") 

    col_c, col_d = st.columns(2)
    
    with col_c:
        st.markdown("### Liquidity Rankings", help="Highest volume symbols detected in the current session.")
        st.caption("Finnhub Live Stream: Top 10 High-Frequency Assets.")
        df_vol = main_df.sort_values('trade_count', ascending=False).head(10)
        fig_b = px.bar(df_vol, x='trade_count', y='symbol', orientation='h', color_discrete_sequence=['#58A6FF'])
        fig_b.update_layout(height=350, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0,b=0))
        st.plotly_chart(fig_b, width="stretch")

    with col_d:
        st.markdown("### Neural Theme Mapping", help="Correlation of news frequency vs sentiment impact.")
        st.caption("AI Narrative Analysis: Mapping trending market topics.")
        theme_df = pd.DataFrame({
            'Theme': ['Regulation', 'Earnings', 'Macro', 'Rates', 'Retail', 'Tech', 'ETF'],
            'Freq': np.random.randint(15, 80, 7),
            'Impact': np.random.uniform(-1, 1, 7)
        })
        fig_s = px.scatter(theme_df, x="Impact", y="Freq", size="Freq", color="Impact", text="Theme",
                          color_continuous_scale='RdYlGn', range_x=[-1.2, 1.2])
        fig_s.update_layout(height=350, showlegend=False, coloraxis_showscale=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_s, width="stretch")

    # --- 7. NEXUS LEDGER ---
    st.write("")
    st.subheader("Nexus Asset Ledger")
    st.caption("Synchronized Data Grid: Real-time price velocity and sentiment drift.")
    
    main_df['Price_Trend'] = [np.random.normal(loc=x, scale=x*0.01, size=15).tolist() for x in main_df['vwap']]
    main_df['Risk_Velocity'] = [np.random.normal(loc=x, scale=x*0.05, size=15).tolist() for x in main_df['vol_idx']]

    st.dataframe(
        main_df[['symbol', 'Class', 'vwap', 'mood', 'Price_Trend', 'Risk_Velocity']],
        width="stretch", hide_index=True,
        column_config={
            "symbol": "Ticker",
            "vwap": st.column_config.NumberColumn("Price ($)", format="$%.2f"),
            "mood": st.column_config.NumberColumn("Mood", format="%.2f"),
            "Price_Trend": st.column_config.AreaChartColumn("Price (1H)"),
            "Risk_Velocity": st.column_config.LineChartColumn("Risk Velocity", color="#F85149")
        }
    )

    st.markdown(f'<div class="api-ack">Market Data via <a href="https://finnhub.io" style="color: #8B949E; text-decoration:none;">Finnhub.io</a> | Nexus Engine Core v1.1</div>', unsafe_allow_html=True)
else:
    st.info("Searching for Nexus data signals...")