@echo off
echo ========================================
echo    PARANDO SISTEMA DE CONDOMINIO
echo ========================================
echo.

echo Parando todos os containers...
docker-compose down

echo.
echo Sistema parado com sucesso!
echo.
pause
