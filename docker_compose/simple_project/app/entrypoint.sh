# Description: Entrypoint for the Docker container
# Collect static files
python manage.py collectstatic --noinput
# Apply database migrations
python manage.py migrate
# Start server
uwsgi --strict --ini uwsgi.ini