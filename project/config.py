import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def load_config():
    config_path = BASE_DIR / 'config.json'

    if not config_path.exists():
        return {
            'database': {
                'name': 'vk_project_so',
                'user': 'root',
                'password': '',
                'host': 'localhost',
                'port': 3306
            },
            'django': {
                'secret_key': 'django-insecure-fallback-key',
                'debug': True,
                'allowed_hosts': ['localhost', '127.0.0.1'],
                "language_code": "en-us",
                "time_zone": "UTC"
            },
            "paths": {
                "media_root": "media",
                "static_root": "staticfiles"
            }
        }
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

config = load_config()