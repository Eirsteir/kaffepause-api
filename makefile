start:
	docker-compose -f local.yml up

fresh:
	docker-compose -f local.yml build
	make start
