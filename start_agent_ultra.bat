@echo off
title Iniciar Agente Local POS - VERSIÓN FINAL
color 0A

echo ================================================================
echo                AGENTE LOCAL POS DEVICE CONNECTOR
echo                   VERSIÓN FINAL CORREGIDA
echo ================================================================
echo.

REM Obtener la ruta del script actual
set SCRIPT_DIR=%~dp0

echo Ubicación actual: %SCRIPT_DIR%
echo.

echo Buscando agente local...

if exist "%SCRIPT_DIR%\local_agent_final.py" (
    echo ✅ Archivo local_agent_final.py encontrado
    echo URL VPS: http://18.222.185.0:5000
    echo Puerto Agente: 5001
    echo.
    echo Iniciando agente final corregido...
    python "%SCRIPT_DIR%\local_agent_final.py"
) else (
    echo ❌ No se encuentra local_agent_final.py en: %SCRIPT_DIR%
    echo Buscando archivos disponibles...
    dir /b "%SCRIPT_DIR%\local_agent*.py"
    echo.
    echo Asegúrate de:
    echo 1. Estar en la carpeta correcta del proyecto
    echo 2. Descargar la última versión desde GitHub
    echo.
    echo ¿Quieres descargar desde GitHub? (S/N)
    set /p download=
    if /i "!download!"=="S" (
        echo Descargando última versión...
        curl -L https://raw.githubusercontent.com/Jona935/pos-device-connector/master/local_agent_final.py -o local_agent_final.py
        echo ✅ Descarga completada
        python local_agent_final.py
    ) else (
        echo Por favor, revisa la ubicación de los archivos.
    )
)

pause