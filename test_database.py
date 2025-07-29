# test_database.py
"""
Simple test script to verify the MySQL database setup works correctly
"""

import sys
import os
from pathlib import Path

def setup_imports():
    """Setup proper imports for backend modules"""
    # Get the current script directory
    script_dir = Path(__file__).parent.resolve()
    backend_dir = script_dir / 'backend'
    
    # Add backend directory to Python path
    if str(backend_dir) not in sys.path:
        sys.path.insert(0, str(backend_dir))
    
    # Change to script directory to ensure relative imports work
    original_cwd = os.getcwd()
    os.chdir(script_dir)
    
    return original_cwd

def import_backend_modules():
    """Import all required backend modules with error handling"""
    try:
        # Import modules one by one with better error reporting
        modules = {}
        
        try:
            import database
            modules['database'] = database
        except ImportError as e:
            print(f"❌ Failed to import database module: {e}")
            raise
            
        try:
            import models
            modules['models'] = models
        except ImportError as e:
            print(f"❌ Failed to import models module: {e}")
            raise
            
        try:
            import ingest_data
            modules['ingest_data'] = ingest_data
        except ImportError as e:
            print(f"❌ Failed to import ingest_data module: {e}")
            raise
            
        return modules
        
    except ImportError as e:
        print("💡 Troubleshooting tips:")
        print("   1. Make sure you're running this script from the project root directory")
        print("   2. Install required dependencies: pip install -r backend/requirements.txt")
        print("   3. Check that all backend files exist:")
        backend_files = ['database.py', 'models.py', 'ingest_data.py']
        for file in backend_files:
            file_path = Path(__file__).parent / 'backend' / file
            status = "✅" if file_path.exists() else "❌"
            print(f"      {status} backend/{file}")
        return None

# Setup imports
original_cwd = setup_imports()

def test_database_connection():
    """Test basic database functionality"""
    
    print("🧪 Testing HackSky MySQL Database Setup")
    print("=" * 40)
    
    # Import backend modules
    modules = import_backend_modules()
    if not modules:
        return False
    
    database = modules['database']
    models = modules['models']
    ingest_data = modules['ingest_data']
    
    try:
        # Test 1: Module imports
        print("\n1️⃣ Testing module imports...")
        print("✅ All modules imported successfully")
        
        # Test 2: Database connection
        print("\n2️⃣ Testing database connection...")
        with database.engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✅ Database connection successful")
            print(f"   Connected to: {database.DATABASE_URL.split('@')[1] if '@' in database.DATABASE_URL else 'localhost'}")
        
        # Test 3: Create tables
        print("\n3️⃣ Creating database tables...")
        database.create_database()
        print("✅ Database tables created")
        
        # Test 4: Simple CRUD operations
        print("\n4️⃣ Testing database operations...")
        
        db = database.SessionLocal()
        try:
            # Create a test device
            test_device = models.Device(
                device_id_str="test_device_1",
                device_name="Test Device",
                device_type="test",
                location="Test Lab"
            )
            db.add(test_device)
            db.commit()
            
            # Query the device
            queried_device = db.query(models.Device).filter(models.Device.device_id_str == "test_device_1").first()
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
        
        # Run a minimal version of data ingestion
        ingest_data.ingest_sample_data()
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
