up:
	docker-compose up --build

down:
	docker-compose down

migrate:
	docker-compose exec api flask db upgrade

seed:
	docker-compose exec api flask seed

test:
	docker-compose exec api pytest --cov=. --cov-report=term
