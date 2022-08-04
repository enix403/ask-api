from dotenv import load_dotenv
from split_settings.tools import include

from app.bootstrap.config import Config
from app.utils import resolve_root

load_dotenv(resolve_root('.env'))

Config.load_default()
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


