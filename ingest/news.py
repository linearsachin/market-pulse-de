import finnhub
import os
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from utils import get_db, logger, get_config

# --- NEURAL ENGINE SETUP ---
# We use ProsusAI/finbert - the industry standard for financial sentiment
MODEL_NAME = "ProsusAI/finbert"
logger.info(f"🧠 Loading Neural Engine: {MODEL_NAME}...")

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
# Initialize the pipeline
nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Finnhub Setup
client = finnhub.Client(api_key=os.getenv('FINNHUB_API_KEY'))
config = get_config()

def get_finbert_score(text):
    """
    Translates FinBERT's labels into a float between -1.0 and 1.0.
    Labels: 'positive', 'negative', 'neutral'
    """
    try:
        # FinBERT has a 512 token limit; we truncate just in case
        result = nlp(text[:512])[0]
        label = result['label']
        confidence = result['score']

        if label == 'positive':
            return confidence
        elif label == 'negative':
            return -confidence
        else:
            return 0.0  # Neutral
    except Exception as e:
        logger.error(f"Sentiment Error: {e}")
        return 0.0

def fetch_news():
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
                
                # Logic to match symbols
                matched_symbol = 'MARKET'
                for s in target_symbols:
                    if s.lower() in headline.lower():
                        matched_symbol = s.upper()
                        break
                
                if matched_symbol == 'MARKET' and cat != 'general':
                    matched_symbol = cat.upper()

                # Process with FinBERT instead of VADER
                sentiment_score = get_finbert_score(headline)

                processed_news.append({
                    'symbol': matched_symbol,
                    'sentiment': sentiment_score,
                    'ts': n.get('datetime')
                })

        if not processed_news:
            logger.warning("No news found across categories.")
            return

        df = pd.DataFrame(processed_news)
        
        with get_db() as con:
            con.execute("CREATE TABLE IF NOT EXISTS bronze_news (symbol VARCHAR, sentiment FLOAT, ts BIGINT)")
            con.append("bronze_news", df)
            
        logger.info(f"✅ Ingested {len(df)} items using FinBERT Neural Engine.")

    except Exception as e:
        logger.error(f"❌ News Ingestion Error: {e}")

if __name__ == "__main__":
    fetch_news()