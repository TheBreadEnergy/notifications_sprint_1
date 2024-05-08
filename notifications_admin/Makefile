# Export poetry dependencies to requirements.txt
requirements:
	poetry export --without-hashes -o requirements.txt

django-superuser:
	DJANGO_SUPERUSER_USERNAME=my_admin \
	DJANGO_SUPERUSER_PASSWORD=PpAaSs!123 \
	DJANGO_SUPERUSER_EMAIL=mail@mail.ru \
	python manage.py createsuperuser --noinput || true


.PHONY: \
	requirements \
	django-superuser
