"""
WADI Dataset Integration for ICS Cybersecurity Dashboard
Singapore University of Technology and Design (SUTD) Water Distribution Dataset
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
import os
import random
import math

# Optional scikit-learn imports
try:
    from sklearn.preprocessing import StandardScaler
    from sklearn.ensemble import IsolationForest
    sklearn_available = True
except ImportError:
    sklearn_available = False
    print("Warning: scikit-learn not available")

class WADIDataConnector:
    """Specialized connector for WADI (Water Distribution) dataset"""
    
    def __init__(self):
        self.dataset_path = 'data/wadi/'
        if sklearn_available:
            self.scaler = StandardScaler()
            self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        else:
            self.scaler = None
            self.anomaly_detector = None
        self.sensor_mapping = self.get_wadi_sensor_mapping()
        self.attack_labels = {}
        
    def get_wadi_sensor_mapping(self):
        """Map WADI sensor codes to readable names"""
        return {
            # Flow Sensors
            'FIT_101': 'Raw Water Flow',
            'FIT_201': 'Process Water Flow', 
            'FIT_301': 'Distribution Flow',
            'FIT_401': 'Consumer Flow',
            'FIT_501': 'Return Flow',
            'FIT_601': 'Waste Flow',
            
            # Level Sensors  
            'LIT_101': 'Raw Water Tank Level',
            'LIT_301': 'Clean Water Tank Level',
            'LIT_401': 'Distribution Tank Level',
            
            # Pressure Sensors
            'PIT_201': 'Process Pressure',
            'PIT_301': 'Distribution Pressure', 
            'PIT_401': 'Consumer Pressure',
            'PIT_501': 'Return Pressure',
            
            # Conductivity/Quality
            'AIT_201': 'Water Quality Analyzer',
            'AIT_202': 'pH Level',
            'AIT_203': 'ORP Level',
            
            # Pump States (Actuators)
            'P_101': 'Raw Water Pump',
            'P_201': 'Booster Pump 1',
            'P_202': 'Booster Pump 2', 
            'P_301': 'Distribution Pump',
            'P_401': 'Consumer Pump',
            'P_501': 'Return Pump',
            'P_601': 'Waste Pump',
            
            # Valve States
            'MV_101': 'Raw Water Valve',
            'MV_201': 'Process Valve',
            'MV_301': 'Distribution Valve',
            'MV_401': 'Consumer Valve',
            
            # UV Treatment
            'UV_401': 'UV Disinfection System',
            
            # Chemical Dosing
            'P_203': 'Chemical Dosing Pump',
            'P_205': 'Backwash Pump'
        }
    
    def load_wadi_data(self, attack_type='normal'):
        """Load WADI dataset files"""
        if not pandas_available:
            print("pandas not available, cannot load WADI data")
            return None
            
        try:
            if attack_type == 'normal':
                # Load normal operation data
                normal_file = os.path.join(self.dataset_path, 'WADI_14days.csv')
                if os.path.exists(normal_file):
                    df = pd.read_csv(normal_file)
                    print(f"✅ Loaded WADI normal data: {len(df)} records")
                    return self.process_wadi_dataframe(df, has_attacks=False)
            else:
                # Load attack data
                attack_file = os.path.join(self.dataset_path, 'WADI_attackdata.csv')
                if os.path.exists(attack_file):
                    df = pd.read_csv(attack_file)
                    print(f"✅ Loaded WADI attack data: {len(df)} records")
                    return self.process_wadi_dataframe(df, has_attacks=True)
                    
        except Exception as e:
            print(f"Error loading WADI data: {e}")
            return None
        
        return None
    
    def process_wadi_dataframe(self, df, has_attacks=False):
        """Process raw WADI dataframe into dashboard format"""
        if not pandas_available:
            return None
            
        try:
            # Handle timestamp column (different formats in WADI)
            timestamp_cols = ['Timestamp', 'Date Time', 'DateTime', 'Time']
            timestamp_col = None
            
            for col in timestamp_cols:
                if col in df.columns:
                    timestamp_col = col
                    break
            
            if timestamp_col:
                df['timestamp'] = pd.to_datetime(df[timestamp_col])
            else:
                # Create synthetic timestamps if none found
                df['timestamp'] = pd.date_range(
                    start='2024-01-28 00:00:00', 
                    periods=len(df), 
                    freq='2S'  # WADI typically has 2-second intervals
                )
            
            # Extract attack labels if present
            if has_attacks and 'Attack LABLE (1:No Attack, -1:Attack)' in df.columns:
                df['is_attack'] = df['Attack LABLE (1:No Attack, -1:Attack)'] == -1
            elif has_attacks and 'Label' in df.columns:
                df['is_attack'] = df['Label'] == -1
            else:
                df['is_attack'] = False
            
            # Select sensor columns (exclude timestamp and label columns)
            sensor_cols = [col for col in df.columns 
                          if col not in ['timestamp', 'is_attack', 'Timestamp', 'Date Time', 
                                       'DateTime', 'Time', 'Attack LABLE (1:No Attack, -1:Attack)', 'Label']]
            
            print(f"📊 Processing {len(sensor_cols)} WADI sensors")
            return df[['timestamp', 'is_attack'] + sensor_cols]
            
        except Exception as e:
            print(f"Error processing WADI dataframe: {e}")
            return None
    
    def get_power_equivalent_data(self, hours_back=1):
        """Convert WADI sensor data to power consumption equivalent for dashboard"""
        
        # Try to load WADI data
        df = self.load_wadi_data('normal')  # Try normal data first
        if df is None:
            df = self.load_wadi_data('attack')  # Fallback to attack data
        
        if df is None or (pandas_available and df.empty):
            print("⚠️ No WADI data found, using simulated data")
            return self.get_simulated_wadi_data(hours_back)
        
        try:
            # Get recent data
            if pandas_available:
                end_time = df['timestamp'].max()
                start_time = end_time - timedelta(hours=hours_back)
                recent_data = df[df['timestamp'] >= start_time].copy()
                
                if recent_data.empty:
                    # Use last available data if no recent data
                    recent_data = df.tail(100).copy()
                
                # Convert sensor readings to "power consumption" equivalent
                power_data = self.convert_sensors_to_power(recent_data)
                
                return power_data[-10:]  # Return last 10 data points
            else:
                return self.get_simulated_wadi_data(hours_back)
            
        except Exception as e:
            print(f"Error processing WADI data: {e}")
            return self.get_simulated_wadi_data(hours_back)
    
    def convert_sensors_to_power(self, df):
        """Convert WADI sensor readings to power consumption equivalent"""
        if not pandas_available:
            return self.get_simulated_wadi_data(1)
            
        dashboard_data = []
        
        # Select key sensors for power calculation
        key_sensors = ['FIT_101', 'FIT_201', 'FIT_301', 'P_101', 'P_201', 'P_301']
        available_sensors = [col for col in key_sensors if col in df.columns]
        
        if not available_sensors:
            # If no key sensors, use any available numeric columns
            numeric_cols = df.select_dtypes(include=[float, int]).columns if pandas_available else []
            available_sensors = [col for col in numeric_cols if col != 'is_attack'][:5]
        
        print(f"🔍 Using WADI sensors for power calculation: {available_sensors}")
        
        # Group data into time intervals
        df['time_interval'] = df['timestamp'].dt.floor('5min')
        agg_dict = {sensor: 'mean' for sensor in available_sensors}
        agg_dict['is_attack'] = 'any'
        grouped = df.groupby('time_interval').agg(agg_dict).reset_index()
        
        for _, row in grouped.iterrows():
            # Calculate equivalent "power consumption" from sensor readings
            power_value = 0
            
            for sensor in available_sensors:
                if sensor in row and not (pandas_available and pd.isna(row[sensor])):
                    sensor_val = row[sensor] if row[sensor] is not None else 0
                    # Convert sensor readings to power equivalent
                    if 'FIT' in sensor:  # Flow sensors
                        power_value += abs(sensor_val) * 10  # Flow contributes to power
                    elif 'P_' in sensor:  # Pump states
                        power_value += sensor_val * 100  # Pumps consume significant power
                    elif 'LIT' in sensor:  # Level sensors
                        power_value += abs(sensor_val) * 5  # Level affects pump power
                    elif 'PIT' in sensor:  # Pressure sensors
                        power_value += abs(sensor_val) * 8  # Pressure affects power
                    else:
                        power_value += abs(sensor_val) * 2  # Other sensors
            
            # Normalize to realistic power range (500-1200 kW)
            normalized_power = 500 + (power_value % 700)
            
            # Check for anomalies
            is_anomaly = row.get('is_attack', False) if 'is_attack' in row else False
            anomaly_power = normalized_power * 1.3 if is_anomaly else None
            
            # Calculate moving average for normal power
            recent_powers = [item['power'] for item in dashboard_data[-5:]] if dashboard_data else [normalized_power]
            avg_power = sum(recent_powers) / len(recent_powers)
            
            dashboard_data.append({
                'time': row['time_interval'].strftime('%H:%M'),
                'power': round(normalized_power, 1),
                'normal': round(avg_power, 1),
                'anomaly': round(anomaly_power, 1) if anomaly_power else None
            })
        
        return dashboard_data
    
    def get_current_data(self):
        """Get current data for the ICS monitor"""
        try:
            # Get power equivalent data
            power_data = self.get_power_equivalent_data(hours_back=0.1)
            if power_data:
                latest = power_data[-1]
                return {
                    'timestamp': datetime.now().isoformat(),
                    'power_consumption': latest['power'],
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
            print(f"Error getting WADI current data: {e}")
        
        return None
    
    def get_simulated_wadi_data(self, hours_back):
        """Fallback simulated data that mimics WADI characteristics"""
        data = []
        base_time = datetime.now() - timedelta(hours=hours_back)
        
        for i in range(10):
            time_point = base_time + timedelta(minutes=i*6)
            
            # Simulate water distribution system power consumption
            base_power = 650 + random.uniform(-50, 50)  # Water systems typically 600-700 kW
            
            # Add realistic variations based on water demand patterns
            hour = time_point.hour
            if 6 <= hour <= 10 or 18 <= hour <= 22:  # Peak demand times
                base_power += 100
            elif 0 <= hour <= 5:  # Low demand overnight
                base_power -= 80
            
            # Simulate cyber attack anomalies (WADI-style)
            if random.random() > 0.85:  # 15% chance of attack simulation
                anomaly_power = base_power * 1.4  # Significant deviation during attacks
            else:
                anomaly_power = None
                
            data.append({
                'time': time_point.strftime('%H:%M'),
                'power': round(base_power + random.uniform(-20, 20)),
                'normal': round(base_power),
                'anomaly': round(anomaly_power) if anomaly_power else None
            })
        
        return data 