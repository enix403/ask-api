# settings/__init__.py
# We use django-split-settings to split the application's settings into separate files in a
# manageable way.
#
# components/ folder contains common settings while environments/ folder contains environment specific settings

from dotenv import load_dotenv
from split_settings.tools import include

from app.bootstrap.config import Config
from app.utils import resolve_root

# Make sure the .env file is read before calling Config.load_default()
load_dotenv(resolve_root('.env'))
Config.load_default()

# Choose the correct settings file based on current environment
environment = 'development' if Config.get_bool('runtime.debug') else 'production'

setting_files = [
    'components/base.py',
    'components/db.py',
    'components/monkeypatchmigrations.py',
    'components/middleware.py',
    'components/templates.py',
    
    f'environments/{environment}.py'
]

include(*setting_files)


