docker_up:
	docker-compose up

docker_up_background:
	docker-compose up -d

init_db_tables:
	docker exec apicrm python manage.py db init 
	docker exec apicrm python manage.py db migrate 
	docker exec apicrm python manage.py db upgrade

update_db_tables:
	docker exec apicrm python manage.py db migrate 
	docker exec apicrm python manage.py db upgrade
