# Guía de Despliegue VPS con Dockploy

## 📋 Requisitos Previos

1. **VPS con Docker instalado**
2. **Cuenta en Dockploy**
3. **Repositorio Git con el código**

## 🚀 Pasos de Despliegue

### 1. Preparar Repositorio Git

```bash
git init
git add .
git commit -m "POS Device Connector v1.0.0"
git remote add origin https://github.com/tu-usuario/pos-device-connector.git
git push -u origin main
```

### 2. Configurar Dockploy

1. **Iniciar sesión en Dockploy**
2. **Crear nuevo servidor**
3. **Conectar repositorio Git**
4. **Configurar variables de entorno**

### 3. Variables de Entorno (Dockploy)

```bash
PORT=5000
FLASK_ENV=production
FLASK_DEBUG=0
LOG_LEVEL=INFO
CLOUD_URL=https://tu-pos-cloud.com
API_KEY=tu-api-key-secreta
CORS_ORIGINS=https://tu-dominio.com
ENABLE_METRICS=true
```

### 4. Configurar Docker Compose

En Dockploy, usar el archivo `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  pos-device-connector:
    build: 
      context: .
      dockerfile: Dockerfile.prod
    restart: unless-stopped
    ports:
      - "${PORT:-5000}:5000"
    environment:
      - FLASK_ENV=production
      - PORT=${PORT:-5000}
      - CLOUD_URL=${CLOUD_URL}
      - API_KEY=${API_KEY}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### 5. Despliegue Automático

Dockploy automáticamente:
- ✅ Clonará el repositorio
- ✅ Construirá la imagen Docker
- ✅ Iniciará los contenedores
- ✅ Configurará health checks
- ✅ Expondrá los puertos

## 🔍 Verificación del Despliegue

### Health Check

```bash
curl https://tu-vps.com:5000/health
```

### API Test

```bash
curl https://tu-vps.com:5000/
```

### Métricas

```bash
curl https://tu-vps.com:5000/metrics
```

## 📊 Monitoreo

### Health Check Endpoint

- **URL**: `/health`
- **Método**: GET
- **Respuesta**: Estado del servidor y recursos

### Métricas Endpoint

- **URL**: `/metrics`
- **Método**: GET
- **Respuesta**: Métricas detalladas del sistema

## 🛠️ Solución de Problemas

### Problemas Comunes

1. **Error 502 Bad Gateway**
   - Verificar que el contenedor está corriendo
   - Revisar logs de Dockploy

2. **Error de Conexión**
   - Verificar variables de entorno
   - Confirmar firewall del VPS

3. **Dispositivos no Detectados**
   - En VPS Linux, montar `/dev:/dev:ro`
   - Verificar permisos de USB/serial

### Logs y Debug

```bash
# Ver logs del contenedor
docker logs pos-device-connector

# Ver estado de servicios
docker-compose -f docker-compose.prod.yml ps
```

## 🔄 Actualizaciones

Dockploy soporta actualizaciones automáticas:

1. **Push al repositorio**
2. **Dockploy detecta cambios**
3. **Reconstrucción automática**
4. **Despliegue sin downtime**

## 🌐 Dominio y SSL

Configurar en Dockploy:

1. **Añadir dominio personalizado**
2. **Configurar certificado SSL**
3. **Setup reverse proxy (opcional)**

## 📈 Escalabilidad

Para alta carga:

1. **Aumentar workers de Gunicorn**
2. **Configurar load balancer**
3. **Añadir réplicas del servicio**

```yaml
# Ejemplo de escalado
services:
  pos-device-connector:
    deploy:
      replicas: 3
```

## ✅ Checklist Pre-Despliegue

- [ ] Repositorio Git actualizado
- [ ] Variables de entorno configuradas
- [ ] Dockerfile.prod optimizado
- [ ] Health checks funcionando
- [ ] Tests locales pasando
- [ ] Firewall VPS configurado
- [ ] Dominio SSL configurado
- [ ] Monitoreo activado

## 🎯 Resultado Esperado

Al finalizar tendrás:

- ✅ API funcionando en `https://tu-dominio.com:5000`
- ✅ Health checks automáticos
- ✅ Despliegue continuo con Git
- ✅ Monitoreo de recursos
- ✅ Conexión con dispositivos locales
- ✅ Integración con POS en la nube