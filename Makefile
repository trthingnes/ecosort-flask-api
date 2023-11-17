.PHONY: build
build:
	docker build . --tag ghcr.io/trthingnes/ecosort-flask-api:latest

.PHONY: run
run:
	docker run -p 8080:8080 ghcr.io/trthingnes/ecosort-flask-api:latest

.PHONY: push
push:
	docker push ghcr.io/trthingnes/ecosort-flask-api:latest