.PHONY: build
build:
	docker build . --tag ghcr.io/trthingnes/ecosort-flask-api:latest

.PHONY: run
run:
	docker run ghcr.io/trthingnes/ecosort-flask-api:latest

.PHONY: push
push:
	docker push ghcr.io/trthingnes/ecosort-flask-api:latest