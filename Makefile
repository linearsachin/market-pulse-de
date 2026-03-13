.PHONY: setup ingest-trades ingest-news transform clean

setup:
	pip install -r requirements.txt
	mkdir -p data

ingest-trades:
	python ingest/streamer.py

ingest-news:
	python ingest/news.py

transform:
	cd transform && dbt run --profiles-dir .

clean:
	rm -rf data/*.duckdb