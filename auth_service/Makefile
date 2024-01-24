create-superuser:
	python -m src.main create-superuser $(SUPERUSER_LOGIN) $(SUPERUSER_PASSWORD) $(SUPERUSER_FIRST_NAME) $(SUPERUSER_LAST_NAME) $(SUPERUSER_EMAIL)

migrate:
	alembic upgrade head
