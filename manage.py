#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import dotenv


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    dotenv.read_dotenv()
    main()

SOCIAL_AUTH_GOOGLE_CLIENT_ID = "949693815197-cb42o1niev0rnved93kpt90vtqiurpub.apps.googleusercontent.com"
SOCIAL_AUTH_GOOGLE_SECRET = "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"
STATE = "idjNEIe2kNGE0vs0vnw"
