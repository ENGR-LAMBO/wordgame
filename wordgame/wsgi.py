"""
WSGI config for wordgame project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wordgame.settings')

application = get_wsgi_application()



if __name__ == '__main__':
    import os
    from gunicorn.app.wsgiapp import run
    port = os.environ.get('PORT', '10000')
    run()  # This will use the default Gunicorn settings, including port