start:
	docker-compose -f local.yml up

fresh:
	docker-compose -f local.yml down -v
	docker-compose -f local.yml build
	make migrate
	make install-labels
	make load_locations
	make seed
	make start

install:
	docker-compose -f local.yml run --rm django pip install -r requirements/local.txt

rebuild:
	docker-compose -f local.yml run --rm django python manage.py reset_db --noinput
	make makemigrations
	make migrate

shell:
	docker-compose -f local.yml run --rm django python manage.py shell_plus

createsuperuser: ##@Docker Create a superuser
	docker-compose -f local.yml run --rm django python manage.py createsuperuser

makemigrations: ##@Docker Set up migration files
	docker-compose -f local.yml run --rm django python manage.py makemigrations

migrate: ##@Docker Perform migrations to database
	docker-compose -f local.yml run --rm django python manage.py migrate

install-labels: ##@Docker Perform migrations to database
	docker-compose -f local.yml run --rm django python manage.py install_labels

dumpdata:
	docker-compose -f local.yml run --rm django python manage.py dumpdata --indent=4 --format=json > ./kaffepause/fixture.json

loaddata:
	docker-compose -f local.yml run --rm django python manage.py loaddata ./kaffepause/fixture.json

seed:
	docker-compose -f local.yml run --rm django python manage.py seed ${args}

load_locations:
	docker-compose -f local.yml run --rm django python manage.py load_locations

test:
	docker-compose -f local.yml run --rm django pytest kaffepause ${args}

coverage:
	docker-compose -f local.yml run --rm django coverage run -m pytest kaffepause
	docker-compose -f local.yml run --rm django coverage report

startapp:
	mkdir ./kaffepause/${appname}
	docker-compose -f local.yml run --rm django django-admin.py startapp ${appname} ./kaffepause/${appname}
