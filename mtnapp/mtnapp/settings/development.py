from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {

    'default': {
        'ENGINE': os.environ['ENGINE'],
        'NAME': os.environ['NAME'],
        'USER': os.environ['USER'],
        'PASSWORD': os.environ['PASSWORD'],
        'HOST': os.environ['HOST'],
        'PORT': os.environ['PORT'],
    }

}
