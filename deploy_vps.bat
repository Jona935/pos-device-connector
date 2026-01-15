@echo off
echo 🐳 Preparando despliegue VPS/Dockploy para Windows...
echo ================================================================

REM Verificar Docker
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker no está instalado o no está en PATH
    pause
    exit /b 1
)

REM Verificar Docker Compose
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose no está instalado o no está en PATH
    pause
    exit /b 1
)

echo ✅ Docker y Docker Compose disponibles

REM Limpiar construcciones anteriores
echo 🧹 Limpiando construcciones anteriores...
docker-compose -f docker-compose.prod.yml down --volumes --remove-orphans
docker system prune -f

REM Construir imagen de producción
echo 🔨 Construyendo imagen de producción...
docker-compose -f docker-compose.prod.yml build --no-cache

if %errorlevel% neq 0 (
    echo ❌ Error construyendo imagen
    pause
    exit /b 1
)

echo ✅ Imagen construida exitosamente

REM Iniciar servicios
echo 🚀 Iniciando servicios...
docker-compose -f docker-compose.prod.yml up -d

REM Esperar a que los servicios inicien
echo ⏳ Esperando a que los servicios inicien...
timeout /t 15 /nobreak >nul

REM Verificar estado
echo 🔍 Verificando estado de los servicios...
docker-compose -f docker-compose.prod.yml ps

REM Ejecutar pruebas
echo 🧪 Ejecutando pruebas VPS...
python test_vps.py http://localhost:5000

echo ================================================================
echo 🎉 Despliegue VPS completado!
echo 📊 Revisa los resultados de las pruebas arriba
echo 🌐 API disponible en: http://localhost:5000
echo 💚 Health check: http://localhost:5000/health
echo 📈 Métricas: http://localhost:5000/metrics
echo.
echo Para detener los servicios:
echo docker-compose -f docker-compose.prod.yml down
echo.
pause