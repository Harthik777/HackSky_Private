# test_database.py
"""
Simple test script to verify the MySQL database setup works correctly
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_dir))

def test_database_connection():
    """Test basic database functionality"""
    
    print("🧪 Testing HackSky MySQL Database Setup")
    print("=" * 40)
    
    try:
        # Test 1: Import modules
        print("\n1️⃣ Testing module imports...")
        from database import engine, DATABASE_URL, create_database
        from models import Device, PowerReading, Alert
        print("✅ All modules imported successfully")
        
        # Test 2: Database connection
        print("\n2️⃣ Testing database connection...")
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✅ Database connection successful")
            print(f"   Connected to: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'localhost'}")
        
        # Test 3: Create tables
        print("\n3️⃣ Creating database tables...")
        create_database()
        print("✅ Database tables created")
        
        # Test 4: Simple CRUD operations
        print("\n4️⃣ Testing database operations...")
        from database import SessionLocal
        
        db = SessionLocal()
        try:
            # Create a test device
            test_device = Device(
                device_id_str="test_device_1",
                device_name="Test Device",
                device_type="test",
                location="Test Lab"
            )
            db.add(test_device)
            db.commit()
            
            # Query the device
            queried_device = db.query(Device).filter(Device.device_id_str == "test_device_1").first()
            if queried_device:
                print("✅ Database CRUD operations working")
                print(f"   Created device: {queried_device.device_name}")
            else:
                print("❌ Device creation failed")
                return False
            
            # Cleanup
            db.delete(queried_device)
            db.commit()
            print("✅ Test cleanup completed")
            
        finally:
            db.close()
        
        # Test 5: Sample data ingestion
        print("\n5️⃣ Testing sample data ingestion...")
        from ingest_data import ingest_sample_data
        
        # Run a minimal version of data ingestion
        ingest_sample_data()
        print("✅ Sample data ingestion completed")
        
        print("\n🎉 All tests passed! Database setup is working correctly.")
        print("\n📝 Next steps:")
        print("   1. Start the backend: cd backend && python server.py")
        print("   2. Test the API: curl http://localhost:5000/api/health")
        print("   3. View database: http://localhost:8080 (phpMyAdmin)")
        
        return True
        
    except ImportError as e:
        print(f"❌ Module import failed: {e}")
        print("💡 Install dependencies: pip install mysqlclient SQLAlchemy")
        return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("💡 Make sure MySQL is running: docker-compose up -d mysql")
        return False

if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1)
