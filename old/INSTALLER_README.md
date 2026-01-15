# Instalador Agente Local - Opciones

## 🚀 Formas de Instalación

### Opción 1: Instalador Automático Python (Recomendado)
```bash
python install_agent.py
```

### Opción 2: Instalador Batch (Windows tradicional)
```bash
installer.bat
```

### Opción 3: Instalación Manual
```bash
pip install pywin32==311 flask requests pyserial python-escpos
python local_agent.py
```

## 📋 Características del Instalador

✅ **Detección automática de Python**
✅ **Instalación de todas las dependencias**
✅ **Configuración personalizada de URL VPS**
✅ **Creación de accesos directos**
✅ **Inicio automático opcional**
✅ **Prueba de conexión con VPS**

## 🎯 Después de Instalar

1. **Inicia el agente** (automáticamente o con el acceso directo)
2. **Verifica conexión** en tu VPS:
   ```bash
   curl http://appprueba-app-0satlm-f01c99-3-148-104-162.traefik.me/agents
   ```
3. **¡Listo para usar!** Tu POS en la nube podrá controlar tus dispositivos

## 📁 Archivos Creados

- `start_agent.bat` - Script para iniciar el agente
- `agent_config.json` - Configuración personalizada
- `Agente POS.lnk` - Acceso directo en escritorio

## 🔧 Configuración

Edita `agent_config.json` para cambiar:
- URL del VPS
- Opciones del agente

```json
{
  "vps_url": "http://appprueba-app-0satlm-f01c99-3-148-104-162.traefik.me"
}
```

## ⚡ Flujo de Trabajo

```
1. Ejecutas el instalador
2. El agente se inicia automáticamente
3. Se registra con tu VPS
4. Tu POS en la nube ve tus dispositivos locales
5. Puedes imprimir y leer básculas remotamente
```

¡Listo para conectar tus dispositivos locales con tu POS en la nube! 🚀