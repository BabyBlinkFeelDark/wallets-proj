import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'project_root.settings'  # Замените на путь к вашему файлу настроек
django.setup()