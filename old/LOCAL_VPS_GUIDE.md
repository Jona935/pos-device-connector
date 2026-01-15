# Instrucciones de Uso - Local + VPS

## 🎯 Arquitectura Final

```
POS Nube → VPS API → Agente Local → Dispositivos Físicos
```

## 📋 Pasos para Configurar

### 1. **VPS (ya está funcionando)**
URL: http://appprueba-app-0satlm-f01c99-3-148-104-162.traefik.me

### 2. **PC Local - Ejecutar el Agente**

#### En Windows:
```bash
# Abrir CMD o PowerShell
cd C:\ruta\a\pos-device-connector
pip install pywin32 requests flask pyserial python-escpos
python local_agent.py
```

#### Requisitos Local:
```bash
pip install pywin32==311 requests flask pyserial python-escpos
```

### 3. **Flujo de Prueba**

1. **El agente local se registra** automáticamente con el VPS
2. **Ver agentes conectados**:
   ```bash
   curl http://appprueba-app-0satlm-f01c99-3-148-104-162.traefik.me/agents
   ```

3. **Imprimir ticket local desde POS nube**:
   ```bash
   curl -X POST http://appprueba-app-0satlm-f01c99-3-148-104-162.traefik.me/agent/AGENTE_ID/print \
     -H "Content-Type: application/json" \
     -d '{
       "printer_name": "Microsoft Print to PDF",
       "content": {
         "items": [{"name": "Producto Test", "price": 10.50}],
         "total": 10.50
       }
     }'
   ```

4. **Leer báscula local**:
   ```bash
   curl -X POST http://appprueba-app-0satlm-f01c99-3-148-104-162.traefik.me/agent/AGENTE_ID/scale/read \
     -H "Content-Type: application/json" \
     -d '{"scale_port": "COM1"}'
   ```

## 🔧 Qué Sucede Detrás

1. **POS en nube** llama a tu VPS
2. **VPS** reenvía la petición a tu PC local
3. **Agente local** controla los dispositivos reales
4. **Resultado** vuelve por el mismo camino

## 📊 Endpoints Importantes

### **VPS API:**
- `/agents` - Ver agentes conectados
- `/agent/{id}/print` - Imprimir vía agente
- `/agent/{id}/scale/read` - Leer báscula vía agente

### **Agente Local:**
- Corre en `http://localhost:5001`
- Se registra automáticamente cada 30 segundos

## 🚀 Probar Todo el Sistema

1. **Inicia el agente en tu PC local**
2. **Espera 30 segundos** para que se registre
3. **Verifica agentes** en el VPS
4. **Prueba imprimir** y leer báscula

## ⚡ Ventajas de esta Arquitectura

✅ **Dispositivos locales** accesibles desde nube
✅ **Seguro** - solo tu agente puede controlar tus dispositivos
✅ **Flexible** - múltiples PCs con diferentes dispositivos
✅ **Offline parcial** - dispositivos funcionan localmente

¡Así tu POS en la nube puede imprimir en tu impresora local! 🎯