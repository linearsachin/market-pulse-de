import duckdb
import yaml
import os
import logging
from dotenv import load_dotenv

load_dotenv()

def get_config():
    # Use an absolute path or navigate up if running from inside ingest/
    # This assumes you run from the project root
    config_path = "config.yaml"
    if not os.path.exists(config_path):
        config_path = "../config.yaml"
        
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def get_db():
    config = get_config()
    
    # Use .get() to provide a fallback if the key is missing
    db_path = config.get('database_path', 'data/market_data.duckdb')
    
    # Ensure the directory exists
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
        
    return duckdb.connect(db_path)

# --- THIS IS THE MISSING PIECE ---
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("market-pulse")
# ---------------------------------