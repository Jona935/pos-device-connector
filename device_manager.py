import platform
import serial
import time
import logging
import subprocess
import os

# Detectar sistema operativo
IS_WINDOWS = platform.system() == 'Windows'
IS_LINUX = platform.system() == 'Linux'

# Intentar importar ESC/POS según el SO
try:
    if IS_WINDOWS:
        from escpos.printer import Win32Printer
        ESCPOS_AVAILABLE = True
    else:
        from escpos.printer import Dummy  # Para Linux usamos dummy por ahora
        ESCPOS_AVAILABLE = True
except ImportError:
    ESCPOS_AVAILABLE = False

class DeviceManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_printers(self):
        """Obtener lista de impresoras disponibles"""
        try:
            printers = []
            
            if IS_WINDOWS:
                # Método Windows
                import win32print
                printer_enum = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)
                for printer in printer_enum:
                    printer_info = {
                        'name': printer[2],
                        'status': 'Disponible',
                        'type': 'Local'
                    }
                    printers.append(printer_info)
            
            elif IS_LINUX:
                # Método Linux - buscar impresoras CUPS
                try:
                    result = subprocess.run(['lpstat', '-p'], capture_output=True, text=True)
                    if result.returncode == 0:
                        lines = result.stdout.split('\n')
                        for line in lines:
                            if 'printer' in line:
                                printer_name = line.split(':')[1].strip()
                                printer_info = {
                                    'name': printer_name,
                                    'status': 'Disponible',
                                    'type': 'CUPS'
                                }
                                printers.append(printer_info)
                except FileNotFoundError:
                    # lpstat no disponible - imprimir mensaje informativo
                    printers.append({
                        'name': 'Demo Printer (Linux)',
                        'status': 'Simulación',
                        'type': 'Demo'
                    })
            
            return printers
            
        except Exception as e:
            self.logger.error(f"Error obteniendo impresoras: {e}")
            # Siempre devolver al menos una impresora demo
            return [{
                'name': 'Demo Printer',
                'status': 'Simulación',
                'type': 'Demo'
            }]
    
    def get_scales(self):
        """Escanear puertos para encontrar básculas"""
        try:
            available_ports = []
            
            if IS_WINDOWS:
                # Escanear puertos COM en Windows
                for i in range(1, 10):
                    port_name = f'COM{i}'
                    try:
                        ser = serial.Serial(port_name, timeout=1)
                        ser.close()
                        available_ports.append({
                            'port': port_name,
                            'status': 'Disponible',
                            'type': 'Báscula'
                        })
                    except:
                        continue
            
            elif IS_LINUX:
                # Escanear puertos tty en Linux
                for i in range(0, 10):
                    port_name = f'/dev/ttyUSB{i}'
                    if os.path.exists(port_name):
                        available_ports.append({
                            'port': port_name,
                            'status': 'Disponible',
                            'type': 'Báscula'
                        })
                
                # También buscar puertos ACM
                for i in range(0, 10):
                    port_name = f'/dev/ttyACM{i}'
                    if os.path.exists(port_name):
                        available_ports.append({
                            'port': port_name,
                            'status': 'Disponible',
                            'type': 'Báscula'
                        })
            
            return available_ports
            
        except Exception as e:
            self.logger.error(f"Error escaneando puertos: {e}")
            return []
    
    def print_ticket(self, printer_name, content):
        """Imprimir ticket usando método apropiado"""
        try:
            if IS_WINDOWS and ESCPOS_AVAILABLE:
                # Usar ESC/POS en Windows
                printer = Win32Printer(printer_name)
                ticket_content = self._format_ticket(content)
                printer.text(ticket_content)
                printer.cut()
            
            elif IS_LINUX:
                # Usar CUPS en Linux
                ticket_content = self._format_ticket(content)
                try:
                    # Intentar imprimir con lp
                    result = subprocess.run(['lp', '-d', printer_name, '-t', 'Ticket'], 
                                      input=ticket_content, text=True, capture_output=True)
                    if result.returncode == 0:
                        status = 'success'
                    else:
                        status = f'error: {result.stderr}'
                except FileNotFoundError:
                    # lp no disponible, simular
                    status = 'simulated'
            
            else:
                # Simulación para cualquier sistema
                ticket_content = self._format_ticket(content)
                print(f"[SIMULACIÓN] Imprimiendo en {printer_name}:")
                print(ticket_content)
                status = 'simulated'
            
            return {
                'printer': printer_name,
                'status': status,
                'timestamp': time.time()
            }
        except Exception as e:
            self.logger.error(f"Error imprimiendo: {e}")
            return {
                'printer': printer_name,
                'status': 'error',
                'error': str(e)
            }
    
    def read_scale(self, scale_port):
        """Leer peso de báscula por puerto serial"""
        try:
            if IS_WINDOWS:
                # Comunicación serial en Windows
                ser = serial.Serial(scale_port, 9600, timeout=2)
            else:
                # Comunicación serial en Linux
                ser = serial.Serial(scale_port, 9600, timeout=2)
            
            time.sleep(0.5)
            
            # Enviar comando para leer peso
            ser.write(b'P\r\n')
            time.sleep(1)
            
            response = ser.readline().decode('utf-8').strip()
            ser.close()
            
            # Parsear respuesta
            if ',' in response:
                parts = response.split(',')
                if len(parts) >= 3:
                    weight_str = parts[2].strip()
                    try:
                        weight = float(weight_str.split()[0])
                        return {
                            'port': scale_port,
                            'weight': weight,
                            'unit': 'kg',
                            'timestamp': time.time()
                        }
                    except ValueError:
                        pass
            
            # Simulación si no se puede parsear
            return {
                'port': scale_port,
                'weight': 1.23,
                'unit': 'kg',
                'timestamp': time.time(),
                'note': 'simulated'
            }
            
        except Exception as e:
            self.logger.error(f"Error leyendo báscula: {e}")
            return {
                'port': scale_port,
                'weight': 0.0,
                'unit': 'kg',
                'error': str(e)
            }
    
    def _format_ticket(self, content):
        """Formatear contenido para ticket"""
        lines = []
        
        # Encabezado
        lines.append('\n' + '='.center(32) + '\n')
        lines.append('TIQUETA DE VENTA\n'.center(32) + '\n')
        lines.append('-'.center(32) + '\n')
        
        # Contenido
        if isinstance(content, dict):
            if 'items' in content:
                for item in content['items']:
                    lines.append(f"{item['name'][:20]:<20} ${item['price']:>8.2f}\n")
                    if 'qty' in item:
                        lines.append(f"  Cantidad: {item['qty']}\n")
            
            if 'total' in content:
                lines.append('-'.center(32) + '\n')
                lines.append(f"TOTAL: ${content['total']:>25.2f}\n")
        
        # Pie
        lines.append('-'.center(32) + '\n')
        lines.append('Gracias por su compra\n'.center(32) + '\n')
        lines.append('\n\n\n')
        
        return ''.join(lines)