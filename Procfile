#web: PYTHONPATH=webvicentenario gunicorn webvicentenario.wsgi:application --bind 0.0.0.0:$PORT

web: python webvicentenario/manage.py collectstatic --noinput && gunicorn webvicentenario.webvicentenario.wsgi:application --bind 0.0.0.0:$PORT