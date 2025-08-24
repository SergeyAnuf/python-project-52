import os
import sys
from pathlib import Path

# Добавляем корень проекта в sys.path
root = Path(__file__).resolve().parent
sys.path.insert(0, str(root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')

import django  # noqa: E402
django.setup()  # noqa: E402