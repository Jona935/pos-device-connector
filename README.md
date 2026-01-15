# POS Device Connector - Organizado

## 📁 Estructura Clara

```
pos-device-connector/
├── 🖥️ app_ultralight.py          # API del servidor VPS
├── 🖥️ Dockerfile.ultralight         # Imagen Docker para VPS
├── 🖥️ requirements.minimal.txt       # Dependencias VPS
├── 🖥️ deploy_vps.sh                # Script despliegue VPS
├── 💻 local_agent_simple.py         # Agente PC Local
├── 💻 install_agent.py              # Instalador PC
├── 💻 installer.bat                 # Instalador batch
├── 💻 start_agent.bat              # Script inicio PC
├── 💻 agent_config.json             # Configuración agente
├── 💻 requirements.txt               # Dependencias PC
├── 📚 shared/                      # Documentación
├── 📚 docs/                         # Documentos técnicos
└── 📦 old/                          # Archivos antiguos
```

## 🚀 Uso Rápido

### **VPS (Ubuntu)**:
```bash
# Desplegar API
chmod +x deploy_vps.sh
./deploy_vps.sh
```

### **PC Local (Windows)**:
```bash
# Instalar y ejecutar agente
python install_agent.py
python start_agent.bat
```

## 🌐 Conexión

```
PC Local (Agent)  ←→  VPS (Server)  ←→  POS Nube
  :5001               :5000           :8000
```

## 📋 Archivos por Sistema

| Sistema | Archivos Clave | Función |
|---------|----------------|----------|
| VPS | app_ultralight.py | API REST |
| PC | local_agent_simple.py | Control dispositivos |
| Ambos | agent_config.json | Configuración |
| Documentación | README.md | Guía completa |

## 🎯 Flujo Trabajo

1. **VPS**: Inicia API en puerto 5000
2. **PC**: Inicia agente en puerto 5001
3. **Registro**: Agente se registra cada 30s
4. **Control**: POS nube → VPS → Agente → Dispositivos
5. **Respuesta**: Dispositivos → Agente → VPS → POS nube

¡Sistema POS Device Connector completo y organizado! 🚀