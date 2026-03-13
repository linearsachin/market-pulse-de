{{ config(
    materialized='incremental',
    unique_key='trade_id' 
) }}

SELECT 
    -- Create a unique ID so we don't double-count trades
    md5(symbol || ts::VARCHAR || price::VARCHAR) as trade_id,
    symbol,
    price::DOUBLE as price,
    volume::DOUBLE as volume,
    to_timestamp(ts / 1000) as trade_at
FROM {{ source('raw', 'bronze_trades') }}

{% if is_incremental() %}
  -- Only pull trades newer than the latest one in our existing table
  WHERE to_timestamp(ts / 1000) > (SELECT MAX(trade_at) FROM {{ this }})
{% endif %}