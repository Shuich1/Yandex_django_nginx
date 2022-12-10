Django + Nginx + PostgreSQL + Docker Compose Web App
===============================================
This is a Django web app that uses Docker Compose to run a Django app with a PostgreSQL database and Nginx web server.

## Requirements
- Docker
- Docker Compose

## Installation
1. Clone the repository
2. Create .env file in the root directory with template from example.env
3. Run `docker-compose up` to build the images and run the containers

## Usage
- The Django app will be available at http://localhost:8000
- The PostgreSQL database will be available at port 5432 on the Docker host
