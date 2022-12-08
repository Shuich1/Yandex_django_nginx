from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

include(
    'components/common.py',
    'components/database.py',
    'components/internationalization.py',
)
