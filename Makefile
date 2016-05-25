clean:
	find . -name "__pycache__" -type d | xargs rm -rf

# This is probably bad, but since we are using docker-compose I
# am just assuming we are using the default database (postgres)
# and calling it a day.
migrate:
	docker-compose run web yoyo apply

build_dev:
	docker-compose build

serve_dev: build_dev
	docker-compose up

.PHONY: clean build_dev serve_dev
