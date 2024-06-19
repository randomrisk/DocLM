.PHONY: docker-dev
docker-dev:
	docker build -t server-qa-stream:dev -f dev/Dockerfile .

.PHONY: run-dev
run-dev:
	docker-compose -f dev/docker-compose.yaml --env-file dev/.env up


.PHONY: docker
docker:
	docker build -t server-qa-stream:dev -f prod/Dockerfile .

.PHONY: run
run:
	docker-compose -f prod/docker-compose.yaml --env-file prod/.env up

.PHONY: rund
rund:
	docker-compose -f prod/docker-compose.yaml --env-file prod/.env up -d