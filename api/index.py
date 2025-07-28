from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import json
from datetime import datetime, timedelta
import random
import os
import sys

# Add the backend directory to the path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Import data integration modules
try:
    from data_integration import RealDataConnector
    real_data_available = True
except ImportError:
    real_data_available = False
    print("Warning: Generic data integration not available.")

try:
    from wadi_integration import WADIDataConnector
    wadi_data_available = True
except ImportError:
    wadi_data_available = False
    print("Warning: WADI data integration not available.")

app = Flask(__name__)
CORS(app)

# Enhanced ICS Monitor with WADI support
class ICSMonitor:
    def __init__(self):
        # Initialize data connectors
        self.real_connector = None
        self.wadi_connector = None
        
        if real_data_available:
            try:
                self.real_connector = RealDataConnector()
                print("Real data connector initialized successfully")
            except Exception as e:
                print(f"Failed to initialize real data connector: {e}")
        
        if wadi_data_available:
            try:
                self.wadi_connector = WADIDataConnector()
                print("WADI data connector initialized successfully")
            except Exception as e:
                print(f"Failed to initialize WADI data connector: {e}")
                
        # Initialize base system with default parameters
        self.initialize_system()
        
    def initialize_system(self):
        # System components
        self.components = {
            'HMI_Stations': {'count': 3, 'status': 'Normal'},
            'PLCs': {'count': 5, 'status': 'Normal'},
            'Sensors': {'count': 24, 'status': 'Normal'},
            'Actuators': {'count': 18, 'status': 'Normal'},
            'Network_Devices': {'count': 8, 'status': 'Normal'}
        }
        
        # Attack detection parameters
        self.detection_params = {
            'power_threshold': 50,
            'network_threshold': 75,
            'sensor_anomaly_threshold': 0.15,
            'response_time_threshold': 2.0
        }
        
        # Historical data for trend analysis
        self.historical_data = []
        self.attack_history = []
        
    def get_real_time_data(self):
        """Get real-time data from available connectors"""
        data = {}
        
        # Try to get data from WADI connector first (more specific)
        if self.wadi_connector:
            try:
                wadi_data = self.wadi_connector.get_current_data()
                if wadi_data:
                    data.update(wadi_data)
                    print("Using WADI real-time data")
            except Exception as e:
                print(f"Error getting WADI data: {e}")
        
        # Try to get data from generic real connector
        if self.real_connector and not data:
            try:
                real_data = self.real_connector.get_current_data()
                if real_data:
                    data.update(real_data)
                    print("Using generic real-time data")
            except Exception as e:
                print(f"Error getting real data: {e}")
        
        # Fallback to simulated data if no real data available
        if not data:
            data = self.generate_simulated_data()
            print("Using simulated data")
            
        return data
    
    def generate_simulated_data(self):
        """Generate realistic simulated ICS data"""
        now = datetime.now()
        
        # Simulate normal variations with occasional anomalies
        anomaly_chance = 0.05  # 5% chance of anomaly
        is_anomaly = random.random() < anomaly_chance
        
        base_power = 45 + random.normalvariate(0, 8)
        if is_anomaly:
            base_power += random.choice([-25, 25])  # Significant deviation
            
        data = {
            'timestamp': now.isoformat(),
            'power_consumption': max(0, base_power),
            'network_traffic': random.normalvariate(60, 15),
            'temperature': random.normalvariate(72, 5),
            'pressure': random.normalvariate(14.7, 0.5),
            'flow_rate': random.normalvariate(150, 20),
            'sensor_readings': {
                f'sensor_{i}': random.normalvariate(50, 10) for i in range(1, 13)
            },
            'system_status': {
                'cpu_usage': random.normalvariate(35, 10),
                'memory_usage': random.normalvariate(65, 15),
                'disk_usage': random.normalvariate(40, 8)
            },
            'network_metrics': {
                'latency': random.normalvariate(15, 5),
                'packet_loss': random.uniform(0, 0.5),
                'bandwidth_utilization': random.normalvariate(45, 12)
            }
        }
        
        return data

# Initialize the monitor
monitor = ICSMonitor()

@app.route('/api/status')
def get_system_status():
    """Get current system status"""
    try:
        current_data = monitor.get_real_time_data()
        
        # Determine overall system health
        power = current_data.get('power_consumption', 0)
        network = current_data.get('network_traffic', 0)
        
        # Simple health scoring
        health_score = 100
        if power > monitor.detection_params['power_threshold']:
            health_score -= 20
        if network > monitor.detection_params['network_threshold']:
            health_score -= 15
            
        status = {
            'overall_status': 'Critical' if health_score < 60 else 'Warning' if health_score < 80 else 'Normal',
            'health_score': max(0, health_score),
            'components': monitor.components,
            'last_updated': datetime.now().isoformat(),
            'active_alerts': max(0, int((100 - health_score) / 20)),
            'real_data_available': monitor.real_connector is not None or monitor.wadi_connector is not None
        }
        
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/power-data')
def get_power_data():
    """Get power consumption data for charts"""
    try:
        # Generate historical data for the chart
        data_points = []
        now = datetime.now()
        
        for i in range(24):  # Last 24 hours
            timestamp = now - timedelta(hours=23-i)
            
            # Get real-time data for current point, simulated for historical
            if i == 23:  # Current data point
                current_data = monitor.get_real_time_data()
                power = current_data.get('power_consumption', 45)
            else:
                power = 45 + random.normalvariate(0, 8)
                # Add some anomalies
                if random.random() < 0.08:
                    power += random.choice([-20, 20])
            
            data_points.append({
                'timestamp': timestamp.strftime('%H:%M'),
                'power': max(0, round(power, 2)),
                'temperature': round(random.normalvariate(72, 5), 1),
                'network': round(random.normalvariate(60, 15), 1)
            })
        
        return jsonify(data_points)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/attacks')
def get_attack_detection():
    """Get attack detection data"""
    try:
        current_data = monitor.get_real_time_data()
        
        # Analyze for potential attacks
        power = current_data.get('power_consumption', 0)
        network = current_data.get('network_traffic', 0)
        
        attacks = []
        
        # Power-based attack detection
        if power > monitor.detection_params['power_threshold']:
            severity = 'High' if power > 70 else 'Medium'
            attacks.append({
                'type': 'Power Anomaly',
                'severity': severity,
                'description': f'Unusual power consumption detected: {power:.1f}kW',
                'timestamp': datetime.now().isoformat(),
                'affected_systems': ['Power Grid', 'Load Balancer']
            })
        
        # Network-based attack detection
        if network > monitor.detection_params['network_threshold']:
            severity = 'High' if network > 90 else 'Medium'
            attacks.append({
                'type': 'Network Intrusion',
                'severity': severity,
                'description': f'Suspicious network activity: {network:.1f}% utilization',
                'timestamp': datetime.now().isoformat(),
                'affected_systems': ['Network Infrastructure', 'HMI Stations']
            })
        
        # Sensor anomaly detection
        sensor_readings = current_data.get('sensor_readings', {})
        for sensor, value in sensor_readings.items():
            if abs(value - 50) > 30:  # Significant deviation from normal
                attacks.append({
                    'type': 'Sensor Manipulation',
                    'severity': 'Medium',
                    'description': f'Sensor {sensor} showing abnormal reading: {value:.1f}',
                    'timestamp': datetime.now().isoformat(),
                    'affected_systems': ['Sensor Network', 'Control Systems']
                })
        
        # Summary statistics
        summary = {
            'total_attacks': len(attacks),
            'high_severity': len([a for a in attacks if a['severity'] == 'High']),
            'medium_severity': len([a for a in attacks if a['severity'] == 'Medium']),
            'low_severity': len([a for a in attacks if a['severity'] == 'Low']),
            'last_scan': datetime.now().isoformat()
        }
        
        return jsonify({
            'attacks': attacks,
            'summary': summary
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/alerts')
def get_alerts():
    """Get system alerts"""
    try:
        current_data = monitor.get_real_time_data()
        alerts = []
        
        # System health alerts
        system_status = current_data.get('system_status', {})
        cpu_usage = system_status.get('cpu_usage', 0)
        memory_usage = system_status.get('memory_usage', 0)
        
        if cpu_usage > 80:
            alerts.append({
                'type': 'System Performance',
                'message': f'High CPU usage detected: {cpu_usage:.1f}%',
                'severity': 'Warning',
                'timestamp': datetime.now().isoformat()
            })
            
        if memory_usage > 85:
            alerts.append({
                'type': 'System Performance',
                'message': f'High memory usage detected: {memory_usage:.1f}%',
                'severity': 'Warning',
                'timestamp': datetime.now().isoformat()
            })
        
        # Network alerts
        network_metrics = current_data.get('network_metrics', {})
        latency = network_metrics.get('latency', 0)
        packet_loss = network_metrics.get('packet_loss', 0)
        
        if latency > 25:
            alerts.append({
                'type': 'Network Performance',
                'message': f'High network latency: {latency:.1f}ms',
                'severity': 'Warning',
                'timestamp': datetime.now().isoformat()
            })
            
        if packet_loss > 1.0:
            alerts.append({
                'type': 'Network Performance',
                'message': f'Packet loss detected: {packet_loss:.2f}%',
                'severity': 'Critical',
                'timestamp': datetime.now().isoformat()
            })
        
        return jsonify(alerts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics')
def get_statistics():
    """Get system statistics"""
    try:
        current_data = monitor.get_real_time_data()
        
        # Calculate statistics
        stats = {
            'total_devices': sum(comp['count'] for comp in monitor.components.values()),
            'active_connections': random.randint(15, 25),
            'data_processed_mb': round(random.uniform(150, 300), 1),
            'uptime_hours': round(random.uniform(720, 8760), 1),  # Between 1 month and 1 year
            'security_score': round(random.uniform(75, 95), 1),
            'avg_response_time': round(random.uniform(0.8, 2.5), 2),
            'power_efficiency': round(random.uniform(85, 98), 1),
            'system_load': round(current_data.get('system_status', {}).get('cpu_usage', 35), 1)
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Export the Flask app for Vercel
# Vercel will automatically handle the WSGI interface 