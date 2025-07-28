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
                    'data_source': 'Simulated ICS Data',
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
                    'dataset_type': 'Simulated',
                    'wadi_available': False,
                    'generic_data_available': False,
                    'environment': 'Vercel Serverless',
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
        """Generate simulated power consumption data"""
        current_time = datetime.now()
        data = []
        
        for i in range(24):  # Last 24 hours
            timestamp = current_time - timedelta(hours=23-i)
            power_value = 100 + random.uniform(-20, 40) + (10 * (i % 8))  # Simulate daily pattern
            
            data.append({
                'time': timestamp.strftime('%H:%M'),
                'timestamp': timestamp.isoformat(),
                'power': round(power_value, 2),
                'status': 'normal' if power_value < 140 else 'high'
            })
        
        return data
    
    def _get_system_status(self):
        """Generate simulated system status"""
        systems = [
            'water_pump_1', 'water_pump_2', 'booster_pump', 
            'plc_control', 'scada_hmi', 'flow_sensor_1', 
            'pressure_sensor', 'valve_control'
        ]
        
        status_data = {}
        for system in systems:
            status_data[system] = {
                'status': random.choice(['online', 'online', 'online', 'warning']),  # Mostly online
                'power': round(80 + random.uniform(-30, 50), 2),
                'anomaly': random.choice([False, False, False, True]),  # Occasional anomalies
                'last_update': datetime.now().isoformat()
            }
        
        return status_data
    
    def _get_alerts(self):
        """Generate simulated security alerts"""
        alert_types = ['security', 'anomaly', 'system', 'network']
        systems = ['Water Pump 1', 'PLC Controller', 'SCADA HMI', 'Network Gateway']
        
        alerts = []
        for i in range(random.randint(2, 6)):
            alert_time = datetime.now() - timedelta(minutes=random.randint(1, 1440))
            alerts.append({
                'id': f'alert_{1000 + i}',
                'type': random.choice(alert_types),
                'system': random.choice(systems),
                'message': f'Simulated alert for {random.choice(systems)}',
                'severity': random.choice(['low', 'medium', 'high']),
                'timestamp': alert_time.isoformat(),
                'time': alert_time.strftime('%H:%M:%S')
            })
        
        return sorted(alerts, key=lambda x: x['timestamp'], reverse=True)
    
    def _get_attack_analysis(self):
        """Generate simulated attack analysis"""
        return {
            'total_attacks_detected': random.randint(15, 45),
            'attack_types': {
                'dos_attacks': random.randint(5, 15),
                'mitm_attempts': random.randint(2, 8),
                'unauthorized_access': random.randint(1, 5),
                'data_manipulation': random.randint(3, 12)
            },
            'risk_level': random.choice(['low', 'medium', 'high']),
            'last_attack': (datetime.now() - timedelta(hours=random.randint(1, 24))).isoformat(),
            'most_targeted_system': random.choice(['Water Pump System', 'PLC Network', 'SCADA Interface']),
            'note': 'Simulated data for demonstration'
        }
    
    def _get_statistics(self):
        """Generate simulated statistics"""
        return {
            'total_systems': 8,
            'systems_online': random.randint(6, 8),
            'anomalies_detected': random.randint(0, 3),
            'power_consumption': {
                'current': round(120 + random.uniform(-20, 30), 2),
                'average_24h': round(115 + random.uniform(-10, 20), 2),
                'peak_24h': round(145 + random.uniform(-5, 15), 2),
                'unit': 'kW'
            },
            'network_status': {
                'connections_active': random.randint(15, 25),
                'bandwidth_usage': round(random.uniform(30, 85), 1),
                'packets_per_second': random.randint(1200, 2500)
            },
            'security_score': round(random.uniform(75, 95), 1),
            'uptime_percentage': round(random.uniform(95, 99.9), 2),
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