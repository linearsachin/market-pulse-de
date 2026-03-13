import duckdb
from ingest.utils import get_config
import os

def run_summary():
    # 1. Setup connection
    config = get_config()
    db_path = config.get('database_path', 'data/market_data.duckdb')
    con = duckdb.connect(db_path)

    print("\n" + "="*50)
    print("🚀 MARKET PULSE: FINAL DATA SUMMARY")
    print("="*50)

    # 2. Check row counts
    print("\n--- [ Table Statistics ] ---")
    counts = con.execute("""
        SELECT 
            (SELECT count(*) FROM bronze_trades) as trades,
            (SELECT count(*) FROM bronze_news) as news,
            (SELECT count(*) FROM fct_volatility_sentiment) as analytic_rows
    """).fetchone()
    print(f"Raw Trades: {counts[0]}")
    print(f"Raw News:   {counts[1]}")
    print(f"Joined Rows: {counts[2]}")

# 3. Sentiment & Volatility Highlights
    print("\n--- [ Sentiment & Volatility Analysis ] ---")
    analysis = con.execute("""
        SELECT 
            symbol, 
            round(avg_sentiment, 2) as sentiment_score,
            round(vol_idx, 4) as volatility,
            trade_count
        FROM fct_volatility_sentiment
        ORDER BY trade_count DESC  -- Show the most active stocks first
        LIMIT 10
    """).df()
    
    if analysis.empty:
        print("No joined data yet. Waiting for more trades/news...")
    else:
        print(analysis.to_string(index=False))

    # Add a "Market Mood" section
    print("\n--- [ Current Market Mood (General News) ] ---")
    mood = con.execute("SELECT round(avg(sentiment), 2) FROM bronze_news").fetchone()[0]
    print(f"Overall Sentiment Score: {mood if mood else 'No news yet'}")

    # 4. Use DuckDB's magic SUMMARIZE on the final table
    print("\n--- [ Data Distribution (SUMMARIZE) ] ---")
    summary = con.execute("SUMMARIZE fct_volatility_sentiment").df()
    # We'll just show the most interesting columns
    print(summary[['column_name', 'column_type', 'min', 'max', 'avg']])

    con.close()

if __name__ == "__main__":
    run_summary()