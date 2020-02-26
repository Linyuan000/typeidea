from .base import * # NOQA
# 告诉 PEP8规范检测工具这个地方不需要检测 
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}