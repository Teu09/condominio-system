@echo off
echo ========================================
echo   VERIFICACAO DE REQUISITOS DO SISTEMA
echo ========================================
echo.

echo Verificando Docker...
docker --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Docker instalado
    docker --version
) else (
    echo [ERRO] Docker nao encontrado!
    echo Por favor, instale o Docker Desktop
    echo Download: https://www.docker.com/products/docker-desktop/
    goto :end
)

echo.
echo Verificando Docker Compose...
docker-compose --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Docker Compose instalado
    docker-compose --version
) else (
    echo [ERRO] Docker Compose nao encontrado!
    goto :end
)

echo.
echo Verificando se Docker esta rodando...
docker ps >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Docker esta rodando
) else (
    echo [ERRO] Docker nao esta rodando!
    echo Por favor, inicie o Docker Desktop
    goto :end
)

echo.
echo Verificando portas disponiveis...
netstat -an | findstr ":8080" >nul
if %errorlevel% equ 0 (
    echo [AVISO] Porta 8080 ja esta em uso
) else (
    echo [OK] Porta 8080 disponivel
)

netstat -an | findstr ":5432" >nul
if %errorlevel% equ 0 (
    echo [AVISO] Porta 5432 ja esta em uso
) else (
    echo [OK] Porta 5432 disponivel
)

echo.
echo ========================================
echo   VERIFICACAO CONCLUIDA
echo ========================================
echo.
echo Se todos os itens estao [OK], voce pode executar:
echo   iniciar_sistema.bat
echo.

:end
pause






