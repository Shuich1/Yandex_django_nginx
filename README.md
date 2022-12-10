Django + Nginx + PostgreSQL + Docker Compose Web App
===============================================
This is a Django web app that uses Docker Compose to run a Django app with a PostgreSQL database and Nginx web server.

## Requirements
- Docker
- Docker Compose

## Installation
1. Clone the repository `git clone https://github.com/Shuich1/new_admin_panel_sprint_2.git`
2. Create .env file in the root directory with template from example.env
3. Run `docker-compose up` to build the images and run the containers
4. Run `docker-compose run -v $(pwd)/sqlite_to_postgres:/sqlite_to_postgres -w /sqlite_to_postgres --entrypoint="/bin/bash -c" backend "python load_data.py"` to load data from sqlite to postgres
5. Run `docker-compose run --entrypoint="/bin/bash -c" backend "python manage.py createsuperuser"` to create superuser

## Usage
- The Django app will be available at http://127.0.0.1:8000
- The Django admin will be available at http://127.0.0.1:8000/admin
- The Django API will be available at http://127.0.0.1:8000/movies and http://127.0.0.1:8000/movies/{id}