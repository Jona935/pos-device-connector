@echo off
title Instalador - Agente Local POS Device Connector
color 0A

echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║         INSTALADOR AGENTE LOCAL POS DEVICE CONNECTOR               ║
echo  ║                                                              ║
echo  ║  Este instalador configurara el agente para que tu POS en la       ║
echo  ║  nube pueda controlar impresoras y dispositivos locales             ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.

pause
cls

echo [1/5] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  ❌ Python no esta instalado
    echo.
    echo  Descargando e instalando Python 3.11...
    start https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
    echo.
    echo  Por favor instala Python y ejecuta este instalador nuevamente.
    pause
    exit /b 1
) else (
    echo  ✅ Python detectado
    python --version
)

echo.
echo [2/5] Instalando dependencias Python...
echo  Instalando pywin32...
pip install pywin32==311

echo  Instalando Flask...
pip install flask

echo  Instalando requests...
pip install requests

echo  Instalando pyserial...
pip install pyserial

echo  Instalando python-escpos...
pip install python-escpos

echo.
echo [3/5] Creando configuracion...
set /p url_vps="Ingrese la URL del VPS (default: http://appprueba-app-0satlm-f01c99-3-148-104-162.traefik.me): " || set url_vps=http://appprueba-app-0satlm-f01c99-3-148-104-162.traefik.me

echo.
echo [4/5] Configurando acceso automatico...
set /p auto_start="¿Desea iniciar el agente automaticamente con Windows? (S/N): "
if /i "%auto_start%"=="S" (
    echo  Creando acceso directo en Startup...
    powershell -command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Agente POS.lnk'); $Shortcut.TargetPath = '%cd%\start_agent.bat'; $Shortcut.Save()"
)

echo.
echo [5/5] Creando scripts de inicio...

REM Crear start_agent.bat
(
echo @echo off
echo title Agente Local POS
echo color 0B
echo echo ╔══════════════════════════════════════════════════════════════╗
echo echo ║          AGENTE LOCAL POS DEVICE CONNECTOR                      ║
echo echo ║                                                              ║
echo echo ║  Conectando dispositivos locales con POS en la nube...           ║
echo echo ╚══════════════════════════════════════════════════════════════╝
echo echo.
echo echo URL VPS: %url_vps%
echo echo Puerto Agente: 5001
echo echo.
echo python local_agent.py
echo pause
) > start_agent.bat

REM Crear stop_agent.bat
(
echo @echo off
echo title Detener Agente
echo taskkill /f /im python.exe 2>nul
echo taskkill /f /im pythonw.exe 2>nul
echo echo Agente detenido.
echo pause
) > stop_agent.bat

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    INSTALACION COMPLETADA                    ║
echo ║                                                              ║
echo ║  ✅ Dependencias instaladas                                      ║
echo ║  ✅ Scripts de inicio creados                                    ║
echo ║  ✅ Configuracion aplicada                                      ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Comandos disponibles:
echo.
echo   🚀 Iniciar Agente:     start_agent.bat
echo   🛑 Detener Agente:      stop_agent.bat
echo   🔗 URL VPS:           %url_vps%
echo.
echo El agente se iniciara en el puerto 5001
echo.
echo ¿Iniciar el agente ahora? (S/N)
set /p start_now=
if /i "%start_now%"=="S" (
    echo.
    echo Iniciando agente...
    start /min start_agent.bat
)

echo.
echo Instalacion completada. El agente esta listo para usar.
echo.
pause