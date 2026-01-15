"""
Agente para PC Local - Versión final corregida
"""
import requests
import flask
from flask import Flask, request, jsonify
import threading
import time
import platform
import serial
import json

# Detectar sistema operativo
IS_WINDOWS = platform.system() == 'Windows'

# Variables globales para manejar importaciones
WIN32_AVAILABLE = False
win32print = None
win32api = None

# Intentar importar librerías Windows
try:
    import win32print
    import win32api
    WIN32_AVAILABLE = True
    win32print = win32print  # Asignar a variable global
    win32api = win32api    # Asignar a variable global
except ImportError as e:
    WIN32_AVAILABLE = False
    print(f"⚠️ win32print no disponible: {e}")

# Configurar logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Leer configuración
try:
    with open('agent_config.json', 'r') as f:
        config = json.load(f)
        VPS_URL = config['vps_url']
except:
    VPS_URL = "http://18.222.185.0:5000"

AGENT_ID = f"agent-{platform.node()}-{int(time.time())}"

# Agent Flask para PC local
agent_app = Flask(__name__)
agent_app.config['SECRET_KEY'] = 'local-agent-secret'

class LocalDeviceManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_printers(self):
        """Obtener impresoras locales"""
        try:
            printers = []
            
            if IS_WINDOWS and WIN32_AVAILABLE and win32print:
                printer_enum = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)
                for printer in printer_enum:
                    printer_info = {
                        'name': printer[2],
                        'status': 'Disponible',
                        'type': 'Local Windows'
                    }
                    printers.append(printer_info)
            else:
                printers.append({'name': 'Demo Printer', 'status': 'Demo', 'type': 'Simulación'})
            
            return printers
            
        except Exception as e:
            self.logger.error(f"Error obteniendo impresoras: {e}")
            return [{'name': 'Demo Printer', 'status': 'Demo', 'type': 'Simulación'}]
    
    def print_ticket(self, printer_name, content):
        """Imprimir ticket localmente - versión final"""
        try:
            self.logger.info(f"🖨️ Intentando imprimir en: {printer_name}")
            
            if IS_WINDOWS and WIN32_AVAILABLE and win32print:
                # Usar método directo con win32print
                ticket_content = self._format_ticket(content)
                self.logger.info("✅ Contenido del ticket generado")
                self.logger.info(f"📄 Longitud: {len(ticket_content)} caracteres")
                
                try:
                    self.logger.info(f"🔧 Abriendo impresora: {printer_name}")
                    hPrinter = win32print.OpenPrinter(printer_name)
                    
                    self.logger.info("📋 Iniciando documento RAW")
                    doc_info = ("Ticket", "RAW", "RAW")
                    win32print.StartDocPrinter(hPrinter, 1, doc_info)
                    
                    self.logger.info("📄 Iniciando página")
                    win32print.StartPagePrinter(hPrinter)
                    
                    self.logger.info("🖨️ Enviando a impresora")
                    data = ticket_content.encode('utf-8')
                    win32print.WritePrinter(hPrinter, data)
                    
                    self.logger.info("✅ Finalizando página")
                    win32print.EndPagePrinter(hPrinter)
                    
                    self.logger.info("📋 Finalizando documento")
                    win32print.EndDocPrinter(hPrinter)
                    
                    self.logger.info("🔒 Cerrando impresora")
                    win32print.ClosePrinter(hPrinter)
                    
                    self.logger.info("🎉 ¡Impresión REAL completada exitosamente!")
                    return {'status': 'success', 'printer': printer_name, 'method': 'real_print'}
                    
                except Exception as print_error:
                    self.logger.error(f"❌ Error en impresión real: {print_error}")
                    return {'status': 'error', 'printer': printer_name, 'error': str(print_error)}
                    
            else:
                self.logger.warning("🖥️ win32print no disponible, usando simulación")
                return {'status': 'simulated', 'printer': printer_name}
                
        except Exception as e:
            self.logger.error(f"❌ Error general imprimiendo: {e}")
            return {'status': 'error', 'printer': printer_name, 'error': str(e)}
    
    def scan_scales(self):
        """Escanear básculas locales"""
        scales = []
        if IS_WINDOWS:
            for i in range(1, 10):
                port_name = f'COM{i}'
                try:
                    ser = serial.Serial(port_name, timeout=1)
                    ser.close()
                    scales.append({'port': port_name, 'status': 'Disponible'})
                except:
                    continue
        return scales
    
    def read_scale(self, port):
        """Leer báscula local"""
        try:
            ser = serial.Serial(port, 9600, timeout=2)
            time.sleep(0.5)
            ser.write(b'P\r\n')
            time.sleep(1)
            response = ser.readline().decode('utf-8').strip()
            ser.close()
            
            if ',' in response:
                parts = response.split(',')
                if len(parts) >= 3:
                    weight = float(parts[2].strip().split()[0])
                    return {'port': port, 'weight': weight, 'unit': 'kg'}
            
            return {'port': port, 'weight': 1.23, 'unit': 'kg', 'simulated': True}
            
        except Exception as e:
            return {'port': port, 'error': str(e)}
    
    def _format_ticket(self, content):
        """Formatear ticket"""
        lines = []
        lines.append('\n' + '='.center(32) + '\n')
        lines.append('TIQUETA DE VENTA\n'.center(32) + '\n')
        lines.append('-'.center(32) + '\n')
        
        if isinstance(content, dict):
            if 'items' in content:
                for item in content['items']:
                    lines.append(f"{item['name'][:20]:<20} ${item['price']:>8.2f}\n")
                    if 'qty' in item:
                        lines.append(f"  Cantidad: {item['qty']}\n")
            if 'total' in content:
                lines.append('-'.center(32) + '\n')
                lines.append(f"TOTAL: ${content['total']:>25.2f}\n")
        
        lines.append('-'.center(32) + '\n')
        lines.append('Gracias por su compra\n'.center(32) + '\n')
        return ''.join(lines)

# Instancia del gestor de dispositivos
device_manager = LocalDeviceManager()

@agent_app.route('/')
def agent_index():
    return jsonify({
        'agent_id': AGENT_ID,
        'status': 'running',
        'platform': platform.system(),
        'win32_available': WIN32_AVAILABLE
    })

@agent_app.route('/devices/printers', methods=['GET'])
def agent_get_printers():
    printers = device_manager.get_printers()
    return jsonify({
        'success': True,
        'printers': printers,
        'agent_id': AGENT_ID
    })

@agent_app.route('/print', methods=['POST'])
def agent_print():
    data = request.json
    printer_name = data.get('printer_name')
    content = data.get('content')
    
    logger.info(f"🖨️ Petición de impresión recibida: {printer_name}")
    result = device_manager.print_ticket(printer_name, content)
    
    # Notificar al VPS que se imprimió
    try:
        requests.post(f"{VPS_URL}/agent/print-completed", json={
            'agent_id': AGENT_ID,
            'result': result
        }, timeout=5)
    except Exception as e:
        logger.error(f"Error notificando VPS: {e}")
    
    return jsonify({
        'success': True,
        'result': result
    })

@agent_app.route('/devices/scales', methods=['GET'])
def agent_get_scales():
    scales = device_manager.scan_scales()
    return jsonify({
        'success': True,
        'scales': scales,
        'agent_id': AGENT_ID
    })

@agent_app.route('/scale/read', methods=['POST'])
def agent_read_scale():
    data = request.json
    scale_port = data.get('scale_port')
    
    weight = device_manager.read_scale(scale_port)
    
    # Notificar al VPS la lectura
    try:
        requests.post(f"{VPS_URL}/agent/scale-reading", json={
            'agent_id': AGENT_ID,
            'reading': weight
        }, timeout=5)
    except:
        pass
    
    return jsonify({
        'success': True,
        'weight': weight
    })

def register_with_vps():
    """Registrar este agente con el VPS"""
    logger.info("🔄 Iniciando registro con VPS...")
    while True:
        try:
            devices_info = {
                'agent_id': AGENT_ID,
                'platform': platform.system(),
                'printers': device_manager.get_printers(),
                'scales': device_manager.scan_scales(),
                'timestamp': time.time(),
                'win32_available': WIN32_AVAILABLE
            }
            
            response = requests.post(
                f"{VPS_URL}/agent/register", 
                json=devices_info, 
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"✅ Agente registrado exitosamente: {AGENT_ID}")
            else:
                logger.warning(f"⚠️ Error registrando agente: {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Error conexión VPS: {e}")
        
        time.sleep(30)  # Registrar cada 30 segundos

if __name__ == '__main__':
    print("🚀 Iniciando Agente Local CORREGIDO para POS")
    print(f"📍 Agent ID: {AGENT_ID}")
    print(f"🌐 VPS URL: {VPS_URL}")
    print(f"🖥️ Sistema: {platform.system()}")
    print(f"📦 win32print disponible: {WIN32_AVAILABLE}")
    print("📊 Este agente expone tus dispositivos locales al VPS")
    print("🔧 Estado de librerías:")
    if WIN32_AVAILABLE:
        print("   ✅ win32print: CARGADA")
        print("   ✅ win32api: CARGADA")
    else:
        print("   ❌ win32print: NO DISPONIBLE")
        print("   ⚠️ Solo modo simulación")
    
    # Iniciar registro en background
    register_thread = threading.Thread(target=register_with_vps, daemon=True)
    register_thread.start()
    
    # Iniciar servidor del agente
    agent_app.run(host='0.0.0.0', port=5001, debug=False)