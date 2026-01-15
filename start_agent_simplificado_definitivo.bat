@echo off
title Iniciar Agente Local POS - VERSIÓN FINAL SIMPLIFICADA
color 0A

echo ================================================================
echo                AGENTE LOCAL POS DEVICE CONNECTOR
echo                   VERSIÓN FINAL SIMPLIFICADA
echo ================================================================
echo.

echo Verificando directorio actual: %~dp0
echo.

if exist local_agent_simplificado.py (
    echo ✅ Archivo local_agent_simplificado.py encontrado
    echo.
    echo Iniciando agente final simplificado...
    python local_agent_simplificado.py
) else (
    echo ❌ No se encuentra local_agent_simplificado.py
    echo.
    echo Buscando en todas las subcarpetas...
    dir /s local_agent*.py /b
    echo.
    echo Archivos encontrados:
    for %%f in (*.py) do echo     %%f
    echo.
    echo Por favor, copia local_agent_simplificado.py al directorio actual.
)

echo.
pause