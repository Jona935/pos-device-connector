"""
Agent para PC Local - Conecta dispositivos locales con VPS
"""
import requests
import flask
from flask import Flask, request, jsonify
import threading
import time
import platform
import serial
import logging

# Detectar sistema operativo
IS_WINDOWS = platform.system() == 'Windows'

if IS_WINDOWS:
    import win32print
    try:
        from escpos.printer import Win32RawPrinter
        ESCPOS_AVAILABLE = True
    except ImportError:
        try:
            from escpos.printer import Win32Printer
            ESCPOS_AVAILABLE = True
        except ImportError:
            ESCPOS_AVAILABLE = False
else:
    ESCPOS_AVAILABLE = False

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Agent Flask para PC local
agent_app = Flask(__name__)
agent_app.config['SECRET_KEY'] = 'local-agent-secret'

# Configuración del VPS
VPS_URL = "http://appprueba-app-0satlm-f01c99-3-148-104-162.traefik.me"
AGENT_ID = f"agent-{platform.node()}-{int(time.time())}"

class LocalDeviceManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_printers(self):
        """Obtener impresoras locales"""
        try:
            if IS_WINDOWS:
                printers = []
                printer_enum = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)
                for printer in printer_enum:
                    printer_info = {
                        'name': printer[2],
                        'status': 'Disponible',
                        'type': 'Local Windows'
                    }
                    printers.append(printer_info)
                return printers
            else:
                return [{'name': 'Demo Printer', 'status': 'Demo', 'type': 'Linux'}]
        except Exception as e:
            logger.error(f"Error obteniendo impresoras: {e}")
            return []
    
    def print_ticket(self, printer_name, content):
        """Imprimir ticket localmente"""
        try:
            if IS_WINDOWS and ESCPOS_AVAILABLE:
                # Intentar con Win32RawPrinter primero
                try:
                    from escpos.printer import Win32RawPrinter
                    printer = Win32RawPrinter(printer_name)
                except:
                    from escpos.printer import Win32Printer
                    printer = Win32Printer(printer_name)
                
                ticket_content = self._format_ticket(content)
                printer.text(ticket_content)
                printer.cut()
                return {'status': 'success', 'printer': printer_name}
            else:
                # Simulación o método alternativo
                logger.info(f"[SIMULACIÓN] Imprimiendo en {printer_name}")
                
                # Método alternativo con win32print directo
                if IS_WINDOWS:
                    try:
                        import win32print
                        import win32api
                        
                        hPrinter = win32print.OpenPrinter(printer_name)
                        ticket_content = self._format_ticket(content)
                        win32print.StartDocPrinter(hPrinter, 1, ("Ticket", None, "RAW"))
                        win32print.StartPagePrinter(hPrinter)
                        win32print.WritePrinter(hPrinter, ticket_content.encode('utf-8'))
                        win32print.EndPagePrinter(hPrinter)
                        win32print.EndDocPrinter(hPrinter)
                        win32print.ClosePrinter(hPrinter)
                        return {'status': 'success', 'printer': printer_name}
                    except:
                        pass
                
                return {'status': 'simulated', 'printer': printer_name}
        except Exception as e:
            logger.error(f"Error imprimiendo: {e}")
            return {'status': 'error', 'error': str(e)}
    
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
            if 'total' in content:
                lines.append('-'.center(32) + '\n')
                lines.append(f"TOTAL: ${content['total']:>25.2f}\n")
        
        lines.append('Gracias por su compra\n'.center(32) + '\n')
        return ''.join(lines)

# Instancia del gestor de dispositivos
device_manager = LocalDeviceManager()

@agent_app.route('/')
def agent_index():
    return jsonify({
        'agent_id': AGENT_ID,
        'status': 'running',
        'platform': platform.system()
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
    
    result = device_manager.print_ticket(printer_name, content)
    
    # Notificar al VPS que se imprimió
    try:
        requests.post(f"{VPS_URL}/agent/print-completed", json={
            'agent_id': AGENT_ID,
            'result': result
        }, timeout=5)
    except:
        pass
    
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
    while True:
        try:
            devices_info = {
                'agent_id': AGENT_ID,
                'platform': platform.system(),
                'printers': device_manager.get_printers(),
                'scales': device_manager.scan_scales(),
                'timestamp': time.time()
            }
            
            response = requests.post(
                f"{VPS_URL}/agent/register", 
                json=devices_info, 
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"✅ Agente registrado: {AGENT_ID}")
            else:
                logger.warning(f"❌ Error registrando agente: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error conexión VPS: {e}")
        
        time.sleep(30)  # Registrar cada 30 segundos

if __name__ == '__main__':
    print("🚀 Iniciando Agente Local para POS")
    print(f"📍 Agent ID: {AGENT_ID}")
    print(f"🌐 VPS URL: {VPS_URL}")
    print("📊 Este agente expone tus dispositivos locales al VPS")
    
    # Iniciar registro en background
    register_thread = threading.Thread(target=register_with_vps, daemon=True)
    register_thread.start()
    
    # Iniciar servidor del agente
    agent_app.run(host='0.0.0.0', port=5001, debug=False)