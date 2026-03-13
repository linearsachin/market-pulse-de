import finnhub
import os
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from utils import get_db, logger, get_config

# Setup
client = finnhub.Client(api_key=os.getenv('FINNHUB_API_KEY'))
analyzer = SentimentIntensityAnalyzer()
config = get_config()

def fetch_news():
    """
    Pulls from 4 categories but only pushes 3 columns (symbol, sentiment, ts)
    to match the existing 'bronze_news' schema.
    """
    categories = ['general', 'crypto', 'forex', 'merger']
    target_symbols = config.get('symbols', [])
    processed_news = []

    try:
        for cat in categories:
            logger.info(f"📡 Fetching {cat} news...")
            news = client.general_news(cat, min_id=0)
            
            for n in news:
                headline = n.get('headline', '')
                if not headline: continue
                
                # Match symbol from config or use category as fallback
                matched_symbol = 'MARKET'
                for s in target_symbols:
                    if s.lower() in headline.lower():
                        matched_symbol = s.upper()
                        break
                
                # Fallback for empty matches in specific feeds
                if matched_symbol == 'MARKET' and cat != 'general':
                    matched_symbol = cat.upper()

                # ONLY 3 COLUMNS: symbol, sentiment, ts
                processed_news.append({
                    'symbol': matched_symbol,
                    'sentiment': analyzer.polarity_scores(headline)['compound'],
                    'ts': n.get('datetime')
                })

        if not processed_news:
            logger.warning("No news found across categories.")
            return

        # Create DataFrame
        df = pd.DataFrame(processed_news)
        
        with get_db() as con:
            # Ensure table exists (3 columns)
            con.execute("CREATE TABLE IF NOT EXISTS bronze_news (symbol VARCHAR, sentiment FLOAT, ts BIGINT)")
            
            # Append the 3 columns
            con.append("bronze_news", df)
            
        logger.info(f"✅ Ingested {len(df)} items to Bronze (3-column schema)")

    except Exception as e:
        logger.error(f"❌ News Ingestion Error: {e}")

if __name__ == "__main__":
    fetch_news()