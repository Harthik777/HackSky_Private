# backend/server_v2.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from datetime import datetime, timedelta
import random
import time
import math

# Import database components
from database_service import db_service
from database import create_database
from models import Base

app = Flask(__name__)
CORS(app)

# Initialize database on startup
try:
    create_database()
    print("✅ Database connection established")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    print("💡 Make sure MySQL is running and credentials are correct")

@app.route('/api/power-data', methods=['GET'])
def get_power_data():
    """Get real-time power monitoring data from the database"""
    try:
        # Get query parameters
        minutes = request.args.get('minutes', 60, type=int)
        limit = request.args.get('limit', 100, type=int)
        
        data = db_service.get_recent_power_data(minutes=minutes, limit=limit)
        
        return jsonify({
            'status': 'success',
            'data': data,
            'timestamp': datetime.now().isoformat(),
            'source': 'database'
        })
        
    except Exception as e:
        print(f"Error getting power data: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to retrieve power data',
            'data': []
        }), 500

@app.route('/api/system-status', methods=['GET'])
def get_system_status():
    """Get current system status from database"""
    try:
        status_data = db_service.get_system_status()
        
        return jsonify({
            'status': 'success',
            **status_data,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error getting system status: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to retrieve system status'
        }), 500

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get system alerts from database"""
    try:
        unacknowledged_only = request.args.get('unacknowledged', 'false').lower() == 'true'
        limit = request.args.get('limit', 50, type=int)
        
        alerts = db_service.get_alerts(limit=limit, unacknowledged_only=unacknowledged_only)
        
        return jsonify({
            'status': 'success',
            'alerts': alerts,
            'count': len(alerts),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error getting alerts: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to retrieve alerts',
            'alerts': []
        }), 500

@app.route('/api/alerts', methods=['POST'])
def add_alert():
    """Add a new alert to the database"""
    try:
        data = request.get_json()
        
        if not data or not all(key in data for key in ['type', 'title', 'message']):
            return jsonify({
                'status': 'error',
                'message': 'Missing required fields: type, title, message'
            }), 400
        
        success = db_service.add_alert(
            alert_type=data['type'],
            title=data['title'],
            message=data['message'],
            system=data.get('system'),
            severity=data.get('severity', 'medium'),
            device_id=data.get('device_id')
        )
        
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Alert added successfully'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to add alert'
            }), 500
            
    except Exception as e:
        print(f"Error adding alert: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to add alert'
        }), 500

@app.route('/api/alerts/<int:alert_id>/acknowledge', methods=['POST'])
def acknowledge_alert(alert_id):
    """Acknowledge a specific alert"""
    try:
        data = request.get_json() or {}
        acknowledged_by = data.get('acknowledged_by', 'user')
        
        success = db_service.acknowledge_alert(alert_id, acknowledged_by)
        
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Alert acknowledged'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Alert not found'
            }), 404
            
    except Exception as e:
        print(f"Error acknowledging alert: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to acknowledge alert'
        }), 500

@app.route('/api/attack-analysis', methods=['GET'])
def get_attack_analysis():
    """Get attack detection analysis from database"""
    try:
        analysis = db_service.get_attack_analysis()
        
        return jsonify({
            'status': 'success',
            **analysis,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error getting attack analysis: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to retrieve attack analysis'
        }), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get dashboard statistics from database"""
    try:
        stats = db_service.get_statistics()
        
        return jsonify({
            'status': 'success',
            **stats
        })
        
    except Exception as e:
        print(f"Error getting statistics: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to retrieve statistics'
        }), 500

@app.route('/api/devices', methods=['GET'])
def get_devices():
    """Get all devices and their health status"""
    try:
        devices = db_service.get_device_health()
        
        return jsonify({
            'status': 'success',
            'devices': devices,
            'count': len(devices),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error getting devices: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to retrieve devices',
            'devices': []
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint with database status"""
    try:
        # Test database connection
        test_stats = db_service.get_statistics()
        db_status = 'connected'
        db_message = 'Database is operational'
        
    except Exception as e:
        db_status = 'error'
        db_message = f'Database connection failed: {str(e)}'
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '3.0.0-database',
        'data_source': 'MySQL Database',
        'database': {
            'status': db_status,
            'message': db_message,
            'type': 'MySQL',
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'ics_monitoring')
        },
        'features': [
            'Real-time power monitoring',
            'Anomaly detection',
            'Attack pattern analysis',
            'Device health tracking',
            'Alert management',
            'Historical data storage'
        ]
    })

@app.route('/api/database/status', methods=['GET'])
def get_database_status():
    """Get detailed database status and statistics"""
    try:
        from database import SessionLocal
        from models import Device, PowerReading, Alert, AttackDetection
        
        db = SessionLocal()
        try:
            # Get table counts
            device_count = db.query(Device).count()
            reading_count = db.query(PowerReading).count()
            alert_count = db.query(Alert).count()
            attack_count = db.query(AttackDetection).count()
            
            # Get date range of data
            oldest_reading = db.query(PowerReading).order_by(PowerReading.timestamp).first()
            newest_reading = db.query(PowerReading).order_by(PowerReading.timestamp.desc()).first()
            
            return jsonify({
                'status': 'success',
                'database': {
                    'connected': True,
                    'type': 'MySQL',
                    'host': os.getenv('DB_HOST', 'localhost'),
                    'database': os.getenv('DB_NAME', 'ics_monitoring')
                },
                'table_counts': {
                    'devices': device_count,
                    'power_readings': reading_count,
                    'alerts': alert_count,
                    'attack_detections': attack_count
                },
                'data_range': {
                    'oldest_reading': oldest_reading.timestamp.isoformat() if oldest_reading else None,
                    'newest_reading': newest_reading.timestamp.isoformat() if newest_reading else None
                },
                'timestamp': datetime.now().isoformat()
            })
            
        finally:
            db.close()
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Database error: {str(e)}',
            'database': {
                'connected': False,
                'error': str(e)
            }
        }), 500

@app.route('/api/database/init', methods=['POST'])
def initialize_database():
    """Initialize database with sample data (for development/demo)"""
    try:
        from ingest_data import ingest_sample_data
        
        # Run the data ingestion
        ingest_sample_data()
        
        return jsonify({
            'status': 'success',
            'message': 'Database initialized with sample data',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to initialize database: {str(e)}'
        }), 500

# Legacy compatibility endpoints (for backward compatibility with existing frontend)
@app.route('/api/data-source', methods=['GET'])
def get_data_source_info():
    """Get information about current data source"""
    return jsonify({
        'dataset_type': 'MySQL Database',
        'database_available': True,
        'instructions': {
            'setup': 'MySQL database with SQLAlchemy ORM',
            'tables': ['devices', 'power_readings', 'alerts', 'attack_detections', 'system_metrics'],
            'features': 'Real-time data storage and retrieval'
        }
    })

if __name__ == '__main__':
    print("🚀 Starting HackSky ICS Cybersecurity Backend v3.0")
    print("🗄️  MySQL Database Integration Enabled")
    print("🔒 Manipal Institute of Technology - Team 0verr1de")
    print()
    
    # Database configuration info
    print("📊 Database Configuration:")
    print(f"   Host: {os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3307')}")
    print(f"   Database: {os.getenv('DB_NAME', 'ics_monitoring')}")
    print(f"   User: {os.getenv('DB_USER', 'root')}")
    print()
    
    print("🛠️  Available Endpoints:")
    print("   📊 Data: /api/power-data")
    print("   🔧 System: /api/system-status")
    print("   🚨 Alerts: /api/alerts")
    print("   🛡️  Security: /api/attack-analysis")
    print("   📈 Stats: /api/statistics")
    print("   🖥️  Devices: /api/devices")
    print("   ❤️  Health: /api/health")
    print("   🗄️  DB Status: /api/database/status")
    print("   🔧 DB Init: /api/database/init [POST]")
    print()
    
    print("💡 To initialize the database with sample data:")
    print("   curl -X POST http://localhost:5000/api/database/init")
    print()
    
    print("🌐 Server running on http://localhost:5000")
    print("📈 API Documentation: http://localhost:5000/api/health")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
