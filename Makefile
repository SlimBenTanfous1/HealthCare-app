# Run local dev
up:
	docker-compose up --build

# Run tests inside docker
test:
	docker-compose -f docker-compose.test.yml run --rm api pytest --cov=. --cov-report=term

# Run migrations
migrate:
	docker-compose exec api flask db upgrade

# Seed data
seed:
	docker-compose exec api flask seed

# Build & push image for prod
deploy:
	docker build -t slimbentanfous1/healthcare-app:latest .
	docker push slimbentanfous1/healthcare-app:latest
