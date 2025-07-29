"""
Vercel Serverless Function Entry Point
Lightweight ICS Cybersecurity Dashboard API
"""

import json
import random
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        # Remove /api prefix if present (since Vercel adds it)
        if path.startswith('/api'):
            path = path[4:]
        
        try:
            # Route to appropriate handler
            if path == '/health':
                data = {
                    'status': 'healthy',
                    'timestamp': datetime.now().isoformat(),
                    'data_source': 'WADI Water Distribution System',
                    'version': '2.0.0'
                }
            elif path == '/power-data':
                data = self._get_power_data()
            elif path == '/system-status':
                data = self._get_system_status()
            elif path == '/alerts':
                data = self._get_alerts()
            elif path == '/attack-analysis':
                data = self._get_attack_analysis()
            elif path == '/statistics':
                data = self._get_statistics()
            elif path == '/wadi-info':
                data = {
                    'dataset_name': 'WADI (Water Distribution)',
                    'description': 'Real water distribution system with cyber attack scenarios',
                    'sensors_mapped': 131,
                    'files_expected': ['WADI_14days.csv', 'WADI_attackdata.csv'],
                    'setup_complete': False,
                    'source': 'Singapore University of Technology and Design (SUTD)',
                    'sensor_types': [
                        'Flow sensors (FIT_*)',
                        'Level sensors (LIT_*)', 
                        'Pressure sensors (PIT_*)',
                        'Water quality analyzers (AIT_*)',
                        'Pump actuators (P_*)',
                        'Valve actuators (MV_*)'
                    ],
                    'note': 'Using simulated data in serverless environment'
                }
            elif path == '/data-source':
                data = {
                    'dataset_type': 'WADI (Simulated)',
                    'wadi_available': False,
                    'generic_data_available': False,
                    'environment': 'Vercel Serverless',
                    'note': 'Using WADI-based simulated data patterns',
                    'instructions': {
                        'local_development': 'Run backend/server.py for full WADI integration',
                        'wadi_setup': 'Download WADI dataset and place in data/wadi/ directory',
                        'wadi_files': ['WADI_14days.csv', 'WADI_attackdata.csv'],
                        'download_wadi': 'https://itrust.sutd.edu.sg/itrust-labs_datasets/'
                    }
                }
            else:
                self._send_error(404, f'Endpoint not found: {path}')
                return
                
            self._send_json_response(data)
            
        except Exception as e:
            self._send_error(500, f'Internal server error: {str(e)}')
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        # Remove /api prefix if present
        if path.startswith('/api'):
            path = path[4:]
            
        try:
            if path == '/alerts':
                # Handle POST to /alerts (simulate adding new alert)
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                if 'type' in data and 'message' in data and 'system' in data:
                    response = {
                        'status': 'success', 
                        'message': 'Alert received (simulated)',
                        'alert_id': f'alert_{random.randint(1000, 9999)}'
                    }
                    self._send_json_response(response)
                else:
                    self._send_error(400, 'Invalid data: type, message, and system required')
            else:
                self._send_error(404, f'POST endpoint not found: {path}')
                
        except Exception as e:
            self._send_error(500, f'Internal server error: {str(e)}')
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def _get_power_data(self):
        """Generate simulated power consumption data - matches frontend expectations"""
        base_time = datetime.now() - timedelta(minutes=30)
        data = []
        
        for i in range(10):
            time_point = base_time + timedelta(minutes=i*3)
            
            # Water distribution system baseline (600-800 kW typical)
            normal_power = 700 + random.uniform(-50, 50)
            
            # Add daily demand patterns
            hour = time_point.hour
            if 6 <= hour <= 10 or 18 <= hour <= 22:  # Peak water demand
                normal_power += 100
            elif 0 <= hour <= 5:  # Low demand overnight
                normal_power -= 80
            
            # Simulate cyber attack anomalies
            anomaly_power = None
            if random.random() > 0.88:  # 12% chance
                anomaly_power = normal_power + random.uniform(100, 200)
                
            data.append({
                'time': time_point.strftime('%H:%M'),
                'power': round(normal_power + random.uniform(-15, 15)),
                'normal': round(normal_power),
                'anomaly': round(anomaly_power) if anomaly_power else None
            })
        
        return data
    
    def _get_system_status(self):
        """Generate simulated system status - matches frontend expectations"""
        component_statuses = ['online', 'online', 'online', 'warning']  # Mostly online
        
        return {
            'overall': random.choice(['good', 'good', 'warning']),  # Mostly good
            'components': {
                'nilm': random.choice(component_statuses),
                'ml_models': random.choice(component_statuses),
                'data_collection': random.choice(component_statuses),
                'alert_system': random.choice(component_statuses)
            },
            'dataset_type': 'Simulated'
        }
    
    def _get_alerts(self):
        """Generate simulated security alerts - matches frontend expectations"""
        alert_types = ['critical', 'warning', 'info']
        systems = ['Water Distribution', 'Sensor Network', 'Treatment Plant', 'Control System']
        messages = [
            'Unusual power spike detected on Water Pump #2',
            'Flow sensor FIT_301 showing irregular patterns', 
            'Scheduled maintenance completed on UV disinfection system',
            'Network latency increased on PLC-001',
            'Pressure anomaly detected in distribution line',
            'Sensor calibration required for AIT_201'
        ]
        
        alerts = []
        for i in range(random.randint(2, 5)):
            alert_time = datetime.now() - timedelta(minutes=random.randint(1, 720))
            alerts.append({
                'id': 1000 + i,  # Frontend expects numeric ID
                'type': random.choice(alert_types),
                'message': random.choice(messages),
                'timestamp': alert_time.isoformat(),
                'system': random.choice(systems)
            })
        
        return sorted(alerts, key=lambda x: x['timestamp'], reverse=True)
    
    def _get_attack_analysis(self):
        """Generate simulated attack analysis with dynamic behavior - matches frontend expectations"""
        
        # Use time-based variation for more realistic dynamic behavior
        import time
        import math
        elapsed_minutes = (time.time() % 3600) / 60  # Reset every hour for demo
        time_factor = math.sin(elapsed_minutes * 0.1) * 0.3 + 1
        
        # Create an array of attack type objects with realistic variations
        base_attacks = [
            {'type': 'Flow Manipulation', 'base_prob': 15},
            {'type': 'Pressure Attack', 'base_prob': 10},
            {'type': 'Sensor Spoofing', 'base_prob': 8},
            {'type': 'Pump Control', 'base_prob': 12},
            {'type': 'Data Exfiltration', 'base_prob': 5},
            {'type': 'Network Intrusion', 'base_prob': 7},
            {'type': 'HMI Manipulation', 'base_prob': 6}
        ]
        
        attack_types_list = []
        for attack in base_attacks:
            # Add realistic variability
            prob_variation = random.uniform(-3, 8)
            time_influence = attack['base_prob'] * (time_factor - 1) * 0.5
            current_prob = max(5, min(30, attack['base_prob'] + prob_variation + time_influence))
            
            # Dynamic detection count based on probability
            detection_chance = current_prob / 100 * random.uniform(0.8, 1.2)
            detected_count = random.randint(0, 6) if random.random() < detection_chance else random.randint(0, 2)
            
            attack_types_list.append({
                'type': attack['type'],
                'probability': round(current_prob, 1),
                'detected': detected_count
            })
        
        random.shuffle(attack_types_list)

        # Generate dynamic model metrics
        confidence = round(random.uniform(92, 98), 1)
        
        # Dynamic threat distribution based on detected attacks
        total_detections = sum(attack['detected'] for attack in attack_types_list)
        if total_detections > 8:
            threat_dist = [
                {'name': 'Normal', 'value': 70, 'color': '#10B981'},
                {'name': 'Suspicious', 'value': 22, 'color': '#F59E0B'},
                {'name': 'Malicious', 'value': 8, 'color': '#EF4444'}
            ]
        elif total_detections > 4:
            threat_dist = [
                {'name': 'Normal', 'value': 78, 'color': '#10B981'},
                {'name': 'Suspicious', 'value': 17, 'color': '#F59E0B'},
                {'name': 'Malicious', 'value': 5, 'color': '#EF4444'}
            ]
        else:
            threat_dist = [
                {'name': 'Normal', 'value': 87, 'color': '#10B981'},
                {'name': 'Suspicious', 'value': 10, 'color': '#F59E0B'},
                {'name': 'Malicious', 'value': 3, 'color': '#EF4444'}
            ]

        # Dynamic threat level based on detections
        total_detections = sum(attack['detected'] for attack in attack_types_list)
        avg_probability = sum(attack['probability'] for attack in attack_types_list) / len(attack_types_list)
        threat_score = total_detections * 3 + avg_probability
        
        if threat_score > 25:
            threat_level = 'High'
        elif threat_score > 15:
            threat_level = 'Medium'  
        else:
            threat_level = 'Low'

        return {
            'threat_level': threat_level,
            'confidence_score': confidence,
            'attack_types': attack_types_list,
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
        }
    
    def _get_statistics(self):
        """Generate simulated statistics - matches frontend expectations"""
        power_value = round(120 + random.uniform(-20, 30))
        accuracy = round(random.uniform(92, 98), 1)
        alert_count = random.randint(1, 5)
        
        return {
            # Frontend expects these exact keys
            'systems_monitored': random.randint(10, 15),
            'power_consumption': f"{power_value} kW",
            'active_alerts': alert_count,
            'detection_accuracy': f"{accuracy}%",
            
            # Additional data for potential future use
            'online_systems': random.randint(8, 12),
            'anomaly_count': random.randint(0, 3),
            'data_source': 'WADI',
            'last_updated': datetime.now().isoformat()
        }
    
    def _send_json_response(self, data):
        """Send JSON response with proper headers"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        
        json_data = json.dumps(data)
        self.wfile.write(json_data.encode('utf-8'))
    
    def _send_error(self, status_code, message):
        """Send error response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        error_data = {'error': message, 'status': status_code}
        json_data = json.dumps(error_data)
        self.wfile.write(json_data.encode('utf-8')) 