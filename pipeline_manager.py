import subprocess
import time
import os
from ingest.utils import logger

def run_task(cmd, desc, cwd=None):
    logger.info(f"🔄 Starting: {desc}")
    subprocess.run(cmd, shell=True, check=True, cwd=cwd)

def run_pipeline(cycles=5):
    for i in range(cycles):
        logger.info(f"🚀 --- STARTING CYCLE {i+1} ---")
        
        # 1. Fetch News (Batch)
        run_task("python3 ingest/news.py", "News Ingestion")

        # 2. Stream Trades (Run for 2 minutes then stop)
        logger.info("📡 Streaming trades for 120 seconds...")
        streamer = subprocess.Popen(["python3", "ingest/streamer.py"])
        time.sleep(120) 
        streamer.terminate() # Releases the DuckDB lock
        logger.info("🛑 Streamer stopped for transformation.")

        # 3. dbt Transformation
        run_task("dbt run --profiles-dir .", "dbt Transformation", cwd="transform")

        # 4. Show Analysis
        run_task("python3 summary.py", "Generating Summary")
        
        logger.info(f"✅ Cycle {i+1} complete. Sleeping 30s...")
        time.sleep(30)

if __name__ == "__main__":
    run_pipeline()