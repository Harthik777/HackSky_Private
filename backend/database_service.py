# backend/database_service.py
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_, or_
from database import SessionLocal
from models import Device, PowerReading, Alert, AttackDetection, SystemMetrics
from datetime import datetime, timedelta
import json
from typing import List, Dict, Optional

class DatabaseService:
    """
    Service layer for all database operations.
    Provides clean, reusable methods for the Flask API.
    """
    
    def __init__(self):
        self.db = None
    
    def get_session(self) -> Session:
        """Get a database session"""
        return SessionLocal()
    
    def get_recent_power_data(self, minutes: int = 60, limit: int = 100) -> List[Dict]:
        """Get recent power consumption data for charts"""
        db = self.get_session()
        try:
            cutoff_time = datetime.now() - timedelta(minutes=minutes)
            
            readings = db.query(PowerReading)\
                        .filter(PowerReading.timestamp >= cutoff_time)\
                        .order_by(desc(PowerReading.timestamp))\
                        .limit(limit)\
                        .all()
            
            # Format for frontend charts
            formatted_data = []
            for reading in reversed(readings):  # Reverse to get chronological order
                formatted_data.append({
                    "time": reading.timestamp.strftime('%H:%M'),
                    "power": round(reading.power_consumption, 2),
                    "voltage": round(reading.voltage or 0, 2),
                    "current": round(reading.current or 0, 2),
                    "normal": 130,  # Baseline for comparison
                    "anomaly": reading.power_consumption if reading.is_anomaly else None,
                    "device": reading.device.device_name if reading.device else "Unknown"
                })
            
            return formatted_data
            
        finally:
            db.close()
    
    def get_system_status(self) -> Dict:
        """Get current system status including device health"""
        db = self.get_session()
        try:
            # Get all devices with latest readings
            devices = db.query(Device).all()
            
            systems = {}
            total_power = 0
            online_count = 0
            anomaly_count = 0
            
            for device in devices:
                # Get latest reading for this device
                latest_reading = db.query(PowerReading)\
                                  .filter(PowerReading.device_id == device.id)\
                                  .order_by(desc(PowerReading.timestamp))\
                                  .first()
                
                if latest_reading:
                    total_power += latest_reading.power_consumption
                    is_anomaly = latest_reading.is_anomaly
                    if is_anomaly:
                        anomaly_count += 1
                else:
                    is_anomaly = False
                
                # Determine status
                if latest_reading and (datetime.now() - latest_reading.timestamp).total_seconds() < 600:  # 10 minutes
                    status = 'warning' if is_anomaly else 'online'
                    if status == 'online':
                        online_count += 1
                else:
                    status = 'offline'
                
                systems[device.device_id_str] = {
                    'status': status,
                    'power': round(latest_reading.power_consumption, 2) if latest_reading else 0,
                    'anomaly': is_anomaly,
                    'last_seen': latest_reading.timestamp.isoformat() if latest_reading else None
                }
            
            return {
                'systems': systems,
                'summary': {
                    'total_devices': len(devices),
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
            query = db.query(Alert)
            
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
                    'device': alert.device.device_name if alert.device else None
                } for alert in alerts
            ]
            
        finally:
            db.close()
    
    def add_alert(self, alert_type: str, title: str, message: str, 
                  system: str = None, severity: str = 'medium', device_id: str = None) -> bool:
        """Add a new alert to the system"""
        db = self.get_session()
        try:
            # Find device if device_id provided
            device_db_id = None
            if device_id:
                device = db.query(Device).filter(Device.device_id_str == device_id).first()
                if device:
                    device_db_id = device.id
            
            alert = Alert(
                alert_type=alert_type,
                severity=severity,
                title=title,
                message=message,
                system=system,
                device_id=device_db_id
            )
            
            db.add(alert)
            db.commit()
            return True
            
        except Exception as e:
            db.rollback()
            print(f"Error adding alert: {e}")
            return False
        finally:
            db.close()
    
    def acknowledge_alert(self, alert_id: int, acknowledged_by: str = "system") -> bool:
        """Acknowledge an alert"""
        db = self.get_session()
        try:
            alert = db.query(Alert).filter(Alert.id == alert_id).first()
            if alert:
                alert.acknowledged = True
                alert.acknowledged_by = acknowledged_by
                alert.acknowledged_at = datetime.now()
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            print(f"Error acknowledging alert: {e}")
            return False
        finally:
            db.close()
    
    def get_attack_analysis(self) -> Dict:
        """Get attack detection analysis"""
        db = self.get_session()
        try:
            # Get recent attack detections (last 24 hours)
            cutoff_time = datetime.now() - timedelta(hours=24)
            
            detections = db.query(AttackDetection)\
                          .filter(AttackDetection.timestamp >= cutoff_time)\
                          .all()
            
            # Group by attack type
            attack_summary = {}
            total_detections = 0
            high_confidence_attacks = 0
            
            for detection in detections:
                attack_type = detection.attack_type
                if attack_type not in attack_summary:
                    attack_summary[attack_type] = {
                        'count': 0,
                        'avg_confidence': 0,
                        'threat_levels': {'Low': 0, 'Medium': 0, 'High': 0}
                    }
                
                attack_summary[attack_type]['count'] += 1
                attack_summary[attack_type]['avg_confidence'] += detection.confidence
                attack_summary[attack_type]['threat_levels'][detection.threat_level] += 1
                
                total_detections += 1
                if detection.confidence > 85:
                    high_confidence_attacks += 1
            
            # Calculate averages
            for attack_type in attack_summary:
                count = attack_summary[attack_type]['count']
                attack_summary[attack_type]['avg_confidence'] /= count
            
            # Determine overall threat level
            if high_confidence_attacks > 5:
                overall_threat = 'High'
            elif high_confidence_attacks > 2:
                overall_threat = 'Medium'
            else:
                overall_threat = 'Low'
            
            return {
                'total_detections': total_detections,
                'high_confidence_attacks': high_confidence_attacks,
                'overall_threat_level': overall_threat,
                'attack_types': [
                    {
                        'type': attack_type,
                        'probability': round(data['avg_confidence'], 1),
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
            # Get counts
            device_count = db.query(Device).count()
            alert_count = db.query(Alert).filter(Alert.acknowledged == False).count()
            
            # Get recent readings for power statistics
            recent_readings = db.query(PowerReading)\
                               .filter(PowerReading.timestamp >= datetime.now() - timedelta(hours=1))\
                               .all()
            
            total_power = sum(r.power_consumption for r in recent_readings) if recent_readings else 0
            avg_power = total_power / len(recent_readings) if recent_readings else 0
            
            # Anomaly detection rate
            anomaly_count = sum(1 for r in recent_readings if r.is_anomaly) if recent_readings else 0
            anomaly_rate = (anomaly_count / len(recent_readings) * 100) if recent_readings else 0
            
            # System uptime (simulated based on device activity)
            active_devices = db.query(Device)\
                              .join(PowerReading)\
                              .filter(PowerReading.timestamp >= datetime.now() - timedelta(minutes=10))\
                              .distinct()\
                              .count()
            
            uptime = (active_devices / device_count * 100) if device_count > 0 else 100
            
            return {
                'devices_monitored': device_count,
                'active_alerts': alert_count,
                'total_power_consumption': round(total_power, 2),
                'average_power': round(avg_power, 2),
                'system_uptime': round(uptime, 1),
                'anomaly_detection_rate': round(anomaly_rate, 1),
                'last_updated': datetime.now().isoformat()
            }
            
        finally:
            db.close()
    
    def get_device_health(self) -> List[Dict]:
        """Get health status for all devices"""
        db = self.get_session()
        try:
            devices = db.query(Device).all()
            health_data = []
            
            for device in devices:
                # Get latest reading
                latest_reading = db.query(PowerReading)\
                                  .filter(PowerReading.device_id == device.id)\
                                  .order_by(desc(PowerReading.timestamp))\
                                  .first()
                
                # Get recent alerts for this device
                recent_alerts = db.query(Alert)\
                                 .filter(and_(
                                     Alert.device_id == device.id,
                                     Alert.timestamp >= datetime.now() - timedelta(hours=24)
                                 ))\
                                 .count()
                
                health_score = 100
                if latest_reading:
                    if latest_reading.is_anomaly:
                        health_score -= 20
                    if (datetime.now() - latest_reading.timestamp).total_seconds() > 600:  # 10 minutes
                        health_score -= 30
                else:
                    health_score = 0  # No data
                
                health_score -= (recent_alerts * 10)  # Each alert reduces health
                health_score = max(0, health_score)  # Don't go below 0
                
                health_data.append({
                    'device_id': device.device_id_str,
                    'device_name': device.device_name,
                    'device_type': device.device_type,
                    'location': device.location,
                    'health_score': health_score,
                    'status': 'healthy' if health_score > 80 else 'warning' if health_score > 50 else 'critical',
                    'last_reading': latest_reading.timestamp.isoformat() if latest_reading else None,
                    'power_consumption': latest_reading.power_consumption if latest_reading else 0,
                    'recent_alerts': recent_alerts
                })
            
            return health_data
            
        finally:
            db.close()

# Global service instance
db_service = DatabaseService()
