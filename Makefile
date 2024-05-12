admin-dev:
	docker-compose -f docker-compose.yaml exec django-admin make admin

super-admin-dev:
	docker compose -f docker-compose.yaml exec auth-api make create-superuser

run-dev:
	docker-compose -f docker-compose-dev.yaml up -d


run-prod:
	docker compose up -d

stop-dev:
	docker-compose -f docker-compose-dev.yaml down

stop-prod:
	docker-compose -f docker-compose.yaml up -d
