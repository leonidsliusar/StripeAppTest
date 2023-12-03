include .env

run:
	docker compose up -d
	@echo Check App http://localhost/admin

stop:
	docker compose down -v

test:
	pytest -v

cov:
	pytest --cov=stripeapp --cov-report=html

runDev:
	docker compose -f dev/docker-compose.yml up -d
	@sleep 5
	python manage.py migrate
	python manage.py createsuperuser \
		--noinput \
		--username $(DJANGO_SUPERUSER_USERNAME) \
		--email $(DJANGO_SUPERUSER_EMAIL)
	python manage.py runserver

stopDev:
	lsof -t -i tcp:8000 | xargs kill -9
	docker compose -f dev/docker-compose.yml down -v


envfile = '.env'

env:
	touch $(envfile)
	echo 'DJANGO_SUPERUSER_USERNAME=root' > $(envfile)
	echo 'DJANGO_SUPERUSER_PASSWORD=rootpassword' >> $(envfile)
	echo 'DJANGO_SUPERUSER_EMAIL=example@example.com' >> $(envfile)
	echo 'DB_HOST=localhost' >> $(envfile)
	echo 'DB_PORT=5451' >> $(envfile)
	echo 'DB_PORT_TEST=5455' >> $(envfile)
	echo 'DB_USER=postgres' >> $(envfile)
	echo 'DB_PASS=postgres' >> $(envfile)
	echo 'DB_NAME=db_app' >> $(envfile)
	echo 'SECRET_KEY=r2res1y1fsdfsdfsdfsdfskmw49!(cjedsf7r6w))0s+_dojngz%$d1@@p@1_l3#8dfffdsfix2lj5ni)fq' >> $(envfile)
	echo 'DEBUG=True' >> $(envfile)
	echo 'ALLOWED_HOSTS=*' >> $(envfile)
	echo 'SUCCESS_URL=https://localhost' >> $(envfile)
	echo 'RETURN_URL=https://localhost' >> $(envfile)
	echo 'STRIPE_PUB_KEY=' >> $(envfile)
	echo 'STRIPE_SEC_KEY=' >> $(envfile)