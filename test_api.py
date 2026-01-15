#!/usr/bin/env python3
"""
Script de prueba rápida para POS Device Connector
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_api():
    print("🚀 Iniciando prueba de POS Device Connector...")
    
    # 1. Probar conexión básica
    print("\n1. Probando conexión básica...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ Conexión exitosa")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"❌ Error en conexión: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # 2. Probar detección de impresoras
    print("\n2. Probando detección de impresoras...")
    try:
        response = requests.get(f"{BASE_URL}/devices/printers", timeout=5)
        if response.status_code == 200:
            printers = response.json()
            print("✅ Detección de impresoras exitosa")
            print(f"   Impresoras encontradas: {len(printers.get('printers', []))}")
            for printer in printers.get('printers', []):
                print(f"   - {printer['name']}")
        else:
            print(f"❌ Error detectando impresoras: {response.status_code}")
    except Exception as e:
        print(f"❌ Error detectando impresoras: {e}")
    
    # 3. Probar detección de básculas
    print("\n3. Probando detección de básculas...")
    try:
        response = requests.get(f"{BASE_URL}/devices/scales", timeout=5)
        if response.status_code == 200:
            scales = response.json()
            print("✅ Detección de básculas exitosa")
            print(f"   Básculas encontradas: {len(scales.get('scales', []))}")
            for scale in scales.get('scales', []):
                print(f"   - {scale['port']}")
        else:
            print(f"❌ Error detectando básculas: {response.status_code}")
    except Exception as e:
        print(f"❌ Error detectando básculas: {e}")
    
    # 4. Probar impresión de prueba
    print("\n4. Probando impresión de prueba...")
    try:
        # Primero obtener impresoras disponibles
        printers_response = requests.get(f"{BASE_URL}/devices/printers", timeout=5)
        if printers_response.status_code == 200:
            printers = printers_response.json().get('printers', [])
            if printers:
                printer_name = printers[0]['name']  # Usar primera impresora
                
                print_data = {
                    "printer_name": printer_name,
                    "content": {
                        "items": [
                            {"name": "Producto Prueba", "price": 10.50, "qty": 2},
                            {"name": "Servicio Prueba", "price": 5.25, "qty": 1}
                        ],
                        "total": 26.25
                    }
                }
                
                response = requests.post(
                    f"{BASE_URL}/print",
                    json=print_data,
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print("✅ Impresión de prueba exitosa")
                    print(f"   Impresora: {result['result']['printer']}")
                    print(f"   Estado: {result['result']['status']}")
                else:
                    print(f"❌ Error en impresión: {response.status_code}")
                    print(f"   Error: {response.json()}")
            else:
                print("⚠️  No hay impresoras disponibles para prueba")
        else:
            print("❌ No se pudo obtener lista de impresoras")
    except Exception as e:
        print(f"❌ Error en impresión de prueba: {e}")
    
    print("\n🎉 Prueba completada!")
    return True

if __name__ == "__main__":
    test_api()