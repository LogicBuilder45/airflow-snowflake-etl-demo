
    .PHONY: init up down logs clean

    init:
		@echo "Initializing Airflow environment (creating logs dir)..."
		@mkdir -p airflow_logs

    up:
		docker compose up -d

    down:
		docker compose down

    logs:
		docker compose logs -f --tail=100

    clean:
		rm -rf airflow_logs
