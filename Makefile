setup:
	pip install -r requirements.txt

run:
	uvicorn api.fastapi.main:app

docker:
	docker-compose -f devops/docker/docker-compose.yml up -d --build web
