import os
import sys
from django.core.wsgi import get_wsgi_application


current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')
application = get_wsgi_application()