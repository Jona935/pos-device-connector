# POS Device Connector

Herramienta para conectar dispositivos locales (impresoras, básculas) con sistema POS en la nube.

## Características

- Detección automática de impresoras locales
- Comunicación con básculas por puerto serial
- API REST para integración con POS en la nube
- Soporte para Docker y Docker Compose
- Simulador de POS en la nube para pruebas

## Instalación

### Local (Windows)

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python app.py
```

### Docker

```bash
# Construir y ejecutar con Docker Compose
docker-compose up --build
```

## API Endpoints

### Dispositivos Locales

- `GET /devices/printers` - Listar impresoras disponibles
- `GET /devices/scales` - Listar básculas disponibles
- `POST /print` - Imprimir ticket
- `POST /scale/read` - Leer peso de báscula

### Conexión con Nube

- `POST /cloud/connect` - Conectar con POS en la nube

## Ejemplo de Uso

### Conectar con POS en la nube

```bash
curl -X POST http://localhost:5000/cloud/connect \
  -H "Content-Type: application/json" \
  -d '{
    "cloud_url": "http://localhost:5001",
    "api_key": "test-api-key"
  }'
```

### Imprimir ticket

```bash
curl -X POST http://localhost:5000/print \
  -H "Content-Type: application/json" \
  -d '{
    "printer_name": "Microsoft Print to PDF",
    "content": {
      "items": [
        {"name": "Producto 1", "price": 10.50, "qty": 2},
        {"name": "Producto 2", "price": 5.25, "qty": 1}
      ],
      "total": 26.25
    }
  }'
```

### Leer báscula

```bash
curl -X POST http://localhost:5000/scale/read \
  -H "Content-Type: application/json" \
  -d '{
    "scale_port": "COM1"
  }'
```

## Arquitectura

```
┌─────────────────┐    API REST    ┌──────────────────┐
│   Dispositivos  │◄──────────────►│  POS en Nube     │
│   Locales       │                │  (Flask)         │
└─────────────────┘                └──────────────────┘
         ▲                                   ▲
         │                                   │
         ▼                                   ▼
┌─────────────────┐                ┌──────────────────┐
│ Device Manager  │                │  Cloud Client    │
│ (Windows API)   │                │  (HTTP Requests) │
└─────────────────┘                └──────────────────┘
```

## Despliegue con Dockploy

1. Subir código a repositorio Git
2. Conectar repositorio en Dockploy
3. Configurar variables de entorno:
   - `CLOUD_URL`: URL del POS en la nube
   - `API_KEY`: Clave de API
4. Desplegar

## Notas

- En Windows, requiere pywin32 para acceso a impresoras
- Para básculas, configurar puerto COM correcto
- El simulador en el puerto 5001 emula el POS en la nube