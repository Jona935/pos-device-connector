@echo off
title Iniciar Agente Local POS - VERSIÓN FINAL SIMPLIFICADA
color 0A

echo ================================================================
echo                AGENTE LOCAL POS DEVICE CONNECTOR
echo                   VERSIÓN FINAL SIMPLIFICADA
echo ================================================================
echo.

echo URL VPS: http://18.222.185.0:5000
echo Puerto Agente: 5001
echo.

echo Iniciando agente final simplificado...

if exist local_agent_simplificado.py (
    echo ✅ Archivo local_agent_simplificado.py encontrado
    python local_agent_simplificado.py
) else (
    echo ❌ No se encuentra local_agent_simplificado.py
    echo.
    echo Buscando archivos disponibles...
    dir /b local_agent*.py
    echo.
    echo Por favor, asegúrate de estar en la carpeta correcta del proyecto.
)

pause