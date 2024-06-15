.PHONY: docker
docker:
	docker build -t nginx:dev -f Dockerfile .
.PHONY: run
run:
	docker-compose -f docker-compose.yaml up
.PHONY: rund
rund:
	docker-compose -f docker-compose.yaml up -d