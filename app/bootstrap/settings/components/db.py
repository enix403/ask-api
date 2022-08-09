from app.bootstrap.config import Config
from app.utils import resolve_root, root_directory

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
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# This allows us to have multiple migrations folders (with separate databases). This is useful e.g for
# having multiple branches each having different db schemas and, consequently, different migrations. Also allows us
# switch branches freely without worrying about stashing/conflicts
migration_subfolder = Config.get('main.migration_folder_name')
if not migration_subfolder:
    migration_subfolder = 'unnamed'

# Create the required folder if it doesn't exist
root_directory(['migrations', migration_subfolder], create_missing=True)

# Set the actual folder
# See https://docs.djangoproject.com/en/4.1/ref/settings/#migration-modules
MIGRATION_MODULES = {'app': f'migrations.{migration_subfolder}'}
