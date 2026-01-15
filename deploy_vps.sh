#!/bin/bash

echo "🐳 Preparando despliegue VPS/Dockploy..."
echo "================================================"

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado"
    exit 1
fi

# Verificar Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado"
    exit 1
fi

echo "✅ Docker y Docker Compose disponibles"

# Limpiar construcciones anteriores
echo "🧹 Limpiando construcciones anteriores..."
docker-compose -f docker-compose.prod.yml down --volumes --remove-orphans
docker system prune -f

# Construir imagen de producción
echo "🔨 Construyendo imagen de producción..."
docker-compose -f docker-compose.prod.yml build --no-cache

if [ $? -eq 0 ]; then
    echo "✅ Imagen construida exitosamente"
else
    echo "❌ Error construyendo imagen"
    exit 1
fi

# Iniciar servicios
echo "🚀 Iniciando servicios..."
docker-compose -f docker-compose.prod.yml up -d

# Esperar a que los servicios inicien
echo "⏳ Esperando a que los servicios inicien..."
sleep 10

# Verificar estado
echo "🔍 Verificando estado de los servicios..."
docker-compose -f docker-compose.prod.yml ps

# Ejecutar pruebas
echo "🧪 Ejecutando pruebas VPS..."
python test_vps.py http://localhost:5000

echo "================================================"
echo "🎉 Despliegue VPS completado!"
echo "📊 Revisa los resultados de las pruebas arriba"
echo "🌐 API disponible en: http://localhost:5000"
echo "💚 Health check: http://localhost:5000/health"
echo "📈 Métricas: http://localhost:5000/metrics"