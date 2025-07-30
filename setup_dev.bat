@echo off
echo 正在設置寵物預訂平台開發環境...

REM 啟動虛擬環境
call .venv\Scripts\activate

echo.
echo ========================================
echo 環境設置完成！
echo ========================================
echo.
echo 可用的命令：
echo   前端開發伺服器: cd frontend && pnpm dev
echo   Django 後端:   cd backend\django_app && python manage.py runserver
echo   Flask 通知服務: cd backend\flask_services\notification_service && python app.py
echo.
echo 或者使用 VS Code 任務:
echo   Ctrl+Shift+P -> Tasks: Run Task -> Start All Services
echo.
echo 服務端口：
echo   前端 (Vue):     http://localhost:5173
echo   Django API:     http://localhost:8000
echo   Flask 通知服務: http://localhost:5000
echo.
