#!/usr/bin/env python3
"""
Generate recent power data for testing the dashboard
"""

import os
import sys

# Add backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from datetime import datetime, timedelta
import random

try:
    from database import SessionLocal
    from models import PowerReading, Device
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure you're running from the project root directory")
    print("💡 And that the backend modules are available")
    sys.exit(1)

def generate_recent_data():
    """Generate power readings for the last hour"""
    db = SessionLocal()
    try:
        # Get all devices
        devices = db.query(Device).all()
        if not devices:
            print("❌ No devices found in database")
            return
        
        print(f"📱 Found {len(devices)} devices")
        
        # Generate readings for the last hour (every 2 minutes)
        now = datetime.now()
        readings_created = 0
        
        for minutes_ago in range(0, 60, 2):  # Every 2 minutes for last hour
            timestamp = now - timedelta(minutes=minutes_ago)
            
            for device in devices:
                # Generate realistic power consumption
                base_power = 120 + random.normalvariate(0, 15)
                is_anomaly = random.random() < 0.1  # 10% chance of anomaly
                
                if is_anomaly:
                    power = base_power * random.uniform(1.5, 2.5)  # Anomalous spike
                else:
                    power = max(50, base_power)  # Normal consumption
                
                reading = PowerReading(
                    device_id=device.id,
                    timestamp=timestamp,
                    power_consumption=round(power, 2),
                    voltage=round(220 + random.normalvariate(0, 5), 2),
                    current=round(power / 220, 3),
                    temperature=round(25 + random.normalvariate(0, 3), 1),
                    is_anomaly=is_anomaly,
                    anomaly_score=random.uniform(0.8, 1.0) if is_anomaly else random.uniform(0.0, 0.3)
                )
                
                db.add(reading)
                readings_created += 1
        
        db.commit()
        print(f"✅ Created {readings_created} recent power readings")
        print(f"📊 Data spans from {(now - timedelta(minutes=60)).strftime('%H:%M')} to {now.strftime('%H:%M')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    print("🚀 Generating recent power data...")
    generate_recent_data()
    print("✅ Done!")
