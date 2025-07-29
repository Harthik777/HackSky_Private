# backend/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import datetime

class Device(Base):
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id_str = Column(String(255), unique=True, index=True, nullable=False)  # MySQL requires String length
    device_name = Column(String(200), nullable=True)  # Human-readable name
    device_type = Column(String(100), nullable=True)  # 'pump', 'sensor', 'controller', etc.
    location = Column(String(200), nullable=True)
    status = Column(String(50), default='online')  # 'online', 'offline', 'warning', 'error'
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    readings = relationship("PowerReading", back_populates="device", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="device", cascade="all, delete-orphan")

class PowerReading(Base):
    __tablename__ = "power_readings"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    power_consumption = Column(Float, nullable=False)
    voltage = Column(Float, nullable=True)
    current = Column(Float, nullable=True)
    frequency = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    is_anomaly = Column(Boolean, default=False)
    anomaly_score = Column(Float, nullable=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    device = relationship("Device", back_populates="readings")

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    alert_type = Column(String(50), nullable=False)  # 'critical', 'warning', 'info'
    severity = Column(String(20), default='medium')  # 'low', 'medium', 'high', 'critical'
    title = Column(String(200), nullable=False)
    message = Column(String(1024), nullable=False)  # MySQL limit for message length
    system = Column(String(100), nullable=True)  # Related system component
    acknowledged = Column(Boolean, default=False)
    acknowledged_by = Column(String(100), nullable=True)
    acknowledged_at = Column(DateTime, nullable=True)
    resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime, nullable=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    device = relationship("Device", back_populates="alerts")

class AttackDetection(Base):
    __tablename__ = "attack_detections"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    attack_type = Column(String(100), nullable=False)  # 'Flow Manipulation', 'Pressure Attack', etc.
    confidence = Column(Float, nullable=False)  # 0.0 to 100.0
    threat_level = Column(String(20), nullable=False)  # 'Low', 'Medium', 'High'
    source_ip = Column(String(45), nullable=True)  # IPv4 or IPv6
    target_system = Column(String(100), nullable=True)
    description = Column(String(1024), nullable=True)  # MySQL String limit
    indicators = Column(String(2048), nullable=True)  # JSON string of indicators (limited for MySQL)
    mitigated = Column(Boolean, default=False)
    mitigation_action = Column(String(1024), nullable=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    device = relationship("Device")

class SystemMetrics(Base):
    __tablename__ = "system_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    metric_name = Column(String(100), nullable=False)  # 'total_power', 'anomaly_count', etc.
    metric_value = Column(Float, nullable=False)
    unit = Column(String(20), nullable=True)  # 'kW', 'count', '%', etc.
    category = Column(String(50), nullable=True)  # 'power', 'security', 'performance'
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    device = relationship("Device")
