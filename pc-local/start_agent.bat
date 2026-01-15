@echo off
title Iniciar Agente Local POS
color 0B

echo ================================================================
echo                AGENTE LOCAL POS DEVICE CONNECTOR
echo ================================================================
echo.
echo URL VPS: http://18.222.185.0:5000
echo Puerto Agente: 5001
echo.
echo Iniciando agente...
python local_agent_simple.py
pause