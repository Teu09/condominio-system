@echo off
echo ========================================
echo    SISTEMA DE CONDOMINIO - INICIANDO
echo ========================================
echo.

echo Verificando se o Docker esta rodando...
docker version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Docker nao esta rodando ou nao esta instalado!
    echo Por favor, instale o Docker Desktop e inicie-o.
    pause
    exit /b 1
)

echo Docker encontrado! Iniciando sistema...
echo.

echo Parando containers existentes (se houver)...
docker-compose down

echo.
echo Construindo e iniciando todos os servicos...
echo Isso pode levar alguns minutos na primeira execucao...
echo.

docker-compose up --build

echo.
echo Sistema finalizado.
pause
