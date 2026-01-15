#!/usr/bin/env python3
"""
Script de prueba para despliegue en VPS con Dockploy
"""

import requests
import json
import time
import sys
from datetime import datetime

class VPSTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.test_results = []
        
    def log_test(self, test_name, success, message, response_time=0.0):
        """Registrar resultado de prueba"""
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'response_time': response_time,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "OK" if success else "FAIL"
        print(f"{status} {test_name}: {message} ({response_time:.2f}s)")
        
    def test_connection(self):
        """Probar conexión básica"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    "Conexión Básica", 
                    True, 
                    f"API funcionando (v{data.get('version', 'unknown')})",
                    response_time
                )
                return True
            else:
                self.log_test(
                    "Conexión Básica", 
                    False, 
                    f"Status code: {response.status_code}",
                    response_time
                )
                return False
        except Exception as e:
            self.log_test("Conexión Básica", False, f"Error: {str(e)}")
            return False
    
    def test_health_check(self):
        """Probar health check"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/health", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                status = data.get('status', 'unknown')
                resources = data.get('resources', {})
                
                self.log_test(
                    "Health Check", 
                    True, 
                    f"Estado: {status}, CPU: {resources.get('cpu_percent', 0):.1f}%",
                    response_time
                )
                return True
            else:
                self.log_test(
                    "Health Check", 
                    False, 
                    f"Status code: {response.status_code}",
                    response_time
                )
                return False
        except Exception as e:
            self.log_test("Health Check", False, f"Error: {str(e)}")
            return False
    
    def test_metrics(self):
        """Probar endpoint de métricas"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/metrics", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    "Métricas", 
                    True, 
                    f"Métricas disponibles: {len(data)} endpoints",
                    response_time
                )
                return True
            elif response.status_code == 404:
                self.log_test(
                    "Métricas", 
                    True, 
                    "Métricas deshabilitadas (normal)",
                    response_time
                )
                return True
            else:
                self.log_test(
                    "Métricas", 
                    False, 
                    f"Status code: {response.status_code}",
                    response_time
                )
                return False
        except Exception as e:
            self.log_test("Métricas", False, f"Error: {str(e)}")
            return False
    
    def test_device_detection(self):
        """Probar detección de dispositivos"""
        try:
            # Probar impresoras
            start_time = time.time()
            response = requests.get(f"{self.base_url}/devices/printers", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                printers_count = data.get('count', 0)
                self.log_test(
                    "Detección Impresoras", 
                    True, 
                    f"{printers_count} impresoras encontradas",
                    response_time
                )
            else:
                self.log_test(
                    "Detección Impresoras", 
                    False, 
                    f"Status code: {response.status_code}",
                    response_time
                )
            
            # Probar básculas
            start_time = time.time()
            response = requests.get(f"{self.base_url}/devices/scales", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                scales_count = data.get('count', 0)
                self.log_test(
                    "Detección Básculas", 
                    True, 
                    f"{scales_count} básculas encontradas",
                    response_time
                )
            else:
                self.log_test(
                    "Detección Básculas", 
                    False, 
                    f"Status code: {response.status_code}",
                    response_time
                )
                
        except Exception as e:
            self.log_test("Detección Dispositivos", False, f"Error: {str(e)}")
    
    def test_cloud_connection(self):
        """Probar conexión con nube (simulada)"""
        try:
            # Intentar conectar con simulador local
            test_data = {
                "cloud_url": "http://localhost:5001",
                "api_key": "test-api-key-vps"
            }
            
            start_time = time.time()
            response = requests.post(
                f"{self.base_url}/cloud/connect",
                json=test_data,
                timeout=10
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    "Conexión Nube", 
                    True, 
                    f"Conexión establecida: {data.get('result', {}).get('status', 'unknown')}",
                    response_time
                )
            else:
                self.log_test(
                    "Conexión Nube", 
                    False, 
                    f"Status code: {response.status_code}",
                    response_time
                )
        except Exception as e:
            self.log_test("Conexión Nube", False, f"Error: {str(e)}")
    
    def test_performance(self):
        """Probar rendimiento bajo carga"""
        try:
            print("\nProbando rendimiento (10 peticiones concurrentes)...")
            
            import threading
            import queue
            
            results = queue.Queue()
            
            def make_request():
                try:
                    start_time = time.time()
                    response = requests.get(f"{self.base_url}/health", timeout=5)
                    response_time = time.time() - start_time
                    results.put({
                        'success': response.status_code == 200,
                        'response_time': response_time
                    })
                except:
                    results.put({'success': False, 'response_time': 0})
            
            # Lanzar 10 peticiones concurrentes
            threads = []
            for _ in range(10):
                thread = threading.Thread(target=make_request)
                threads.append(thread)
                thread.start()
            
            # Esperar a que terminen
            for thread in threads:
                thread.join()
            
            # Analizar resultados
            successful_requests = 0
            total_response_time = 0
            
            while not results.empty():
                result = results.get()
                if result['success']:
                    successful_requests += 1
                    total_response_time += result['response_time']
            
            success_rate = (successful_requests / 10) * 100
            avg_response_time = total_response_time / successful_requests if successful_requests > 0 else 0
            
            self.log_test(
                "Rendimiento", 
                success_rate >= 80, 
                f"Tasa éxito: {success_rate:.0f}%, Tiempo promedio: {avg_response_time:.3f}s"
            )
            
        except Exception as e:
            self.log_test("Rendimiento", False, f"Error: {str(e)}")
    
    def run_all_tests(self):
        """Ejecutar todas las pruebas"""
        print(f"Iniciando pruebas VPS/Dockploy - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"URL objetivo: {self.base_url}")
        print("=" * 60)
        
        # Ejecutar pruebas en orden
        tests = [
            self.test_connection,
            self.test_health_check,
            self.test_metrics,
            self.test_device_detection,
            self.test_cloud_connection,
            self.test_performance
        ]
        
        for test in tests:
            test()
            time.sleep(1)  # Pequeña pausa entre pruebas
        
        # Resumen final
        self.print_summary()
    
    def print_summary(self):
        """Imprimir resumen de pruebas"""
        print("\n" + "=" * 60)
        print("RESUMEN DE PRUEBAS")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for result in self.test_results if result['success'])
        success_rate = (successful_tests / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"Total pruebas: {total_tests}")
        print(f"Exitosas: {successful_tests}")
        print(f"Tasa éxito: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("Despliegue listo para producción!")
        elif success_rate >= 60:
            print("Despliegue funcional pero necesita revision")
        else:
            print("Despliegue con problemas criticos")
        
        # Detalles de pruebas fallidas
        failed_tests = [result for result in self.test_results if not result['success']]
        if failed_tests:
            print("\nPruebas fallidas:")
            for test in failed_tests:
                print(f"   - {test['test']}: {test['message']}")
        
        # Guardar resultados en archivo
        self.save_results()
    
    def save_results(self):
        """Guardar resultados en archivo JSON"""
        try:
            filename = f"vps_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump({
                    'summary': {
                        'total_tests': len(self.test_results),
                        'successful_tests': sum(1 for r in self.test_results if r['success']),
                        'timestamp': datetime.now().isoformat()
                    },
                    'results': self.test_results
                }, f, indent=2)
            print(f"\nResultados guardados en: {filename}")
        except Exception as e:
            print(f"\nNo se pudieron guardar resultados: {e}")

if __name__ == "__main__":
    # Permitir URL personalizada como argumento
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    
    tester = VPSTester(base_url)
    tester.run_all_tests()