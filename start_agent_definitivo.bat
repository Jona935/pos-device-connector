@echo off
title Iniciar Agente Local POS - VERSIÓN DEFINITIVA
color 0A

echo ================================================================
echo                AGENTE LOCAL POS DEVICE CONNECTOR
echo                  VERSIÓN DEFINITIVA CON LOGS
echo ================================================================
echo.

echo Ubicación actual: %~dp0
echo.

echo Verificando agente...

if exist local_agent_definitivo.py (
    echo ✅ Archivo local_agent_definitivo.py encontrado
    
    REM Crear directorio de datos si no existe
    if not exist "%USERPROFILE%\POSDeviceConnector" (
        echo 📁 Creando directorio de datos: %USERPROFILE%\POSDeviceConnector
        mkdir "%USERPROFILE%\POSDeviceConnector"
    )
    
    echo.
    echo URL VPS: http://18.222.185.0:5000
    echo Puerto Agente: 5001
    echo Datos guardados en: %USERPROFILE%\POSDeviceConnector
    echo.
    echo Iniciando agente definitivo con soporte completo...
    
    REM Ejecutar con la carpeta actual en PATH
    python "%~dp0\local_agent_definitivo.py"
    
    if errorlevel 1 (
        echo.
        echo ❌ Error iniciando el agente
        echo Revisando logs disponibles...
        echo.
        dir "%USERPROFILE%\POSDeviceConnector\*.log"
    ) else (
        echo.
        echo ✅ Agente iniciado correctamente
        echo 📋 Logs disponibles en: %USERPROFILE%\POSDeviceConnector
    )
    
) else (
    echo ❌ No se encuentra local_agent_definitivo.py
    echo.
    echo Buscando en carpeta actual...
    dir /b local_agent*.py
    echo.
    echo Por favor, asegúrate de estar en la carpeta correcta del proyecto.
    echo.
    echo Si necesitas descargar desde GitHub, presiona cualquier tecla...
    pause
    
    echo Descargando última versión...
    curl -L https://raw.githubusercontent.com/Jona935/pos-device-connector/master/local_agent_definitivo.py -o local_agent_definitivo.py
    
    echo ✅ Descarga completada. Ejecutando...
    python local_agent_definitivo.py
)

pause