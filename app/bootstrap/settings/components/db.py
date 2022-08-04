from app.bootstrap.config import Config
from app.utils import resolve_root

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'USER': Config.get('db.user'),
#         'NAME': Config.get('db.name'),
#         'PASSWORD': Config.get('db.pass'),
#         'HOST': Config.get('db.host'),
#         'PORT': Config.get('db.port'),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':  resolve_root('db.sqlite'),
    }
}

migration_subfolder = Config.get('main.migration_folder_name')
if not migration_subfolder:
    migration_subfolder = 'unnamed'

MIGRATION_MODULES = {'app': f'migrations.{migration_subfolder}'}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'