# backend/ingest_data.py
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from database import SessionLocal, engine, create_database
from models import Base, Device, PowerReading, Alert, AttackDetection, SystemMetrics
import os
from datetime import datetime, timedelta
import random

def ingest_sample_data():
    """
    Complete data ingestion script that populates the database with:
    1. Device information
    2. Historical power readings from CSV
    3. Sample alerts
    4. Attack detection records
    5. System metrics
    """
    
    print("🚀 Starting HackSky Database Ingestion...")
    
    # Create all tables
    create_database()
    
    # Get database session
    db = SessionLocal()
    
    try:
        # Clear existing data (optional - remove in production)
        print("🗑️ Clearing existing data...")
        db.query(SystemMetrics).delete()
        db.query(AttackDetection).delete()
        db.query(Alert).delete()
        db.query(PowerReading).delete()
        db.query(Device).delete()
        db.commit()
        
        # Step 1: Ingest Devices
        print("📱 Creating device records...")
        devices_data = [
            {"device_id_str": "motor_controller_1", "device_name": "Primary Motor Controller", "device_type": "controller", "location": "Pump Station A"},
            {"device_id_str": "plc_001", "device_name": "Main PLC Unit", "device_type": "plc", "location": "Control Room"},
            {"device_id_str": "hmi_station", "device_name": "HMI Workstation", "device_type": "hmi", "location": "Control Room"},
            {"device_id_str": "scada_server", "device_name": "SCADA Server", "device_type": "server", "location": "Server Room"},
            {"device_id_str": "sensor_array", "device_name": "Environmental Sensors", "device_type": "sensor", "location": "Field"},
            {"device_id_str": "water_pump_1", "device_name": "Primary Water Pump", "device_type": "pump", "location": "Pump Station A"},
            {"device_id_str": "water_pump_2", "device_name": "Secondary Water Pump", "device_type": "pump", "location": "Pump Station B"},
            {"device_id_str": "booster_pump", "device_name": "Pressure Booster Pump", "device_type": "pump", "location": "Distribution"},
            {"device_id_str": "flow_sensor_array", "device_name": "Flow Monitoring Sensors", "device_type": "sensor", "location": "Pipeline"},
            {"device_id_str": "pressure_sensors", "device_name": "Pressure Monitoring", "device_type": "sensor", "location": "Distribution"}
        ]
        
        device_map = {}
        for device_data in devices_data:
            device = Device(**device_data)
            db.add(device)
            db.flush()  # Get the ID
            device_map[device_data["device_id_str"]] = device.id
        
        db.commit()
        print(f"✅ Created {len(devices_data)} devices")
        
        # Step 2: Ingest Power Readings from CSV
        print("⚡ Ingesting power consumption data...")
        
        # Check if CSV exists
        script_dir = os.path.dirname(__file__)
        project_root = os.path.abspath(os.path.join(script_dir, '..'))
        csv_file = os.path.join(project_root, 'data', 'power_consumption.csv')
        
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            print(f"📄 Loaded {len(df)} rows from CSV")
            
            # Ingest readings in chunks for efficiency
            chunk_size = 500
            total_readings = 0
            
            for i in range(0, len(df), chunk_size):
                chunk = df[i:i+chunk_size]
                readings_to_add = []
                
                for _, row in chunk.iterrows():
                    if row['device_id'] in device_map:
                        # Add some realistic anomaly detection
                        is_anomaly = row['power_consumption'] > 150 or random.random() < 0.05
                        anomaly_score = random.uniform(0.8, 1.0) if is_anomaly else random.uniform(0.0, 0.3)
                        
                        reading = PowerReading(
                            timestamp=row['timestamp'],
                            power_consumption=row['power_consumption'],
                            voltage=row.get('voltage'),
                            current=row.get('current'),
                            temperature=random.uniform(20, 35) if random.random() > 0.3 else None,
                            humidity=random.uniform(40, 80) if random.random() > 0.3 else None,
                            is_anomaly=is_anomaly,
                            anomaly_score=anomaly_score,
                            device_id=device_map[row['device_id']]
                        )
                        readings_to_add.append(reading)
                
                db.bulk_save_objects(readings_to_add)
                db.commit()
                total_readings += len(readings_to_add)
                print(f"📊 Ingested chunk {i//chunk_size + 1}/{(len(df)//chunk_size)+1}")
            
            print(f"✅ Ingested {total_readings} power readings")
        else:
            print("⚠️ CSV file not found, generating synthetic power data...")
            # Generate synthetic data for the last 24 hours
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=24)
            current_time = start_time
            
            synthetic_readings = []
            while current_time <= end_time:
                for device_str, device_id in device_map.items():
                    # Generate realistic power consumption based on device type
                    base_power = {
                        "motor_controller_1": 130,
                        "plc_001": 85,
                        "hmi_station": 45,
                        "scada_server": 200,
                        "sensor_array": 25,
                        "water_pump_1": 120,
                        "water_pump_2": 115,
                        "booster_pump": 125,
                        "flow_sensor_array": 45,
                        "pressure_sensors": 30
                    }.get(device_str, 50)
                    
                    # Add realistic variation
                    power = base_power + random.uniform(-10, 20)
                    is_anomaly = random.random() < 0.02  # 2% anomaly rate
                    if is_anomaly:
                        power += random.uniform(30, 80)  # Anomalous spike
                    
                    reading = PowerReading(
                        timestamp=current_time,
                        power_consumption=power,
                        voltage=220 + random.uniform(-5, 5),
                        current=power/220 + random.uniform(-0.1, 0.1),
                        temperature=random.uniform(20, 35),
                        humidity=random.uniform(40, 80),
                        is_anomaly=is_anomaly,
                        anomaly_score=random.uniform(0.8, 1.0) if is_anomaly else random.uniform(0.0, 0.3),
                        device_id=device_id
                    )
                    synthetic_readings.append(reading)
                
                current_time += timedelta(minutes=5)
            
            # Bulk insert synthetic data
            db.bulk_save_objects(synthetic_readings)
            db.commit()
            print(f"✅ Generated {len(synthetic_readings)} synthetic power readings")
        
        # Step 3: Create Sample Alerts
        print("🚨 Creating sample alerts...")
        sample_alerts = [
            {
                "alert_type": "critical",
                "severity": "high",
                "title": "Power Consumption Spike Detected",
                "message": "Motor Controller 1 showing abnormal power consumption (+47% above baseline)",
                "system": "Power Management",
                "device_id": device_map.get("motor_controller_1")
            },
            {
                "alert_type": "warning",
                "severity": "medium",
                "title": "HMI Connection Timeout",
                "message": "Intermittent connection issues detected with HMI station",
                "system": "Network",
                "device_id": device_map.get("hmi_station")
            },
            {
                "alert_type": "info",
                "severity": "low",
                "title": "Scheduled Maintenance Due",
                "message": "Water Pump 2 scheduled for maintenance in 2 days",
                "system": "Maintenance",
                "device_id": device_map.get("water_pump_2")
            },
            {
                "alert_type": "critical",
                "severity": "critical",
                "title": "Potential Cyber Attack Detected",
                "message": "Unusual network traffic pattern detected from SCADA server",
                "system": "Security",
                "device_id": device_map.get("scada_server")
            }
        ]
        
        for alert_data in sample_alerts:
            alert = Alert(**alert_data)
            db.add(alert)
        
        db.commit()
        print(f"✅ Created {len(sample_alerts)} sample alerts")
        
        # Step 4: Create Attack Detection Records
        print("🛡️ Creating attack detection records...")
        attack_types = [
            "Flow Manipulation", "Pressure Attack", "Sensor Spoofing",
            "Pump Control", "Data Exfiltration", "Network Intrusion", "HMI Manipulation"
        ]
        
        attack_records = []
        for i in range(20):  # Create 20 attack detection records
            attack_record = AttackDetection(
                timestamp=datetime.now() - timedelta(hours=random.randint(1, 168)),  # Last week
                attack_type=random.choice(attack_types),
                confidence=random.uniform(70, 95),
                threat_level=random.choice(["Low", "Medium", "High"]),
                source_ip=f"192.168.1.{random.randint(1, 254)}",
                target_system=random.choice(list(device_map.keys())),
                description=f"Automated detection of suspicious activity",
                mitigated=random.choice([True, False]),
                device_id=random.choice(list(device_map.values()))
            )
            attack_records.append(attack_record)
        
        db.bulk_save_objects(attack_records)
        db.commit()
        print(f"✅ Created {len(attack_records)} attack detection records")
        
        # Step 5: Create System Metrics
        print("📊 Creating system metrics...")
        current_time = datetime.now()
        metrics = []
        
        # Create metrics for the last 24 hours
        for hour in range(24):
            timestamp = current_time - timedelta(hours=hour)
            
            # System-wide metrics
            metrics.extend([
                SystemMetrics(timestamp=timestamp, metric_name="total_power_consumption", 
                            metric_value=random.uniform(800, 1200), unit="kW", category="power"),
                SystemMetrics(timestamp=timestamp, metric_name="active_alerts", 
                            metric_value=random.randint(0, 5), unit="count", category="security"),
                SystemMetrics(timestamp=timestamp, metric_name="system_uptime", 
                            metric_value=random.uniform(98, 100), unit="%", category="performance"),
                SystemMetrics(timestamp=timestamp, metric_name="network_latency", 
                            metric_value=random.uniform(10, 50), unit="ms", category="performance"),
                SystemMetrics(timestamp=timestamp, metric_name="cpu_usage", 
                            metric_value=random.uniform(20, 80), unit="%", category="performance")
            ])
        
        db.bulk_save_objects(metrics)
        db.commit()
        print(f"✅ Created {len(metrics)} system metrics")
        
        print("\n🎉 Database ingestion completed successfully!")
        print(f"📊 Summary:")
        print(f"   - Devices: {len(devices_data)}")
        print(f"   - Power Readings: {db.query(PowerReading).count()}")
        print(f"   - Alerts: {len(sample_alerts)}")
        print(f"   - Attack Records: {len(attack_records)}")
        print(f"   - System Metrics: {len(metrics)}")
        
    except Exception as e:
        print(f"❌ Error during ingestion: {str(e)}")
        db.rollback()
        raise
    
    finally:
        db.close()

if __name__ == "__main__":
    ingest_sample_data()
