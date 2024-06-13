web: gunicorn wordgame.wsgi:application --bind 0.0.0.0:$PORT --workers 3


bind = "0.0.0.0:10000"
workers = 3
timeout = 120

web: gunicorn -c gunicorn_config.py wordgame.wsgi:application
