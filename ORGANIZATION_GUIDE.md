# Estructura de Archivos - Organización Clara

## 📁 Estructura Recomendada

```
pos-device-connector/
├── 🖥️ vps/                          # Para el servidor VPS
│   ├── Dockerfile.ultralight
│   ├── app_ultralight.py
│   ├── requirements.minimal.txt
│   └── deploy_vps.sh
│
├── 💻 pc-local/                      # Para la PC local (Windows)
│   ├── local_agent_simple.py
│   ├── install_agent.py
│   ├── installer.bat
│   ├── start_agent.bat
│   ├── requirements.txt
│   └── agent_config.json
│
├── 📚 shared/                        # Archivos compartidos
│   ├── README.md
│   ├── LOCAL_VPS_GUIDE.md
│   └── docs/
│
└── 🔄 old/                          # Versión antigua (para referencia)
    ├── app.py
    ├── device_manager.py
    ├── cloud_client.py
    └── ...
```

## 🎯 ¿Qué va dónde?

### **🖥️ VPS (Ubuntu) - Solo estos archivos:**
- `Dockerfile.ultralight` - Para construir imagen Docker
- `app_ultralight.py` - API del servidor
- `requirements.minimal.txt` - Dependencias mínimas
- `deploy_vps.sh` - Script de despliegue

### **💻 PC Local (Windows) - Solo estos archivos:**
- `local_agent_simple.py` - Agente que controla dispositivos
- `install_agent.py` - Instalador automático
- `installer.bat` - Instalador batch
- `start_agent.bat` - Script para iniciar
- `requirements.txt` - Todas las dependencias Windows
- `agent_config.json` - Configuración local

### **📚 Shared - Documentación:**
- `README.md` - General
- `LOCAL_VPS_GUIDE.md` - Guía de uso
- `docs/` - Documentación detallada

## 🚀 Flujo de Trabajo Limpio

### **1. Configurar VPS:**
```bash
# En VPS
cd /home/ubuntu/pos-device-connector/vps
docker build -f Dockerfile.ultralight -t pos-connector .
docker run -d --name pos-connector -p 5000:5000 pos-connector
```

### **2. Configurar PC Local:**
```bash
# En PC Windows
cd C:\pos-device-connector\pc-local
python install_agent.py
```

### **3. Comunicación:**
```
PC Local (pc-local/)  ←→  VPS (vps/)  ←→  POS Nube
```

## 📋 Ventajas de esta organización:

✅ **Sin confusión** - Cada sistema tiene sus archivos  
✅ **Fácil mantenimiento** - Sabes qué editar dónde  
✅ **Despliegue limpio** - Solo copias lo necesario  
✅ **Escalable** - Puedes añadir más agentes fácilmente  
✅ **Seguro** - Separación de responsabilidades  

## 🔄 Para reorganizar:

```bash
# Crear estructura
mkdir -p vps pc-local shared old docs

# Mover archivos VPS
mv Dockerfile.ultralight app_ultralight.py requirements.minimal.txt vps/

# Mover archivos PC Local
mv local_agent_simple.py install_agent.py installer.bat start_agent.bat requirements.txt pc-local/

# Mover documentación
mv README.md LOCAL_VPS_GUIDE.md shared/

# Mover archivos viejos
mv app.py device_manager.py cloud_client.py simulator.py old/
```

**¿Quieres que reorganice los archivos así?** 🎯