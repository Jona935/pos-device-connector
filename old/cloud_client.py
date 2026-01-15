import requests
import json
import time
import logging

class CloudClient:
    def __init__(self):
        self.cloud_url = None
        self.api_key = None
        self.logger = logging.getLogger(__name__)
        self.connected = False
    
    def connect(self, cloud_url, api_key):
        """Conectar con sistema POS en la nube"""
        try:
            self.cloud_url = cloud_url.rstrip('/')
            self.api_key = api_key
            
            # Probar conexión
            test_url = f"{self.cloud_url}/api/health"
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(test_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                self.connected = True
                return {
                    'status': 'connected',
                    'cloud_url': self.cloud_url,
                    'timestamp': time.time()
                }
            else:
                return {
                    'status': 'error',
                    'error': f'Status code: {response.status_code}'
                }
                
        except Exception as e:
            self.logger.error(f"Error conectando a nube: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def notify_print_completed(self, print_result):
        """Notificar al POS que se completó la impresión"""
        if not self.connected:
            return False
        
        try:
            url = f"{self.cloud_url}/api/device/print/completed"
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'device_type': 'printer',
                'result': print_result,
                'timestamp': time.time()
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=5)
            return response.status_code == 200
            
        except Exception as e:
            self.logger.error(f"Error notificando impresión: {e}")
            return False
    
    def send_weight_reading(self, weight_data):
        """Enviar lectura de peso al POS"""
        if not self.connected:
            return False
        
        try:
            url = f"{self.cloud_url}/api/device/scale/reading"
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'device_type': 'scale',
                'data': weight_data,
                'timestamp': time.time()
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=5)
            return response.status_code == 200
            
        except Exception as e:
            self.logger.error(f"Error enviando peso: {e}")
            return False
    
    def register_device(self, device_info):
        """Registrar dispositivo en el sistema POS"""
        if not self.connected:
            return False
        
        try:
            url = f"{self.cloud_url}/api/device/register"
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'device_info': device_info,
                'local_ip': self._get_local_ip(),
                'timestamp': time.time()
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=5)
            return response.status_code == 200
            
        except Exception as e:
            self.logger.error(f"Error registrando dispositivo: {e}")
            return False
    
    def _get_local_ip(self):
        """Obtener IP local"""
        try:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"