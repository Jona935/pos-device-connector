from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import logging

app = Flask(__name__)
CORS(app)

# Base de datos simulada
devices = {}
print_jobs = []
scale_readings = []

@app.route('/')
def index():
    return jsonify({
        'status': 'running',
        'message': 'POS Cloud Simulator',
        'version': '1.0.0'
    })

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time()
    })

@app.route('/api/device/register', methods=['POST'])
def register_device():
    """Registrar dispositivo local"""
    try:
        data = request.json
        device_info = data.get('device_info')
        local_ip = data.get('local_ip')
        
        device_id = f"device_{len(devices) + 1}"
        devices[device_id] = {
            'info': device_info,
            'local_ip': local_ip,
            'registered_at': time.time(),
            'status': 'active'
        }
        
        return jsonify({
            'success': True,
            'device_id': device_id,
            'message': 'Dispositivo registrado exitosamente'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/device/print/completed', methods=['POST'])
def print_completed():
    """Recibir notificación de impresión completada"""
    try:
        data = request.json
        result = data.get('result')
        
        print_jobs.append({
            'result': result,
            'completed_at': time.time()
        })
        
        return jsonify({
            'success': True,
            'message': 'Notificación de impresión recibida'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/device/scale/reading', methods=['POST'])
def scale_reading():
    """Recibir lectura de báscula"""
    try:
        data = request.json
        weight_data = data.get('data')
        
        scale_readings.append({
            'data': weight_data,
            'received_at': time.time()
        })
        
        return jsonify({
            'success': True,
            'message': 'Lectura de báscula recibida'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/devices', methods=['GET'])
def get_devices():
    """Obtener lista de dispositivos registrados"""
    return jsonify({
        'success': True,
        'devices': devices
    })

@app.route('/api/print-jobs', methods=['GET'])
def get_print_jobs():
    """Obtener historial de impresiones"""
    return jsonify({
        'success': True,
        'jobs': print_jobs[-10:]  # Últimos 10 trabajos
    })

@app.route('/api/scale-readings', methods=['GET'])
def get_scale_readings():
    """Obtener historial de lecturas de báscula"""
    return jsonify({
        'success': True,
        'readings': scale_readings[-10:]  # Últimas 10 lecturas
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)