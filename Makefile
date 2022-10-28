make_migrations:
	docker-compose run --rm web sh -c "python manage.py makemigrations"
migrate:
	docker-compose run --rm web sh -c "python manage.py migrate"
test:
	docker-compose run --rm web sh -c "python manage.py test"
create_super:
	docker-compose run --rm web sh -c "python manage.py createsuperuser"
shell:
	docker-compose run --rm web sh -c "python manage.py shell"