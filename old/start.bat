@echo off
echo Iniciando POS Device Connector...
echo.

REM Iniciar servidor principal
echo Iniciando servidor principal en puerto 5000...
start "POS Device Connector" cmd /k "cd /d %~dp0 && python app.py"

REM Esperar a que el servidor principal inicie
timeout /t 3 /nobreak >nul

REM Iniciar simulador de nube
echo Iniciando simulador de POS en la nube en puerto 5001...
start "POS Cloud Simulator" cmd /k "cd /d %~dp0 && python simulator.py"

REM Esperar a que el simulador inicie
timeout /t 3 /nobreak >nul

echo.
echo Servidores iniciados!
echo.
echo Servicios disponibles:
echo - API Principal: http://localhost:5000
echo - Simulador Nube: http://localhost:5001
echo.
echo Ejecutando prueba de API...
python test_api.py

echo.
echo Presiona cualquier tecla para salir...
pause >nul