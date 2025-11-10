@echo off
REM Script de execução do Formatador ABNT para Windows
REM Este script verifica se as dependências estão instaladas e executa o aplicativo

echo ========================================
echo   FORMATADOR ABNT - Desktop
echo ========================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Python nao encontrado!
    echo.
    echo Por favor, instale Python 3.7 ou superior:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo.

REM Verifica se as dependências estão instaladas
echo Verificando dependencias...
python -c "import docx" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] Instalando dependencias necessarias...
    echo.
    pip install -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo [ERRO] Falha ao instalar dependencias!
        echo.
        pause
        exit /b 1
    )
    echo.
    echo [OK] Dependencias instaladas com sucesso!
) else (
    echo [OK] Dependencias ja instaladas
)

echo.
echo Iniciando Formatador ABNT...
echo.

REM Executa o aplicativo
python formatador_abnt.py

REM Verifica se houve erro na execução
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRO] Ocorreu um erro ao executar o aplicativo
    echo.
    pause
    exit /b 1
)

pause
