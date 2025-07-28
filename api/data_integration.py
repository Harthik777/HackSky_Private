"""
Real Data Integration Module for ICS NILM System
Replace fake data with real power consumption data from actual ICS systems
"""

try:
    import pandas as pd
    pandas_available = True
except ImportError:
    pandas_available = False
    print("Warning: pandas not available")

try:
    import numpy as np
    numpy_available = True
except ImportError:
    numpy_available = False
    print("Warning: numpy not available")

from datetime import datetime, timedelta
import json
import csv
import os
import random
import math

class RealDataConnector:
    """Connect to real ICS data sources"""
    
    def __init__(self, data_source_type="csv"):
        self.data_source_type = data_source_type
        self.ml_model = None  # Your trained ML model
        self.anomaly_threshold = 0.8
        
    def normalvariate_fallback(self, mu, sigma):
        """Fallback normal distribution using Python's random and math"""
        return random.gauss(mu, sigma)
        
    def load_csv_data(self, file_path):
        """Load real power consumption data from CSV"""
        if not pandas_available:
            print("pandas not available, cannot load CSV data")
            return None
            
        try:
            # Expected CSV format: timestamp, device_id, power_consumption, voltage, current
            df = pd.read_csv(file_path)
            required_columns = ['timestamp', 'device_id', 'power_consumption']
            
            if not all(col in df.columns for col in required_columns):
                raise ValueError(f"CSV must contain columns: {required_columns}")
                
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
            
        except Exception as e:
            print(f"Error loading CSV data: {e}")
            return None
    
    def load_real_time_data(self, modbus_config=None):
        """Connect to real-time ICS systems via Modbus/OPC-UA"""
        # Note: pymodbus removed from requirements to avoid build issues
        print("Real-time Modbus connection not available in serverless environment")
        return None
    
    def process_modbus_data(self, registers):
        """Process raw Modbus register data into power metrics"""
        # Convert register values to actual power readings
        power_data = []
        for i in range(0, len(registers), 2):
            if i + 1 < len(registers):
                # Combine two 16-bit registers into 32-bit float
                raw_value = (registers[i] << 16) | registers[i + 1]
                power_value = self.convert_raw_to_power(raw_value)
                power_data.append(power_value)
        
        return power_data
    
    def convert_raw_to_power(self, raw_value):
        """Convert raw sensor values to actual power readings"""
        # Implement your specific conversion formula
        # Example: assuming linear conversion
        scale_factor = 0.1  # Adjust based on your sensors
        offset = 0
        return (raw_value * scale_factor) + offset
    
    def apply_ml_model(self, power_data):
        """Apply your trained ML model for anomaly detection"""
        if self.ml_model is None:
            return self.simple_anomaly_detection(power_data)
        
        # Use your actual ML model here
        predictions = self.ml_model.predict(power_data)
        return predictions
    
    def simple_anomaly_detection(self, power_data):
        """Simple statistical anomaly detection if no ML model available"""
        if len(power_data) < 10:
            return [0] * len(power_data)  # No anomalies for small datasets
        
        if numpy_available:
            mean_power = np.mean(power_data)
            std_power = np.std(power_data)
        else:
            mean_power = sum(power_data) / len(power_data)
            variance = sum((x - mean_power) ** 2 for x in power_data) / len(power_data)
            std_power = math.sqrt(variance)
        
        anomalies = []
        for power in power_data:
            # Flag as anomaly if beyond 2 standard deviations
            z_score = abs((power - mean_power) / std_power) if std_power > 0 else 0
            anomalies.append(1 if z_score > 2 else 0)
        
        return anomalies
    
    def get_real_power_data(self, hours_back=1):
        """Get real power consumption data for the dashboard"""
        # Try different data sources in order of preference
        
        # Option 1: Load from CSV file (most common for hackathons)
        csv_file = 'data/power_consumption.csv'
        if os.path.exists(csv_file) and pandas_available:
            df = self.load_csv_data(csv_file)
            if df is not None:
                return self.format_dashboard_data(df, hours_back)
        
        # Option 2: Connect to real-time systems (not available in serverless)
        print("Real-time data connection not available, using simulated data")
        
        # Option 3: Fallback to simulated data (original behavior)
        return self.get_simulated_data(hours_back)
    
    def format_dashboard_data(self, df, hours_back):
        """Format real CSV data for dashboard consumption"""
        if not pandas_available:
            return self.get_simulated_data(hours_back)
            
        # Get recent data
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours_back)
        
        # Filter by time range
        recent_data = df[df['timestamp'] >= start_time].copy()
        
        if recent_data.empty:
            return self.get_simulated_data(hours_back)
        
        # Group by time intervals (e.g., 5-minute intervals)
        recent_data['time_group'] = recent_data['timestamp'].dt.floor('5min')
        grouped = recent_data.groupby('time_group')['power_consumption'].mean().reset_index()
        
        # Apply anomaly detection
        power_values = grouped['power_consumption'].values
        anomalies = self.apply_ml_model(power_values.reshape(-1, 1) if numpy_available else power_values)
        
        # Format for dashboard
        dashboard_data = []
        mean_power = sum(power_values) / len(power_values) if power_values else 0
        
        for i, row in grouped.iterrows():
            dashboard_data.append({
                'time': row['time_group'].strftime('%H:%M'),
                'power': round(row['power_consumption'], 1),
                'normal': round(mean_power, 1),  # Expected normal range
                'anomaly': round(row['power_consumption'], 1) if anomalies[i] == 1 else None
            })
        
        return dashboard_data[-10:]  # Return last 10 data points
    
    def format_real_time_data(self, power_readings):
        """Format real-time data for dashboard"""
        current_time = datetime.now()
        dashboard_data = []
        
        mean_power = sum(power_readings) / len(power_readings) if power_readings else 0
        if numpy_available:
            std_power = np.std(power_readings)
        else:
            variance = sum((x - mean_power) ** 2 for x in power_readings) / len(power_readings)
            std_power = math.sqrt(variance)
        
        for i, power in enumerate(power_readings):
            time_point = current_time - timedelta(minutes=(len(power_readings) - i) * 5)
            is_anomaly = abs(power - mean_power) > std_power * 2
            dashboard_data.append({
                'time': time_point.strftime('%H:%M'),
                'power': round(power, 1),
                'normal': round(mean_power, 1),
                'anomaly': round(power, 1) if is_anomaly else None
            })
        
        return dashboard_data
    
    def get_simulated_data(self, hours_back):
        """Fallback simulated data (original implementation)"""
        data = []
        base_time = datetime.now() - timedelta(hours=hours_back)
        
        for i in range(10):
            time_point = base_time + timedelta(minutes=i*6)
            normal_power = 850 + random.uniform(-20, 20)
            
            # Simulate occasional anomalies
            if random.random() > 0.9:
                anomaly_power = normal_power + random.uniform(50, 100)
            else:
                anomaly_power = None
                
            data.append({
                'time': time_point.strftime('%H:%M'),
                'power': round(normal_power + random.uniform(-10, 10)),
                'normal': round(normal_power),
                'anomaly': round(anomaly_power) if anomaly_power else None
            })
        
        return data
    
    def get_current_data(self):
        """Get current data for the ICS monitor"""
        try:
            return {
                'timestamp': datetime.now().isoformat(),
                'power_consumption': 45 + random.uniform(-15, 15),
                'network_traffic': random.uniform(45, 75),
                'temperature': random.uniform(68, 76),
                'pressure': random.uniform(14.2, 15.2),
                'flow_rate': random.uniform(130, 170),
                'sensor_readings': {
                    f'sensor_{i}': random.uniform(40, 60) for i in range(1, 13)
                },
                'system_status': {
                    'cpu_usage': random.uniform(25, 45),
                    'memory_usage': random.uniform(50, 80),
                    'disk_usage': random.uniform(30, 50)
                },
                'network_metrics': {
                    'latency': random.uniform(10, 20),
                    'packet_loss': random.uniform(0, 0.5),
                    'bandwidth_utilization': random.uniform(35, 55)
                }
            }
        except Exception as e:
            print(f"Error getting current data: {e}")
            return None 