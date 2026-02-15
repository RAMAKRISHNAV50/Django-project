import os
import sys
sys.path.insert(0, r'C:\Users\ramak\OneDrive\Desktop\Django\v1\woody')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'woody.settings')
import django
django.setup()
from django.db import connection
with connection.cursor() as cur:
    try:
        cur.execute("ALTER TABLE wood_app_quotations ADD COLUMN budget INT NOT NULL DEFAULT 0;")
        print('Added budget column.')
    except Exception as e:
        print('Could not add column (it may already exist):', e)
    cur.execute('SHOW COLUMNS FROM wood_app_quotations')
    for row in cur.fetchall():
        print(row)