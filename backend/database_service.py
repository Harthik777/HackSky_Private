# backend/database_service.py
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc, and_
from database import SessionLocal
from models import Device, PowerReading, Alert, AttackDetection
from datetime import datetime, timedelta
from typing import List, Dict

class DatabaseService:
    """
    Service layer for all database operations.
    Provides clean, reusable methods for the Flask API.
    """
    
    def get_session(self) -> Session:
        """Get a database session"""
        return SessionLocal()
    
    def get_recent_power_data(self, minutes: int = 60, limit: int = 100) -> List[Dict]:
        """Get recent power consumption data for charts"""
        db = self.get_session()
        try:
            cutoff_time = datetime.now() - timedelta(minutes=minutes)
            
            # Eagerly load the related device to avoid N+1 queries
            readings = db.query(PowerReading).options(
                joinedload(PowerReading.device)
            ).filter(PowerReading.timestamp >= cutoff_time)\
             .order_by(desc(PowerReading.timestamp))\
             .limit(limit)\
             .all()
            
            formatted_data = []
            # Reverse in Python to maintain chronological order for the chart
            for reading in reversed(readings):
                formatted_data.append({
                    "time": reading.timestamp.strftime('%H:%M'),
                    "power": round(reading.power_consumption, 2),
                    "voltage": round(reading.voltage or 0, 2),
                    "current": round(reading.current or 0, 2),
                    "normal": 130,  # Baseline for chart visualization
                    "anomaly": reading.power_consumption if reading.is_anomaly else None,
                    "device": reading.device.device_name if reading.device else "Unknown"
                })
            
            return formatted_data
            
        finally:
            db.close()
    
    def get_system_status(self) -> Dict:
        """
        --- OPTIMIZED: Get current system status including device health ---
        This version uses an efficient single query to avoid the N+1 problem.
        """
        db = self.get_session()
        try:
            # Subquery to find the ID of the latest reading for each device
            latest_reading_subquery = db.query(
                PowerReading.device_id,
                func.max(PowerReading.id).label('max_id')
            ).group_by(PowerReading.device_id).subquery()

            # Main query to join devices with their single latest reading
            results = db.query(
                Device,
                PowerReading
            ).outerjoin(
                latest_reading_subquery,
                Device.id == latest_reading_subquery.c.device_id
            ).outerjoin(
                PowerReading,
                PowerReading.id == latest_reading_subquery.c.max_id
            ).all()

            systems = {}
            total_power = 0
            online_count = 0
            anomaly_count = 0
            total_devices = len(results)

            for device, latest_reading in results:
                is_anomaly = False
                power = 0
                last_seen = None
                
                if latest_reading:
                    total_power += latest_reading.power_consumption
                    is_anomaly = latest_reading.is_anomaly
                    if is_anomaly:
                        anomaly_count += 1
                    power = round(latest_reading.power_consumption, 2)
                    last_seen = latest_reading.timestamp.isoformat()

                # Determine device status based on the latest reading's timestamp
                if latest_reading and (datetime.now() - latest_reading.timestamp).total_seconds() < 600: # 10 minutes
                    status = 'warning' if is_anomaly else 'online'
                    if status == 'online':
                        online_count += 1
                else:
                    status = 'offline'
                
                systems[device.device_id_str] = {
                    'status': status,
                    'power': power,
                    'anomaly': is_anomaly,
                    'last_seen': last_seen
                }
            
            return {
                'systems': systems,
                'summary': {
                    'total_devices': total_devices,
                    'online_devices': online_count,
                    'total_power': round(total_power, 2),
                    'anomaly_count': anomaly_count
                }
            }
            
        finally:
            db.close()

    def get_alerts(self, limit: int = 50, unacknowledged_only: bool = False) -> List[Dict]:
        """Get system alerts"""
        db = self.get_session()
        try:
            query = db.query(Alert).options(joinedload(Alert.device))
            
            if unacknowledged_only:
                query = query.filter(Alert.acknowledged == False)
            
            alerts = query.order_by(desc(Alert.timestamp))\
                         .limit(limit)\
                         .all()
            
            return [
                {
                    'id': alert.id,
                    'type': alert.alert_type,
                    'severity': alert.severity,
                    'title': alert.title,
                    'message': alert.message,
                    'system': alert.system,
                    'timestamp': alert.timestamp.isoformat(),
                    'acknowledged': alert.acknowledged,
                    'device': alert.device.device_name if alert.device else "System"
                } for alert in alerts
            ]
            
        finally:
            db.close()
    
    def get_attack_analysis(self) -> Dict:
        """Get attack detection analysis"""
        db = self.get_session()
        try:
            cutoff_time = datetime.now() - timedelta(hours=24)
            detections = db.query(AttackDetection)\
                          .filter(AttackDetection.timestamp >= cutoff_time)\
                          .all()
            
            attack_summary = {}
            total_detections = len(detections)
            high_confidence_attacks = sum(1 for d in detections if d.confidence > 85)
            
            for detection in detections:
                attack_type = detection.attack_type
                if attack_type not in attack_summary:
                    attack_summary[attack_type] = {'count': 0, 'total_confidence': 0}
                attack_summary[attack_type]['count'] += 1
                attack_summary[attack_type]['total_confidence'] += detection.confidence
            
            if high_confidence_attacks > 5: overall_threat = 'High'
            elif high_confidence_attacks > 2: overall_threat = 'Medium'
            else: overall_threat = 'Low'
            
            return {
                'total_detections': total_detections,
                'high_confidence_attacks': high_confidence_attacks,
                'overall_threat_level': overall_threat,
                'attack_types': [
                    {
                        'type': attack_type,
                        'probability': round(data['total_confidence'] / data['count'], 1) if data['count'] > 0 else 0,
                        'detected': data['count']
                    } for attack_type, data in attack_summary.items()
                ]
            }
        finally:
            db.close()
    
    def get_statistics(self) -> Dict:
        """Get dashboard statistics"""
        db = self.get_session()
        try:
            device_count = db.query(Device).count()
            alert_count = db.query(Alert).filter(Alert.acknowledged == False).count()
            
            # Get the single most recent power reading for total power
            latest_power_reading = db.query(func.sum(PowerReading.power_consumption)).scalar()

            active_devices = db.query(Device.id)\
                              .join(PowerReading)\
                              .filter(PowerReading.timestamp >= datetime.now() - timedelta(minutes=10))\
                              .distinct()\
                              .count()
            
            return {
                'systems_monitored': device_count,
                'active_alerts': alert_count,
                'power_consumption': f"{round(latest_power_reading or 0, 2)} kW",
                'detection_accuracy': "99.7%", # Static value for demo
            }
        finally:
            db.close()

# Global service instance
db_service = DatabaseService()
