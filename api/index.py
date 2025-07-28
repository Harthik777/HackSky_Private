"""
Vercel Serverless Function Entry Point
Routes API requests to the backend Flask application logic
"""

import os
import sys
import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Add the backend directory to the path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

# Import the ICS Monitor from our backend
try:
    from server import ICSMonitor
    monitor = ICSMonitor()
    backend_available = True
except ImportError as e:
    monitor = None
    backend_available = False
    import_error = str(e)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        # Remove /api prefix if present (since Vercel adds it)
        if path.startswith('/api'):
            path = path[4:]
        
        try:
            if not backend_available:
                self._send_error(500, f"Backend import failed: {import_error}")
                return
                
            # Route to appropriate handler
            if path == '/health':
                data = {
                    'status': 'healthy',
                    'timestamp': monitor.get_power_data()[0]['time'] if monitor.get_power_data() else '',
                    'data_source': monitor.dataset_type,
                    'wadi_available': hasattr(monitor, 'wadi_connector') and monitor.wadi_connector is not None,
                    'generic_data_available': hasattr(monitor, 'data_connector') and monitor.data_connector is not None,
                    'version': '2.0.0'
                }
            elif path == '/power-data':
                data = monitor.get_power_data()
            elif path == '/system-status':
                data = monitor.get_system_status()
            elif path == '/alerts':
                data = monitor.get_alerts()
            elif path == '/attack-analysis':
                data = monitor.get_attack_analysis()
            elif path == '/statistics':
                data = monitor.get_statistics()
            elif path == '/wadi-info':
                if hasattr(monitor, 'wadi_connector') and monitor.wadi_connector:
                    data = {
                        'dataset_name': 'WADI (Water Distribution)',
                        'description': 'Real water distribution system with cyber attack scenarios',
                        'sensors_mapped': len(monitor.wadi_connector.sensor_mapping),
                        'files_expected': ['WADI_14days.csv', 'WADI_attackdata.csv'],
                        'setup_complete': monitor.dataset_type == 'WADI',
                        'source': 'Singapore University of Technology and Design (SUTD)',
                        'sensor_types': [
                            'Flow sensors (FIT_*)',
                            'Level sensors (LIT_*)', 
                            'Pressure sensors (PIT_*)',
                            'Water quality analyzers (AIT_*)',
                            'Pump actuators (P_*)',
                            'Valve actuators (MV_*)'
                        ]
                    }
                else:
                    self._send_error(404, 'WADI integration not available')
                    return
            elif path == '/data-source':
                data = {
                    'dataset_type': monitor.dataset_type,
                    'wadi_available': hasattr(monitor, 'wadi_connector') and monitor.wadi_connector is not None,
                    'generic_data_available': hasattr(monitor, 'data_connector') and monitor.data_connector is not None,
                    'instructions': {
                        'wadi_setup': 'Download WADI dataset and place in data/wadi/ directory',
                        'wadi_files': ['WADI_14days.csv', 'WADI_attackdata.csv'],
                        'csv_integration': 'Place CSV file at data/power_consumption.csv',
                        'modbus_integration': 'Set environment variables: MODBUS_HOST, MODBUS_PORT',
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
            if not backend_available:
                self._send_error(500, f"Backend import failed: {import_error}")
                return
                
            if path == '/alerts':
                # Handle POST to /alerts (add new alert)
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                if 'type' in data and 'message' in data and 'system' in data:
                    monitor.add_alert(data['type'], data['message'], data['system'])
                    response = {'status': 'success', 'message': 'Alert added'}
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