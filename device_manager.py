import win32print
import serial
import time
import logging

# Intentar importar ESC/POS, si no está disponible usar método alternativo
try:
    from escpos.printer import Win32Printer
    ESCPOS_AVAILABLE = True
except ImportError:
    ESCPOS_AVAILABLE = False

class DeviceManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_printers(self):
        """Obtener lista de impresoras disponibles en Windows"""
        try:
            printers = []
            printer_enum = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)
            
            for printer in printer_enum:
                printer_info = {
                    'name': printer[2],  # Nombre de la impresora
                    'status': 'Disponible',
                    'type': 'Local'
                }
                printers.append(printer_info)
            
            return printers
        except Exception as e:
            self.logger.error(f"Error obteniendo impresoras: {e}")
            return []
    
    def get_scales(self):
        """Escanear puertos COM para encontrar básculas"""
        try:
            available_ports = []
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
            return available_ports
        except Exception as e:
            self.logger.error(f"Error escaneando puertos: {e}")
            return []
    
    def print_ticket(self, printer_name, content):
        """Imprimir ticket usando ESC/POS o método alternativo"""
        try:
            if ESCPOS_AVAILABLE:
                # Usar ESC/POS si está disponible
                printer = Win32Printer(printer_name)
                ticket_content = self._format_ticket(content)
                printer.text(ticket_content)
                printer.cut()
            else:
                # Método alternativo usando win32print directamente
                import win32print
                import win32api
                
                hPrinter = win32print.OpenPrinter(printer_name)
                try:
                    ticket_content = self._format_ticket(content)
                    win32print.StartDocPrinter(hPrinter, 1, ("Ticket", None, "RAW"))
                    win32print.StartPagePrinter(hPrinter)
                    win32print.WritePrinter(hPrinter, ticket_content.encode('utf-8'))
                    win32print.EndPagePrinter(hPrinter)
                    win32print.EndDocPrinter(hPrinter)
                finally:
                    win32print.ClosePrinter(hPrinter)
            
            return {
                'printer': printer_name,
                'status': 'success',
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
            ser = serial.Serial(scale_port, 9600, timeout=2)
            time.sleep(0.5)
            
            # Enviar comando para leer peso (varía por fabricante)
            ser.write(b'P\r\n')
            time.sleep(1)
            
            response = ser.readline().decode('utf-8').strip()
            ser.close()
            
            # Parsear respuesta (formato típico: "ST,GS,  1.23 kg")
            if ',' in response:
                parts = response.split(',')
                if len(parts) >= 3:
                    weight_str = parts[2].strip()
                    weight = float(weight_str.split()[0])
                    return {
                        'port': scale_port,
                        'weight': weight,
                        'unit': 'kg',
                        'timestamp': time.time()
                    }
            
            return {
                'port': scale_port,
                'error': 'No se pudo parsear respuesta',
                'raw_response': response
            }
            
        except Exception as e:
            self.logger.error(f"Error leyendo báscula: {e}")
            return {
                'port': scale_port,
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