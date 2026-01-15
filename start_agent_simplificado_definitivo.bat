@echo off
title Iniciar Agente Local POS - VERSIÓN FINAL
color 0A

echo ================================================================
echo                AGENTE LOCAL POS DEVICE CONNECTOR
echo                   VERSIÓN FINAL SIMPLIFICADA
echo ================================================================
echo.

echo URL VPS: http://18.222.185.0:5000
echo Puerto Agente: 5001
echo.

echo Buscando agente local...

if exist local_agent_simplificado.py (
    echo ✅ Archivo local_agent_simplificado.py encontrado
    echo URL VPS: http://18.222.185.0:5000
    echo Puerto Agente: 5001
    echo.
    echo Iniciando agente final simplificado...
    python local_agent_simplificado.py
) else (
    echo ❌ No se encuentra local_agent_simplificado.py
    echo.
    echo Buscando en todas las subcarpetas...
    dir /s local_agent*.py /b
    echo.
    echo Asegúrate de estar en la carpeta correcta del proyecto.
    echo.
    echo Listando archivos encontrados:
    for /f "%%f" in (*.py) do (
        echo     %%f
    )
    
    echo.
    echo Posibles soluciones:
    echo     1. Copiar local_agent_simplificado.py al directorio actual
    echo     2. Moverse a una carpeta sin caracteres especiales
    echo     3. Ejutar desde la carpeta del proyecto
    echo.
    echo Si los problemas persisten, revisar el manual de instalación.
    echo.
    echo Archivos que deberían existir:
    echo     - local_agent_simplificado.py (versión final)
    echo     - requirements.txt (dependencias)
    echo     - agent_config.json (configuración)
    echo.
    
    echo Archivos que pueden ser eliminados (versiones antiguas):
    echo     - local_agent_final.py
    echo     - local_agent_fixed.py
    echo     - local_agent_simple.py
    
    echo.
    echo El script intentará descargar la última versión automáticamente si es necesario.
    
    echo.
    echo ¿Desea que el script copie el archivo a su directorio actual?
    
    echo Si no hay más problemas, presione cualquier tecla para continuar...
    echo De lo contrario, presione 'S' para copiar.
    
    set /p copy=
    set /p copy_option=
    
    if /i "%copy_option%"=="S" (
        echo Copiando local_agent_simplificado.py a directorio actual...
        copy "local_agent_simplificado.py" "local_agent.py" /Y > nul
        
        echo ✅ Archivo copiado correctamente
        echo.
        echo Ahora puedes ejecutar: python local_agent.py
    ) else (
        echo No se copió el archivo.
    )
    
    echo.
    echo Presione una tecla para continuar...
    pause >nul

)