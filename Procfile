release: python manage.py migrate
web: gunicorn home_manager.wsgi:application --port $PORT --bind 0.0.0.0 -v2