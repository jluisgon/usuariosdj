from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret('DB_NAME'),
        'USER': get_secret('USER'),
        'PASSWORD' : get_secret('PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# se la indica la carpeta donde estaran los archivos estaticos --> static
STATICFILES_DIRS = [BASE_DIR.child('static')]

# para guardar los archivos multimedias
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.child('media')

# email settings
# activar el envio de emails don Django
EMAIL_USE_TLS = True
# con que tipo de correo vamos a enviarlo
EMAIL_HOST = 'smtp.gmail.com'
# correo remitente
EMAIL_HOST_USER = get_secret('EMAIL')
# password del email
EMAIL_HOST_PASSWORD = get_secret('PASS_EMAIL')
# puerto de correos. en los servidores de ubuntu es el 587
EMAIL_PORT = '587'
