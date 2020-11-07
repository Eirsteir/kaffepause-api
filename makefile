start:
	docker-compose -f local.yml up

fresh:
	docker-compose -f local.yml build
	make start

install:
	docker-compose -f local.yml run --rm django pip install -r requirements/local.txt

rebuild:
	docker-compose -f local.yml run --rm django python manage.py reset_db --noinput
	make makemigrations
	make migrate
	make seed

shell:
	docker-compose -f local.yml run --rm django python manage.py shell_plus

createsuperuser: ##@Docker Create a superuser
	docker-compose -f local.yml run --rm django python manage.py createsuperuser

makemigrations: ##@Docker Set up migration files
	docker-compose -f local.yml run --rm django python manage.py makemigrations

migrate: ##@Docker Perform migrations to database
	docker-compose -f local.yml run --rm django python manage.py migrate

dumpdata:
	docker-compose -f local.yml run --rm django python manage.py dumpdata --indent=4 --format=json > ./kaffepause/fixture.json

loaddata:
	docker-compose -f local.yml run --rm django python manage.py loaddata ./kaffepause/fixture.json

seed:
	docker-compose -f local.yml run --rm django python manage.py seed ${args}
	make dumpdata

test:
	docker-compose -f local.yml run --rm django pytest ${args}

coverage:
	docker-compose -f local.yml run --rm django coverage run -m pytest
	docker-compose -f local.yml run --rm django coverage report
