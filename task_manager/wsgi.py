import os
import sys

# Добавьте путь к src
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..')  # Переходим в папку src
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')
application = get_wsgi_application()