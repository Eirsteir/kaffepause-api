start:
	docker-compose -f local.yml up

fresh:
	docker-compose -f local.yml build
	make start

createsuperuser: ##@Docker Create a superuser
	docker-compose -f local.yml run --rm django python manage.py createsuperuser

makemigrations: ##@Docker Set up migration files
	docker-compose -f local.yml run --rm django python manage.py makemigrations

migrate: ##@Docker Perform migrations to database
	docker-compose -f local.yml run --rm django python manage.py migrate

dumpdata:
	docker-compose -f local.yml run --rm django python manage.py dumpdata -e admin -e auth.Permission -e contenttypes --indent=4 > ./app/fixture.json

loaddata:
	docker-compose -f local.yml run --rm django python manage.py loaddata ./app/fixture.json
