.PHONY: help build up down logs test

help:
	@echo "Available targets: build, up, down, logs, test"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

test:
	pytest tests/