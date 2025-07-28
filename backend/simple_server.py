#!/usr/bin/env python3
"""
Simple Test Server for ICS Dashboard - WADI Attack Types
This server provides dynamic attack detection data that changes over time
"""

from flask import Flask, jsonify
from flask_cors import CORS
import random
import time
import math

app = Flask(__name__)
CORS(app)

# Track detection history for more realistic data
detection_history = {
    'Flow Manipulation': {'base_prob': 15, 'detected_count': 0, 'last_detection': 0},
    'Pressure Attack': {'base_prob': 10, 'detected_count': 0, 'last_detection': 0},
    'Level Sensor Spoofing': {'base_prob': 8, 'detected_count': 0, 'last_detection': 0},
    'Pump Control Attack': {'base_prob': 12, 'detected_count': 0, 'last_detection': 0},
    'Quality Tampering': {'base_prob': 5, 'detected_count': 0, 'last_detection': 0},
    'Network Intrusion': {'base_prob': 7, 'detected_count': 0, 'last_detection': 0},
    'HMI Manipulation': {'base_prob': 6, 'detected_count': 0, 'last_detection': 0}
}

# Simulation state
simulation_start_time = time.time()

def generate_dynamic_attack_data():
    """Generate realistic, time-varying attack detection data"""
    current_time = time.time()
    elapsed_minutes = (current_time - simulation_start_time) / 60
    
    # Create time-based patterns (some attacks more likely at certain times)
    time_factor = math.sin(elapsed_minutes * 0.1) * 0.3 + 1  # Oscillates between 0.7 and 1.3
    
    attack_types = []
    
    for attack_name, data in detection_history.items():
        base_prob = data['base_prob']
        
        # Add realistic variability
        prob_variation = random.uniform(-3, 5)  # Slight random variation
        time_influence = base_prob * (time_factor - 1) * 0.5  # Time-based influence
        
        # Calculate current probability (ensure it stays reasonable)
        current_prob = max(0, min(30, base_prob + prob_variation + time_influence))
        
        # Simulate detection events (higher probability = higher chance of detection)
        detection_chance = current_prob / 100 * random.uniform(0.8, 1.2)
        
        if random.random() < detection_chance:
            data['detected_count'] += 1
            data['last_detection'] = current_time
            
        # Occasional false negatives (reset detection count)
        if random.random() < 0.02:  # 2% chance
            data['detected_count'] = max(0, data['detected_count'] - 1)
            
        attack_types.append({
            'type': attack_name,
            'probability': round(current_prob, 1),
            'detected': data['detected_count']
        })
    
    return attack_types

def generate_dynamic_threat_level():
    """Generate dynamic threat level based on current attack probabilities"""
    current_time = time.time()
    elapsed_minutes = (current_time - simulation_start_time) / 60
    
    # Base threat calculation
    total_detections = sum(data['detected_count'] for data in detection_history.values())
    avg_probability = sum(data['base_prob'] for data in detection_history.values()) / len(detection_history)
    
    # Time-based threat level changes
    time_modifier = math.sin(elapsed_minutes * 0.15) * 0.2 + 1
    threat_score = (total_detections * 5 + avg_probability) * time_modifier
    
    if threat_score > 25:
        return 'High'
    elif threat_score > 15:
        return 'Medium'
    else:
        return 'Low'

def generate_dynamic_confidence():
    """Generate dynamic confidence score"""
    base_confidence = 94.7
    variation = random.uniform(-2, 3)  # ±2-3% variation
    time_influence = math.sin(time.time() * 0.05) * 1.5  # Slow oscillation
    
    confidence = base_confidence + variation + time_influence
    return max(85, min(99, confidence))  # Keep between 85-99%

@app.route('/api/attack-analysis', methods=['GET'])
def get_attack_analysis():
    """Return dynamic WADI-specific attack analysis data"""
    
    # Generate dynamic data
    dynamic_attacks = generate_dynamic_attack_data()
    threat_level = generate_dynamic_threat_level()
    confidence = generate_dynamic_confidence()
    
    # Dynamic threat distribution (changes based on detections)
    total_detections = sum(attack['detected'] for attack in dynamic_attacks)
    if total_detections > 8:
        # High activity scenario
        threat_dist = [
            {'name': 'Normal', 'value': 70, 'color': '#10B981'},
            {'name': 'Suspicious', 'value': 22, 'color': '#F59E0B'},
            {'name': 'Malicious', 'value': 8, 'color': '#EF4444'}
        ]
    elif total_detections > 4:
        # Medium activity scenario
        threat_dist = [
            {'name': 'Normal', 'value': 78, 'color': '#10B981'},
            {'name': 'Suspicious', 'value': 17, 'color': '#F59E0B'},
            {'name': 'Malicious', 'value': 5, 'color': '#EF4444'}
        ]
    else:
        # Low activity scenario
        threat_dist = [
            {'name': 'Normal', 'value': 87, 'color': '#10B981'},
            {'name': 'Suspicious', 'value': 10, 'color': '#F59E0B'},
            {'name': 'Malicious', 'value': 3, 'color': '#EF4444'}
        ]
    
    return jsonify({
        'threat_level': threat_level,
        'confidence_score': round(confidence, 1),
        'attack_types': dynamic_attacks,
        'threat_distribution': threat_dist,
        'model_metrics': {
            'accuracy': round(confidence - random.uniform(0, 2), 1),
            'precision': round(confidence - random.uniform(1, 3), 1),
            'recall': round(confidence - random.uniform(2, 4), 1),
            'f1Score': round(confidence - random.uniform(1.5, 3.5), 1)
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
    print("🚀 Starting Dynamic ICS Dashboard Server...")
    print("💧 WADI Attack Types with Dynamic Data!")
    print("📊 Attack probabilities and detections will change over time")
    print("🌐 Server running on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False) 