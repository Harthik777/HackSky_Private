#!/usr/bin/env python3
"""
Simple Test Server for ICS Dashboard - WADI Attack Types
This is a minimal server to test the frontend attack types display
"""

from flask import Flask, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

@app.route('/api/attack-analysis', methods=['GET'])
def get_attack_analysis():
    """Return WADI-specific attack analysis data"""
    return jsonify({
        'threat_level': 'medium',
        'confidence_score': round(random.uniform(85, 95), 1),
        'attack_types': [
            {'type': 'Flow Manipulation', 'probability': 18, 'detected': 2},
            {'type': 'Pressure Attack', 'probability': 12, 'detected': 1},
            {'type': 'Level Sensor Spoofing', 'probability': 8, 'detected': 0},
            {'type': 'Pump Control Attack', 'probability': 15, 'detected': 1},
            {'type': 'Quality Tampering', 'probability': 5, 'detected': 0}
        ],
        'threat_distribution': [
            {'name': 'Normal', 'value': 85, 'color': '#10B981'},
            {'name': 'Suspicious', 'value': 12, 'color': '#F59E0B'},
            {'name': 'Malicious', 'value': 3, 'color': '#EF4444'}
        ],
        'model_metrics': {
            'accuracy': 96.2,
            'precision': 94.1,
            'recall': 91.8,
            'f1Score': 92.9
        },
        'dataset_info': {
            'type': 'WADI',
            'attacks_available': True
        }
    })

@app.route('/api/power-data', methods=['GET'])
def get_power_data():
    """Return simulated power data"""
    import datetime
    data = []
    base_time = datetime.datetime.now() - datetime.timedelta(minutes=30)
    
    for i in range(10):
        time_point = base_time + datetime.timedelta(minutes=i*3)
        base_power = 500 + random.uniform(-50, 50)
        
        data.append({
            'time': time_point.strftime('%H:%M'),
            'power': round(base_power, 1),
            'anomaly': random.random() < 0.1
        })
    
    return jsonify(data)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    print("🚀 Starting Simple ICS Dashboard Server...")
    print("💧 WADI Attack Types Ready!")
    print("🌐 Server running on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False) 