{{ config(materialized='table') }}

WITH trade_metrics AS (
    SELECT 
        symbol,
        SUM(price * volume) / SUM(volume) as vwap,
        STDDEV(price) as price_stddev,
        COUNT(*) as trade_count,
        MAX(trade_at) as last_trade
    FROM {{ ref('stg_trades') }}
    GROUP BY 1
),

news_metrics AS (
    SELECT 
        symbol,
        AVG(sentiment) as avg_sentiment
    FROM {{ source('raw', 'bronze_news') }}
    GROUP BY 1
)

SELECT 
    t.*,
    -- Use COALESCE to show 0 instead of NULL for sentiment
    COALESCE(n.avg_sentiment, 0) as avg_sentiment,
    -- Volatility Index (handle division by zero just in case)
    CASE WHEN t.vwap > 0 THEN (t.price_stddev / t.vwap) * 100 ELSE 0 END as vol_idx
FROM trade_metrics t
LEFT JOIN news_metrics n ON t.symbol = n.symbol -- Change from INNER to LEFT JOIN