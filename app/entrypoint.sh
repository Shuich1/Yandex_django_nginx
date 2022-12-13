# Description: Entrypoint for the Docker container
# Collect static files
python manage.py collectstatic --noinput
# Apply database migrations
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
      echo "Waiting for database..."
done 
python manage.py migrate
# Start server
uwsgi --strict --ini uwsgi.ini