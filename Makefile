include .env
export

start:
	docker compose up -d
	@sleep 5
	@echo Check App http://localhost:81
	@echo ADMIN USERNAME: $(DJANGO_SUPERUSER_USERNAME)\nADMIN PASS: root


stop:
	docker compose down -v

test:
	pytest -v

dev:
	docker compose -f docker-compose-dev.yml up -d
	@sleep 5
	python manage.py migrate
	python manage.py createsuperuser \
        --noinput \
        --username $(DJANGO_SUPERUSER_USERNAME) \
        --email $(DJANGO_SUPERUSER_EMAIL)
	python manage.py runserver
	@echo ADMIN USERNAME: $(DJANGO_SUPERUSER_USERNAME)\nADMIN PASS: root

stopDev:
	lsof -t -i tcp:8000 | xargs kill -9
	docker compose -f docker-compose-dev.yml down

migrate:
	cd app && python manage.py migrate

uploadData:
	cd app && python manage.py shell < main.py

run:
	cd app && python manage.py runserver

shell:
	cd app && python manage.py shell_plus --print-sql

