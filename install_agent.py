"""
Instalador Automático para Agente Local POS Device Connector
"""
import os
import sys
import subprocess
import requests
import json
from pathlib import Path

class AgentInstaller:
    def __init__(self):
        self.vps_url = "http://appprueba-app-0satlm-f01c99-3-148-104-162.traefik.me"
        self.required_packages = [
            'pywin32==311',
            'flask',
            'requests', 
            'pyserial',
            'python-escpos'
        ]
    
    def print_banner(self):
        print("=" * 65)
        print("     INSTALADOR AUTOMÁTICO AGENTE LOCAL POS")
        print("     Conecta dispositivos locales con POS en la nube")
        print("=" * 65)
        print()
    
    def check_python(self):
        """Verificar instalación de Python"""
        print("🐍 [1/6] Verificando Python...")
        try:
            version = sys.version_info
            if version.major >= 3 and version.minor >= 8:
                print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
                return True
            else:
                print(f"❌ Python {version.major}.{version.minor} encontrado, se requiere 3.8+")
                print("Por favor instale Python 3.8 o superior")
                input("Presione Enter para salir...")
                return False
        except:
            print("❌ Python no encontrado")
            print("Descargando Python...")
            try:
                import webbrowser
                webbrowser.open("https://www.python.org/downloads/")
                print("Abriendo página de descargas de Python...")
                input("Presione Enter después de instalar Python...")
                return False
            except:
                print("Visite https://www.python.org/downloads/ para instalar Python")
                input("Presione Enter para salir...")
                return False
    
    def install_packages(self):
        """Instalar paquetes requeridos"""
        print("\n📦 [2/6] Instalando paquetes Python...")
        
        for package in self.required_packages:
            try:
                print(f"   Instalando {package}...")
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", package],
                    capture_output=True, text=True
                )
                
                if result.returncode == 0:
                    print(f"   ✅ {package} instalado")
                else:
                    print(f"   ⚠️  Error instalando {package}")
                    print(f"      {result.stderr}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
    
    def configure_vps_url(self):
        """Configurar URL del VPS"""
        print(f"\n🌐 [3/6] Configurando URL del VPS...")
        print(f"URL por defecto: {self.vps_url}")
        
        user_url = input(f"Ingrese URL del VPS (Enter para usar default): ").strip()
        if user_url:
            self.vps_url = user_url
        
        print(f"✅ URL configurada: {self.vps_url}")
        
        # Guardar configuración
        config = {'vps_url': self.vps_url}
        with open('agent_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        print("✅ Configuración guardada")
    
    def create_start_script(self):
        """Crear script de inicio"""
        print("\n🚀 [4/6] Creando script de inicio...")
        
        script_content = f'''@echo off
title Agente Local POS Device Connector
color 0B

echo ╔══════════════════════════════════════════════════════════════╗
echo ║          AGENTE LOCAL POS DEVICE CONNECTOR                      ║
echo ║                                                              ║
echo ║  Conectando dispositivos locales con POS en la nube...           ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo URL VPS: {self.vps_url}
echo Puerto Agente: 5001
echo.
echo Iniciando agente...
python local_agent.py
pause
'''
        
        with open('start_agent.bat', 'w') as f:
            f.write(script_content)
        
        print("✅ start_agent.bat creado")
    
    def create_desktop_shortcut(self):
        """Crear acceso directo en el escritorio"""
        print("\n🖥️  [5/6] Creando acceso directo...")
        
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            path = os.path.join(desktop, "Agente POS.lnk")
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = os.path.abspath('start_agent.bat')
            shortcut.WorkingDirectory = os.path.abspath('.')
            shortcut.IconLocation = 'python.exe'
            shortcut.save()
            
            print("✅ Acceso directo creado en escritorio")
        except ImportError:
            print("⚠️  Creando acceso directo alternativo...")
            self.create_alt_shortcut()
        except Exception as e:
            print(f"⚠️  Error creando acceso directo: {e}")
            self.create_alt_shortcut()
    
    def create_alt_shortcut(self):
        """Crear acceso directo alternativo"""
        import shutil
        desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
        if not os.path.exists(desktop):
            desktop = os.path.expanduser('~')
        
        try:
            shutil.copy('start_agent.bat', os.path.join(desktop, 'Iniciar Agente POS.bat'))
            print("✅ Script copiado al escritorio")
        except:
            print("⚠️  No se pudo crear acceso directo")
    
    def setup_autostart(self):
        """Configurar inicio automático"""
        print("\n🔄 [6/6] Configurando inicio automático...")
        
        auto_start = input("¿Iniciar agente automáticamente con Windows? (S/N): ").strip().upper()
        
        if auto_start == 'S':
            try:
                import winshell
                startup = winshell.startup()
                path = os.path.join(startup, "Agente POS.lnk")
                
                from win32com.client import Dispatch
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(path)
                shortcut.Targetpath = os.path.abspath('start_agent.bat')
                shortcut.WorkingDirectory = os.path.abspath('.')
                shortcut.save()
                
                print("✅ Inicio automático configurado")
            except:
                # Método alternativo
                import shutil
                startup_path = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
                if not os.path.exists(startup_path):
                    os.makedirs(startup_path)
                
                shutil.copy('start_agent.bat', os.path.join(startup_path, 'Agente POS.bat'))
                print("✅ Inicio automático configurado (método alternativo)")
        else:
            print("ℹ️  Inicio automático omitido")
    
    def test_connection(self):
        """Probar conexión con VPS"""
        print(f"\n🔗 Probando conexión con VPS...")
        try:
            response = requests.get(f"{self.vps_url}/", timeout=5)
            if response.status_code == 200:
                print("✅ Conexión con VPS exitosa")
                return True
            else:
                print(f"⚠️  VPS respondió con código: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return False
    
    def show_completion(self):
        """Mostrar mensaje de completado"""
        print("\n" + "=" * 65)
        print("                ¡INSTALACIÓN COMPLETADA!")
        print("=" * 65)
        print()
        print("✅ Dependencias Python instaladas")
        print("✅ Scripts de inicio creados")
        print("✅ Acceso directo en escritorio")
        print("✅ Configuración guardada")
        print()
        print("📋 Comandos disponibles:")
        print("   🚀 start_agent.bat      - Iniciar agente")
        print("   🔗 agent_config.json  - Configuración")
        print("   🌐 VPS URL:         ", self.vps_url)
        print()
        print("El agente correrá en http://localhost:5001")
        print("y se registrará automáticamente con tu VPS.")
        print()
        
        start_now = input("¿Iniciar agente ahora? (S/N): ").strip().upper()
        if start_now == 'S':
            print("\n🚀 Iniciando agente...")
            subprocess.Popen(['start_agent.bat'], shell=True)
        
        print("\n🎯 ¡Listo para conectar dispositivos locales con tu POS!")
        print("   Desde tu POS en la nube podrás:")
        print("   • Imprimir tickets")
        print("   • Leer básculas")
        print("   • Controlar dispositivos locales")
    
    def run(self):
        """Ejecutar instalación completa"""
        self.print_banner()
        
        # Paso 1: Verificar Python
        if not self.check_python():
            return
        
        # Paso 2: Instalar paquetes
        self.install_packages()
        
        # Paso 3: Configurar VPS
        self.configure_vps_url()
        
        # Paso 4: Crear scripts
        self.create_start_script()
        
        # Paso 5: Acceso directo
        self.create_desktop_shortcut()
        
        # Paso 6: Inicio automático
        self.setup_autostart()
        
        # Prueba de conexión
        self.test_connection()
        
        # Mensaje final
        self.show_completion()
        
        input("\nPresione Enter para salir...")

if __name__ == "__main__":
    installer = AgentInstaller()
    installer.run()