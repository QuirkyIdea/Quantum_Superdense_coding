"""
Quantum Server - Flask API for Quantum Superdense Coding and Steganography
"""

from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
import json
import numpy as np
from quantum_core.superdense_coding import SuperdenseCoding
from quantum_core.steganography import QuantumSteganography
import secrets
import os
import urllib.request
import pathlib
import requests

app = Flask(__name__)
CORS(app)

# Initialize quantum systems
superdense_coding = SuperdenseCoding()
steganography = QuantumSteganography()

# Paths for serving dashboard assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, 'web_interface')
ASSETS_DIR = os.path.join(WEB_DIR, 'assets')

def ensure_local_assets():
    """Download required front-end assets locally if missing."""
    try:
        pathlib.Path(ASSETS_DIR).mkdir(parents=True, exist_ok=True)
        assets = {
            'three.min.js': 'https://unpkg.com/three@0.128.0/build/three.min.js',
            'GLTFLoader.js': 'https://unpkg.com/three@0.128.0/examples/js/loaders/GLTFLoader.js',
            'OrbitControls.js': 'https://unpkg.com/three@0.128.0/examples/js/controls/OrbitControls.js',
        }
        for filename, url in assets.items():
            target_path = os.path.join(ASSETS_DIR, filename)
            if not os.path.exists(target_path) or os.path.getsize(target_path) == 0:
                try:
                    urllib.request.urlretrieve(url, target_path)
                except Exception:
                    # If download fails, leave any existing file as-is
                    pass
    except Exception:
        # Non-fatal; 2D fallback will still run
        pass

# Ensure assets are present on startup
ensure_local_assets()

# Session storage for active communications
active_sessions = {}

@app.route('/')
def home():
    """Home page with API documentation"""
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🚀 Quantum Superdense Coding Server</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #1a1a1a; color: #fff; }
            .container { max-width: 900px; margin: 0 auto; }
            .header { text-align: center; margin-bottom: 40px; }
            .endpoint { background: #333; padding: 20px; margin: 20px 0; border-radius: 8px; }
            .method { color: #4CAF50; font-weight: bold; }
            .url { color: #2196F3; font-family: monospace; }
            .description { margin: 10px 0; }
            .example { background: #444; padding: 15px; border-radius: 5px; font-family: monospace; }
            a.button { display:inline-block; padding:10px 16px; background:#2196F3; color:#fff; text-decoration:none; border-radius:6px; margin-top: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Quantum Superdense Coding Server</h1>
                <p>Advanced quantum communication with steganography</p>
                <p><a class="button" href="/dashboard">Open 3D Web Game Dashboard</a></p>
            </div>
            
            <div class="endpoint">
                <h3><span class="method">POST</span> <span class="url">/api/encode</span></h3>
                <div class="description">Encode a 2-bit message using superdense coding</div>
                <div class="example">
                    {"message": "01", "steganography": true, "watermark": "QUANTUM_TEAM"}
                </div>
            </div>
            
            <div class="endpoint">
                <h3><span class="method">POST</span> <span class="url">/api/decode</span></h3>
                <div class="description">Decode a quantum message</div>
                <div class="example">{"session_id": "..."}</div>
            </div>
            
            <div class="endpoint">
                <h3><span class="method">POST</span> <span class="url">/api/steganography/hide</span></h3>
                <div class="description">Hide message in quantum noise</div>
            </div>
            
            <div class="endpoint">
                <h3><span class="method">POST</span> <span class="url">/api/steganography/extract</span></h3>
                <div class="description">Extract hidden message from noise</div>
            </div>
            
            <div class="endpoint">
                <h3><span class="method">GET</span> <span class="url">/api/status</span></h3>
                <div class="description">Get server status and statistics</div>
            </div>
        </div>
    </body>
    </html>
    ''')

@app.route('/dashboard')
def serve_dashboard():
    """Serve the 3D web game dashboard"""
    return send_from_directory(WEB_DIR, 'dashboard.html')

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """Serve dashboard assets (JS/CSS) from web_interface/assets"""
    assets_dir = os.path.join(WEB_DIR, 'assets')
    asset_path = os.path.join(assets_dir, filename)
    # Fallback to root of WEB_DIR if not present in assets
    if not os.path.exists(asset_path):
        fallback_path = os.path.join(WEB_DIR, filename)
        if os.path.exists(fallback_path):
            return send_from_directory(WEB_DIR, filename)
    return send_from_directory(assets_dir, filename)

@app.route('/api/encode', methods=['POST'])
def encode_message():
    """Encode a 2-bit message using superdense coding"""
    try:
        data = request.get_json()
        message = data.get('message')
        # Derive operator from message to enforce correct mapping
        pauli_operator = None
        apply_steganography = data.get('apply_steganography', False)
        watermark = data.get('watermark')
        
        if not message or message not in ['00', '01', '10', '11']:
            return jsonify({'error': 'Invalid message. Must be 2-bit string (00, 01, 10, 11)'}), 400
        
        # Fixed mapping (00->I, 01->X, 10->Z, 11->Y/XZ)
        try:
            pauli_operator = superdense_coding._get_pauli_operator(message)  # type: ignore
        except Exception:
            # Fallback mapping if method signature changes
            mapping = {'00': 'I', '01': 'X', '10': 'Z', '11': 'Y'}
            pauli_operator = mapping.get(message, 'I')
        
        # Encode message
        encoded_data = superdense_coding.encode_message(
            message=message,
            apply_steganography=apply_steganography,
            watermark=watermark
        )
        
        # Create session
        session_id = secrets.token_hex(16)
        active_sessions[session_id] = {
            'encoded_data': encoded_data,
            'timestamp': np.random.random(),
            'type': 'superdense_coding'
        }
        
        return jsonify({
            'session_id': session_id,
            'message': message,
            'pauli_operator': pauli_operator,
            'steganography_applied': apply_steganography,
            'watermark': watermark,
            'success': True,
            'circuit_depth': encoded_data['circuit'].depth(),
            'circuit_gates': len(encoded_data['circuit'].data)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/decode', methods=['POST'])
def decode_message():
    """Decode a quantum message"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        if session_id not in active_sessions:
            return jsonify({'error': 'Invalid session ID'}), 400
        
        session_data = active_sessions[session_id]
        encoded_data = session_data['encoded_data']
        
        # Decode message
        decoded_result = superdense_coding.decode_message(encoded_data)
        
        # Clean up session
        del active_sessions[session_id]
        
        return jsonify({
            'decoded_message': decoded_result['decoded_message'],
            'original_message': decoded_result['original_message'],
            'success': decoded_result['success'],
            'fidelity': decoded_result['fidelity'],
            'watermark': decoded_result.get('watermark')
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/steganography/hide', methods=['POST'])
def hide_message():
    """Hide message in quantum noise"""
    try:
        data = request.get_json()
        message = data.get('message')
        watermark = data.get('watermark')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Create noise circuit with hidden message
        circuit_data = steganography.create_noise_circuit(message, watermark)
        
        # Create session
        session_id = secrets.token_hex(16)
        active_sessions[session_id] = {
            'circuit_data': circuit_data,
            'timestamp': np.random.random(),
            'type': 'steganography'
        }
        
        # Analyze noise appearance
        noise_analysis = steganography.create_noise_analysis_report(circuit_data)
        
        return jsonify({
            'session_id': session_id,
            'hidden_message': message,
            'watermark': watermark,
            'noise_level': circuit_data['noise_level'],
            'appears_random': noise_analysis['appears_random'],
            'circuit_entropy': noise_analysis['circuit_entropy'],
            'measurement_entropy': noise_analysis['measurement_entropy'],
            'total_gates': noise_analysis['total_gates']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/steganography/extract', methods=['POST'])
def extract_message():
    """Extract hidden message from noise"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        if session_id not in active_sessions:
            return jsonify({'error': 'Invalid session ID'}), 400
        
        session_data = active_sessions[session_id]
        circuit_data = session_data['circuit_data']
        
        # Extract hidden message
        extraction_result = steganography.extract_hidden_message(circuit_data)
        
        # Clean up session
        del active_sessions[session_id]
        
        return jsonify({
            'extracted_message': extraction_result['extracted_message'],
            'watermark': extraction_result.get('watermark'),
            'signature_valid': extraction_result['signature_valid'],
            'extraction_success': extraction_result['extraction_success']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/eavesdropping/simulate', methods=['POST'])
def simulate_eavesdropping():
    """Simulate eavesdropping attempt"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        eavesdropper_knowledge = data.get('eavesdropper_knowledge', 0.5)
        
        if session_id not in active_sessions:
            return jsonify({'error': 'Invalid session ID'}), 400
        
        session_data = active_sessions[session_id]
        encoded_data = session_data['encoded_data']
        
        # Simulate eavesdropping
        eavesdropping_result = superdense_coding.simulate_eavesdropping(
            encoded_data, eavesdropper_knowledge
        )
        
        return jsonify({
            'eavesdropper_success': eavesdropping_result['eavesdropper_success'],
            'detection_probability': eavesdropping_result['detection_probability'],
            'original_message': eavesdropping_result['original_message']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/quantum/signature', methods=['POST'])
def create_quantum_signature():
    """Create quantum signature for message authentication"""
    try:
        data = request.get_json()
        message = data.get('message')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Create quantum signature
        signature_data = superdense_coding.create_quantum_signature(message)
        
        return jsonify({
            'message_hash': signature_data['message_hash'],
            'signature_bits': signature_data['signature_bits'],
            'signature_circuit_depth': signature_data['signature_circuit']['circuit'].depth()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/quantum/signature/verify', methods=['POST'])
def verify_quantum_signature():
    """Verify quantum signature"""
    try:
        data = request.get_json()
        message = data.get('message')
        signature_data = data.get('signature_data')
        
        if not message or not signature_data:
            return jsonify({'error': 'Message and signature data are required'}), 400
        
        # Verify signature
        is_valid = superdense_coding.verify_quantum_signature(message, signature_data)
        
        return jsonify({
            'signature_valid': is_valid,
            'message': message
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/team/watermark', methods=['POST'])
def create_team_watermark():
    """Create team watermark for embedding"""
    try:
        data = request.get_json()
        team_name = data.get('team_name')
        logo_data = data.get('logo_data')
        
        if not team_name:
            return jsonify({'error': 'Team name is required'}), 400
        
        # Create team watermark
        watermark_data = steganography.create_team_watermark(team_name, logo_data)
        
        return jsonify({
            'team_name': watermark_data['team_name'],
            'signature': watermark_data['signature'],
            'timestamp': watermark_data['timestamp']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get server status and statistics"""
    try:
        active_sessions_count = len(active_sessions)
        
        # Calculate session types
        session_types = {}
        for session in active_sessions.values():
            session_type = session['type']
            session_types[session_type] = session_types.get(session_type, 0) + 1
        
        return jsonify({
            'status': 'running',
            'active_sessions': active_sessions_count,
            'session_types': session_types,
            'quantum_backend': 'qasm_simulator',
            'steganography_noise_level': steganography.noise_level
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/demo/superdense_coding', methods=['GET'])
def demo_superdense_coding():
    """Demo superdense coding with all 2-bit messages"""
    try:
        results = {}
        
        for message in ['00', '01', '10', '11']:
            # Encode
            encoded_data = superdense_coding.encode_message(message, apply_steganography=False)
            
            # Decode
            decoded_result = superdense_coding.decode_message(encoded_data)
            
            results[message] = {
                'encoded': message,
                'decoded': decoded_result['decoded_message'],
                'success': decoded_result['success'],
                'fidelity': decoded_result['fidelity']
            }
        
        return jsonify({
            'demo_type': 'superdense_coding',
            'results': results,
            'total_success_rate': sum(1 for r in results.values() if r['success']) / len(results)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/demo/steganography', methods=['GET'])
def demo_steganography():
    """Demo quantum steganography"""
    try:
        # Create hidden message
        secret_message = "Hello Quantum World!"
        circuit_data = steganography.create_noise_circuit(secret_message, "QUANTUM_TEAM")
        
        # Extract message
        extraction_result = steganography.extract_hidden_message(circuit_data)
        
        # Analyze noise
        noise_analysis = steganography.create_noise_analysis_report(circuit_data)
        
        return jsonify({
            'demo_type': 'steganography',
            'original_message': secret_message,
            'extracted_message': extraction_result['extracted_message'],
            'extraction_success': extraction_result['extraction_success'],
            'appears_random': noise_analysis['appears_random'],
            'circuit_entropy': noise_analysis['circuit_entropy'],
            'measurement_entropy': noise_analysis['measurement_entropy']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/gemini', methods=['POST'])
def gemini_proxy():
    """Proxy endpoint for Gemini API calls to avoid CORS issues"""
    try:
        # Get the request data
        data = request.get_json()
        user_message = data.get('message', '')
        
        # Gemini API configuration
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        api_key = os.getenv('GEMINI_API_KEY', '')  # Get API key from environment variable
        
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": api_key
        }
        
        # Project knowledge base
        project_knowledge = """
        This is a Quantum Superdense Coding + Steganography project with the following features:

        PROJECT OVERVIEW:
        - Quantum superdense coding implementation using Qiskit
        - Quantum steganography to hide messages in quantum noise
        - Interactive 3D visualization with Three.js
        - Flask API server for quantum operations
        - Educational gamification features

        KEY COMPONENTS:
        1. quantum_core/ - Core quantum implementation
           - superdense_coding.py: Main protocol implementation
           - bell_states.py: Bell state operations
           - steganography.py: Message hiding in quantum noise

        2. web_interface/ - 3D visualization
           - dashboard.html: Main web interface
           - quantum_canvas.js: Three.js 3D graphics
           - assets/: Three.js libraries

        3. quantum_server.py - Flask API server
        4. vr_visualizer/ - Dash-based VR application
        5. steganography_demo.py - Demo script

        QUANTUM CONCEPTS:
        - Superdense coding: Send 2 classical bits using 1 qubit
        - Bell states: |Φ⁺⟩ = (|00⟩ + |11⟩)/√2, |Φ⁻⟩, |Ψ⁺⟩, |Ψ⁻⟩
        - Pauli operators: I (Identity), X (NOT), Z (Phase), Y (Both)
        - Quantum entanglement: Non-local correlations
        - Quantum steganography: Hide messages in quantum noise

        PROTOCOL STEPS:
        1. Create Bell pair |Φ⁺⟩ between Alice and Bob
        2. Alice applies Pauli operation to encode 2-bit message
        3. Alice sends her qubit to Bob
        4. Bob performs Bell measurement to decode message

        SECURITY FEATURES:
        - Quantum steganography for message hiding
        - Eavesdropping detection
        - Quantum signatures for authentication
        - Team watermarking

        USAGE:
        - Start server: python quantum_server.py
        - Open dashboard: http://localhost:5000/dashboard
        - Select 2-bit message (00, 01, 10, 11)
        - Choose Pauli operator (I, X, Z, Y)
        - Enable/disable steganography
        - Watch 3D animation of quantum transmission

        TECHNOLOGIES:
        - Python, Qiskit, Flask
        - Three.js, WebGL
        - HTML5, CSS3, JavaScript
        - Dash, Plotly
        """
        
        # Prepare the request to Gemini
        gemini_data = {
            "contents": [{
                "parts": [{
                    "text": f"You are a helpful AI assistant specializing in quantum computing and specifically this quantum superdense coding project. \n\n{project_knowledge}\n\nUser question: {user_message}\n\nPlease provide a helpful, accurate response based on the project knowledge above. Keep responses concise but informative."
                }]
            }]
        }
        
        # Make the request to Gemini API
        response = requests.post(url, headers=headers, data=json.dumps(gemini_data))
        
        if response.status_code == 200:
            result = response.json()
            if result.get("candidates") and result["candidates"][0].get("content"):
                ai_response = result["candidates"][0]["content"]["parts"][0]["text"]
                return jsonify({"success": True, "response": ai_response})
            else:
                return jsonify({"success": False, "error": "No response from AI model"})
        else:
            return jsonify({"success": False, "error": f"API Error: {response.status_code}"})
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/interactive-demo', methods=['POST'])
def interactive_demo():
    """Interactive demo endpoint for real-time quantum simulation"""
    try:
        data = request.get_json()
        bits = data.get('bits', '00')
        noise_level = data.get('noise', 0) / 100.0  # Convert percentage to decimal
        
        # Validate input
        if bits not in ['00', '01', '10', '11']:
            return jsonify({"success": False, "error": "Invalid bits. Must be 00, 01, 10, or 11"})
        
        # Create quantum circuit with noise
        circuit_data = superdense_coding.create_demo_circuit(bits, noise_level)
        
        return jsonify({
            "success": True,
            "circuit": circuit_data,
            "original_bits": bits,
            "noise_level": noise_level,
            "fidelity": max(0, 1 - noise_level),  # Simple fidelity calculation
            "comparison": {
                "classical_transmissions": 2,
                "quantum_transmissions": 1,
                "efficiency_gain": "50%"
            }
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/game/score', methods=['POST'])
def update_game_score():
    """Update game score and track performance"""
    try:
        data = request.get_json()
        player_name = data.get('player', 'Anonymous')
        score = data.get('score', 0)
        correct_decodings = data.get('correct', 0)
        errors = data.get('errors', 0)
        
        # Store in session (in production, use a database)
        if 'game_scores' not in active_sessions:
            active_sessions['game_scores'] = []
        
        game_result = {
            "player": player_name,
            "score": score,
            "correct_decodings": correct_decodings,
            "errors": errors,
            "success_rate": correct_decodings / max(1, correct_decodings + errors) * 100,
            "timestamp": str(np.datetime64('now'))
        }
        
        active_sessions['game_scores'].append(game_result)
        
        return jsonify({
            "success": True,
            "message": "Score updated successfully",
            "leaderboard": get_top_scores()
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/game/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get top scores for the game"""
    try:
        return jsonify({
            "success": True,
            "leaderboard": get_top_scores()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

def get_top_scores():
    """Get top 10 scores from active sessions"""
    if 'game_scores' not in active_sessions:
        return []
    
    scores = active_sessions['game_scores']
    sorted_scores = sorted(scores, key=lambda x: x['score'], reverse=True)
    return sorted_scores[:10]

@app.route('/api/quantum-hardware/simulate', methods=['POST'])
def simulate_quantum_hardware():
    """Simulate real quantum hardware with realistic noise"""
    try:
        data = request.get_json()
        bits = data.get('bits', '00')
        backend_type = data.get('backend', 'simulator')  # 'simulator' or 'real_hardware'
        
        # Simulate different noise profiles
        if backend_type == 'simulator':
            noise_profile = {
                "readout_error": 0.01,
                "gate_error": 0.005,
                "decoherence_time": 100.0
            }
        else:  # real_hardware
            noise_profile = {
                "readout_error": 0.05,
                "gate_error": 0.02,
                "decoherence_time": 50.0
            }
        
        # Run simulation with noise
        result = superdense_coding.simulate_with_noise(bits, noise_profile)
        
        return jsonify({
            "success": True,
            "backend_type": backend_type,
            "noise_profile": noise_profile,
            "result": result,
            "fidelity": result.get('fidelity', 0.95),
            "error_rate": 1 - result.get('fidelity', 0.95)
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    print("🚀 Starting Quantum Superdense Coding Server...")
    print("🌐 Server will be available at: http://localhost:5000")
    print("📚 API documentation available at: http://localhost:5000/")
    print("🕹️ 3D Web Game dashboard: http://localhost:5000/dashboard")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
