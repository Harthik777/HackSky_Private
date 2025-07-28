"""
Real Data Integration Module for ICS NILM System
Replace fake data with real power consumption data from actual ICS systems
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import csv
import os

class RealDataConnector:
    """Connect to real ICS data sources"""
    
    def __init__(self, data_source_type="csv"):
        self.data_source_type = data_source_type
        self.ml_model = None  # Your trained ML model
        self.anomaly_threshold = 0.8
        
    def load_csv_data(self, file_path):
        """Load real power consumption data from CSV"""
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
        # Example: Connect to Modbus RTU/TCP devices
        try:
            # Install: pip install pymodbus
            from pymodbus.client.sync import ModbusTcpClient
            
            if modbus_config:
                client = ModbusTcpClient(
                    host=modbus_config.get('host', 'localhost'),
                    port=modbus_config.get('port', 502)
                )
                
                if client.connect():
                    # Read power data from holding registers
                    result = client.read_holding_registers(
                        address=modbus_config.get('start_address', 0),
                        count=modbus_config.get('register_count', 10),
                        unit=modbus_config.get('unit_id', 1)
                    )
                    
                    if not result.isError():
                        return self.process_modbus_data(result.registers)
                        
                client.close()
                
        except ImportError:
            print("Install pymodbus for real-time data: pip install pymodbus")
        except Exception as e:
            print(f"Error connecting to Modbus: {e}")
            
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
            # Load your pre-trained model
            # Example: self.ml_model = joblib.load('path/to/your/model.pkl')
            return self.simple_anomaly_detection(power_data)
        
        # Use your actual ML model here
        predictions = self.ml_model.predict(power_data)
        return predictions
    
    def simple_anomaly_detection(self, power_data):
        """Simple statistical anomaly detection if no ML model available"""
        if len(power_data) < 10:
            return [0] * len(power_data)  # No anomalies for small datasets
        
        mean_power = np.mean(power_data)
        std_power = np.std(power_data)
        
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
        if os.path.exists(csv_file):
            df = self.load_csv_data(csv_file)
            if df is not None:
                return self.format_dashboard_data(df, hours_back)
        
        # Option 2: Connect to real-time systems
        modbus_config = {
            'host': os.getenv('MODBUS_HOST', 'localhost'),
            'port': int(os.getenv('MODBUS_PORT', 502)),
            'start_address': 0,
            'register_count': 10,
            'unit_id': 1
        }
        
        real_time_data = self.load_real_time_data(modbus_config)
        if real_time_data:
            return self.format_real_time_data(real_time_data)
        
        # Option 3: Fallback to simulated data (original behavior)
        return self.get_simulated_data(hours_back)
    
    def format_dashboard_data(self, df, hours_back):
        """Format real CSV data for dashboard consumption"""
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
        anomalies = self.apply_ml_model(power_values.reshape(-1, 1))
        
        # Format for dashboard
        dashboard_data = []
        for i, row in grouped.iterrows():
            dashboard_data.append({
                'time': row['time_group'].strftime('%H:%M'),
                'power': round(row['power_consumption'], 1),
                'normal': round(np.mean(power_values), 1),  # Expected normal range
                'anomaly': round(row['power_consumption'], 1) if anomalies[i] == 1 else None
            })
        
        return dashboard_data[-10:]  # Return last 10 data points
    
    def format_real_time_data(self, power_readings):
        """Format real-time data for dashboard"""
        current_time = datetime.now()
        dashboard_data = []
        
        for i, power in enumerate(power_readings):
            time_point = current_time - timedelta(minutes=(len(power_readings) - i) * 5)
            dashboard_data.append({
                'time': time_point.strftime('%H:%M'),
                'power': round(power, 1),
                'normal': round(np.mean(power_readings), 1),
                'anomaly': round(power, 1) if abs(power - np.mean(power_readings)) > np.std(power_readings) * 2 else None
            })
        
        return dashboard_data
    
    def get_simulated_data(self, hours_back):
        """Fallback simulated data (original implementation)"""
        data = []
        base_time = datetime.now() - timedelta(hours=hours_back)
        
        for i in range(10):
            time_point = base_time + timedelta(minutes=i*6)
            normal_power = 850 + np.random.uniform(-20, 20)
            
            # Simulate occasional anomalies
            if np.random.random() > 0.9:
                anomaly_power = normal_power + np.random.uniform(50, 100)
            else:
                anomaly_power = None
                
            data.append({
                'time': time_point.strftime('%H:%M'),
                'power': round(normal_power + np.random.uniform(-10, 10)),
                'normal': round(normal_power),
                'anomaly': round(anomaly_power) if anomaly_power else None
            })
        
        return data

# Example usage for your data integration
"""
# Save this as instructions for integrating your real data:

1. CSV DATA INTEGRATION:
   - Create folder: mkdir data/
   - Put your CSV file: data/power_consumption.csv
   - Required columns: timestamp, device_id, power_consumption
   - Example format:
     timestamp,device_id,power_consumption,voltage,current
     2024-01-01 10:00:00,motor_01,125.5,220.1,0.57
     2024-01-01 10:05:00,motor_01,130.2,219.8,0.59

2. REAL-TIME MODBUS INTEGRATION:
   - Install: pip install pymodbus
   - Set environment variables:
     export MODBUS_HOST=192.168.1.100
     export MODBUS_PORT=502
   - Configure your device addresses in modbus_config

3. ML MODEL INTEGRATION:
   - Train your 1D CNN/LSTM model
   - Save model: joblib.dump(model, 'models/anomaly_detector.pkl')
   - Load in RealDataConnector.__init__()

4. CUSTOM SENSOR INTEGRATION:
   - Modify convert_raw_to_power() for your sensor specifications
   - Update process_modbus_data() for your data format
   - Adjust anomaly_threshold based on your system requirements
""" 