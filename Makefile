tag=latest

run:
	@docker-compose run --service-ports backup

build:
	@docker build --pull  -t mwaaas/db_backup:$(tag) .

push:
	@docker push mwaaas/db_backup:$(tag)

build_push: build push