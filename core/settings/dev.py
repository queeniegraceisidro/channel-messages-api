import tempfile

from .base import *


INSTALLED_APPS += (
    "naomi",
)

# To avoid sending data real clients in the future, do a naomi backend
EMAIL_BACKEND="naomi.mail.backends.naomi.NaomiBackend"
EMAIL_FILE_PATH = tempfile.gettempdir()
