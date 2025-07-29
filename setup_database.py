# setup_database.py
"""
Complete database setup script for HackSky
This script will:
1. Create database tables
2. Ingest sample data
3. Verify the setup
"""

import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_dir))

def setup_database():
    """Complete database setup process"""
    
    print("🚀 HackSky Database Setup Starting...")
    print("=" * 50)
    
    # Step 1: Check environment
    print("\n📋 Step 1: Environment Check")
    
    # Check if .env file exists
    env_file = Path('.env')
    if not env_file.exists():
        print("⚠️  .env file not found, copying from .env.example")
        import shutil
        shutil.copy('.env.example', '.env')
        print("✅ Created .env file - please update database credentials if needed")
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment variables loaded")
    except ImportError:
        print("⚠️  python-dotenv not installed, using default values")
    
    # Step 2: Test database connection
    print("\n🔌 Step 2: Database Connection Test")
    
    try:
        # Import from the backend directory (now in path)
        from database import engine, DATABASE_URL
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✅ Database connection successful")
            print(f"📊 Connected to: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'localhost'}")
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\n💡 Make sure MySQL is running:")
        print("   - With Docker: docker-compose up -d mysql")
        print("   - Local MySQL: Check service is running and credentials are correct")
        print("   - Install dependencies: pip install mysqlclient SQLAlchemy")
        return False
    
    # Step 3: Create database schema
    print("\n🏗️  Step 3: Create Database Schema")
    
    try:
        from database import create_database
        create_database()
        print("✅ Database tables created successfully")
        
    except Exception as e:
        print(f"❌ Failed to create database schema: {e}")
        return False
    
    # Step 4: Ingest sample data
    print("\n📊 Step 4: Data Ingestion")
    
    try:
        from ingest_data import ingest_sample_data
        ingest_sample_data()
        print("✅ Sample data ingested successfully")
        
    except Exception as e:
        print(f"❌ Failed to ingest sample data: {e}")
        return False
    
    # Step 5: Verification
    print("\n✅ Step 5: Setup Verification")
    
    try:
        from database_service import db_service
        
        # Test basic operations
        stats = db_service.get_statistics()
        power_data = db_service.get_recent_power_data(limit=5)
        alerts = db_service.get_alerts(limit=3)
        
        print(f"   📊 Statistics: {stats['devices_monitored']} devices monitored")
        print(f"   ⚡ Power Data: {len(power_data)} recent readings")
        print(f"   🚨 Alerts: {len(alerts)} system alerts")
        print("✅ All database operations working correctly")
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False
    
    # Success summary
    print("\n" + "=" * 50)
    print("🎉 HackSky Database Setup Complete!")
    print("\n📝 Next Steps:")
    print("   1. Start the backend server:")
    print("      cd backend && python server_v2.py")
    print("   2. Access the API at: http://localhost:5000")
    print("   3. View database in phpMyAdmin: http://localhost:8080")
    print("   4. Check API health: http://localhost:5000/api/health")
    print("\n🛠️  Development Commands:")
    print("   - Reset database: python setup_database.py --reset")
    print("   - Add sample data: python backend/ingest_data.py")
    print("   - Start MySQL: docker-compose up -d mysql")
    print("\n🔗 Frontend Integration:")
    print("   - Update API calls to use new endpoints")
    print("   - All existing endpoints are compatible")
    print("   - New features: /api/devices, /api/database/status")
    
    return True

def reset_database():
    """Reset the database (drop and recreate all tables)"""
    print("⚠️  Resetting database - this will delete all data!")
    confirm = input("Are you sure? Type 'yes' to continue: ")
    
    if confirm.lower() != 'yes':
        print("❌ Database reset cancelled")
        return
    
    try:
        from database import SessionLocal, engine
        from models import Base
        
        print("🗑️ Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        
        print("🏗️ Creating fresh tables...")
        Base.metadata.create_all(bind=engine)
        
        print("📊 Adding fresh sample data...")
        from ingest_data import ingest_sample_data
        ingest_sample_data()
        
        print("✅ Database reset complete!")
        
    except Exception as e:
        print(f"❌ Database reset failed: {e}")

def main():
    """Main setup function"""
    
    if len(sys.argv) > 1 and sys.argv[1] == '--reset':
        reset_database()
    else:
        setup_database()

if __name__ == "__main__":
    main()
