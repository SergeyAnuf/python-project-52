import os
import sys
from pathlib import Path

# Добавляем корень проекта в sys.path
root = Path(__file__).resolve().parent
sys.path.insert(0, str(root))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')
django.setup()