#!/usr/bin/env python3
"""
Generate real-time data for HackSky dashboard
This script populates the database with current timestamps
"""

import sys
import os
from pathlib import Path
import random
import numpy as np
from datetime import datetime, timedelta

def setup_imports():
    """Setup proper imports for backend modules"""
    script_dir = Path(__file__).parent.resolve()
    backend_dir = script_dir / 'backend'
    
    if str(backend_dir) not in sys.path:
        sys.path.insert(0, str(backend_dir))
    
    original_cwd = os.getcwd()
    os.chdir(script_dir)
    return original_cwd

def generate_real_time_data():
    """Generate real-time power monitoring data"""
    setup_imports()
    
    try:
        from database import SessionLocal
        from models import Device, PowerReading, Alert, AttackDetection
        from datetime import datetime, timedelta
        
        print("🚀 Generating Real-Time Data for HackSky...")
        
        db = SessionLocal()
        
        # Get existing devices
        devices = db.query(Device).all()
        if not devices:
            print("❌ No devices found. Run setup_database.py first.")
            return
        
        # Clear old power readings
        db.query(PowerReading).delete()
        db.query(Alert).delete()
        db.query(AttackDetection).delete()
        db.commit()
        
        print("🗑️ Cleared old data...")
        
        # Generate power readings for the last 2 hours with current timestamps
        current_time = datetime.now()
        start_time = current_time - timedelta(hours=2)
        
        readings = []
        alerts = []
        attacks = []
        
        # Generate data every 5 minutes for the last 2 hours
        time_points = []
        current = start_time
        while current <= current_time:
            time_points.append(current)
            current += timedelta(minutes=5)
        
        print(f"📊 Generating {len(time_points)} time points...")
        
        for i, timestamp in enumerate(time_points):
            for device in devices[:5]:  # Use first 5 devices
                # Generate realistic power consumption with some anomalies
                base_power = 120 + random.gauss(0, 10)
                
                # Add some anomalies (10% chance)
                is_anomaly = random.random() < 0.1
                if is_anomaly:
                    base_power += random.gauss(0, 50)  # Large deviation
                
                # Ensure positive values
                power = max(50, base_power)
                
                # Generate correlated voltage and current
                voltage = 220 + random.gauss(0, 5)
                current = power / voltage if voltage > 0 else 0.5
                
                reading = PowerReading(
                    timestamp=timestamp,
                    power_consumption=round(power, 2),
                    voltage=round(voltage, 2),
                    current=round(current, 3),
                    frequency=50.0 + random.gauss(0, 0.1),
                    temperature=25 + random.gauss(0, 5),
                    humidity=45 + random.gauss(0, 10),
                    is_anomaly=is_anomaly,
                    anomaly_score=abs(random.gauss(0, 1)) if is_anomaly else 0.1,
                    device_id=device.id
                )
                readings.append(reading)
                
                # Generate alerts for anomalies
                if is_anomaly:
                    alert = Alert(
                        timestamp=timestamp,
                        alert_type='warning' if power < 200 else 'critical',
                        severity='high' if power > 200 else 'medium',
                        title=f'Power Anomaly Detected - {device.device_name}',
                        message=f'Unusual power consumption: {power:.1f}kW detected',
                        device_id=device.id,
                        acknowledged=False
                    )
                    alerts.append(alert)
                    
                    # Generate attack detection for critical anomalies
                    if power > 150 or power < 60:  # Lower threshold for more attacks
                        attack_threat_level = 'Critical' if power > 180 or power < 60 else 'High'
                        attack = AttackDetection(
                            timestamp=timestamp,
                            attack_type=random.choice(['dos', 'injection', 'manipulation', 'malware', 'mitm']),
                            threat_level=attack_threat_level,
                            confidence=random.uniform(0.6, 0.95),
                            source_ip='192.168.1.' + str(random.randint(100, 200)),
                            target_system=device.device_id_str,
                            description=f'Suspicious power pattern detected: {power:.1f}kW',
                            mitigated=random.choice([True, False])
                        )
                        attacks.append(attack)
        
        # Bulk insert all data
        print(f"💾 Inserting {len(readings)} power readings...")
        db.bulk_save_objects(readings)
        
        print(f"🚨 Inserting {len(alerts)} alerts...")
        db.bulk_save_objects(alerts)
        
        print(f"🛡️ Inserting {len(attacks)} attack detections...")
        db.bulk_save_objects(attacks)
        
        db.commit()
        
        print("✅ Real-time data generation completed!")
        print(f"📊 Summary:")
        print(f"   - Power Readings: {len(readings)}")
        print(f"   - Alerts: {len(alerts)}")
        print(f"   - Attack Detections: {len(attacks)}")
        print(f"   - Time Range: {start_time.strftime('%H:%M')} - {current_time.strftime('%H:%M')}")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error generating real-time data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    generate_real_time_data()
