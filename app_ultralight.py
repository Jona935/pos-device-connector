from flask import Flask, request, jsonify
import os
import time

app = Flask(__name__)

# Almacenamiento simplificado
agents = {}

@app.route('/')
def index():
    return jsonify({
        'status': 'running',
        'message': 'POS Device Connector API - Ultralight',
        'version': '1.0.0',
        'environment': os.getenv('FLASK_ENV', 'development')
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time()
    })

@app.route('/metrics')
def metrics():
    return jsonify({
        'status': 'ok',
        'agents_count': len(agents)
    })

@app.route('/agent/register', methods=['POST'])
def agent_register():
    """Registrar agente local"""
    try:
        data = request.json
        agent_id = data.get('agent_id')
        
        agents[agent_id] = {
            'info': data,
            'last_seen': time.time(),
            'status': 'online'
        }
        
        print(f"✅ Agente registrado: {agent_id}")
        
        return jsonify({
            'success': True,
            'agent_id': agent_id,
            'message': 'Agente registrado exitosamente'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/agents', methods=['GET'])
def get_agents():
    """Obtener lista de agentes conectados"""
    try:
        agents_list = []
        current_time = time.time()
        
        for agent_id, agent_data in agents.items():
            is_online = (current_time - agent_data['last_seen']) < 60
            
            agents_list.append({
                'agent_id': agent_id,
                'platform': agent_data['info'].get('platform', 'Unknown'),
                'status': 'online' if is_online else 'offline',
                'last_seen': agent_data['last_seen'],
                'printers_count': len(agent_data['info'].get('printers', [])),
                'scales_count': len(agent_data['info'].get('scales', []))
            })
        
        return jsonify({
            'success': True,
            'agents': agents_list,
            'total': len(agents_list)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/agent/<agent_id>/print', methods=['POST'])
def print_via_agent(agent_id):
    """Imprimir via agente específico"""
    try:
        if agent_id not in agents:
            return jsonify({'success': False, 'error': 'Agente no encontrado'}), 404
        
        # Simular impresión por ahora
        data = request.json
        print(f"🖨️ Simulación impresión para {agent_id}:")
        print(f"   Impresora: {data.get('printer_name')}")
        print(f"   Contenido: {data.get('content')}")
        
        return jsonify({
            'success': True,
            'result': {
                'printer': data.get('printer_name'),
                'status': 'simulated',
                'timestamp': time.time()
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/agent/<agent_id>/scale/read', methods=['POST'])
def read_scale_via_agent(agent_id):
    """Leer báscula via agente específico"""
    try:
        if agent_id not in agents:
            return jsonify({'success': False, 'error': 'Agente no encontrado'}), 404
        
        # Simular lectura de báscula
        data = request.json
        print(f"⚖️ Simulación lectura báscula para {agent_id}:")
        print(f"   Puerto: {data.get('scale_port')}")
        
        return jsonify({
            'success': True,
            'weight': {
                'port': data.get('scale_port'),
                'weight': 1.23,
                'unit': 'kg',
                'timestamp': time.time(),
                'note': 'simulated'
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)