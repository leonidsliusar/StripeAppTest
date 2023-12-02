run:
	docker compose up -d
	@echo Check App http://localhost:81/admin

stop:
	docker compose down -v

test:
	pytest -v

