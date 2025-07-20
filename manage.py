#!/usr/bin/env python
import os
import sys


def main():
    # Добавьте путь к src в sys.path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(current_dir, 'src')
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')

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
    main()