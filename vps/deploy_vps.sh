#!/bin/bash

echo "🚀 Desplegando POS Device Connector en VPS"
echo "================================================"

# Detener contenedor anterior
docker stop pos-connector 2>/dev/null
docker rm pos-connector 2>/dev/null

# Construir imagen
echo "🔨 Construyendo imagen..."
docker build -t pos-connector .

# Iniciar contenedor
echo "🚀 Iniciando contenedor..."
docker run -d \
  --name pos-connector \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e PORT=5000 \
  --restart unless-stopped \
  pos-connector

# Verificar
echo "🔍 Verificando estado..."
sleep 3
docker ps
docker logs pos-connector

echo "✅ Despliegue completado!"
echo "🌐 API disponible en: http://localhost:5000"