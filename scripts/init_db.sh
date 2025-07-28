#!/bin/bash

echo "Initializing database..."

# 進入 Django 應用目錄
cd backend/django_app

# 建立資料庫遷移檔案
python manage.py makemigrations

# 執行資料庫遷移
python manage.py migrate

# 建立超級使用者 (可選)
echo "Creating superuser..."
python manage.py createsuperuser

# 載入初始資料 (如果有 fixtures)
# python manage.py loaddata initial_data.json

echo "Database initialization completed!"
