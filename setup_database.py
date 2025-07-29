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
            return None
            
        try:
            import models
            modules['models'] = models
        except ImportError as e:
            print(f"❌ Failed to import models module: {e}")
            return None
            
        try:
            import ingest_data
            modules['ingest_data'] = ingest_data
        except ImportError as e:
            print(f"❌ Failed to import ingest_data module: {e}")
            return None
            
        return modules
        
    except Exception as e:
        print(f"❌ Unexpected error during import: {e}")
        return None

def test_database_connection(db_module):
    """Test database connectivity"""
    try:
        # Test connection
        engine = db_module.engine
        with engine.connect() as connection:
            # Simple connectivity test
            connection.execute(db_module.engine.dialect.name == 'mysql' and 'SELECT 1' or 'SELECT 1')
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("💡 Make sure MySQL is running and credentials are correct")
        print(f"💡 Connection string: {db_module.DATABASE_URL}")
        return False

def create_tables(modules):
    """Create all database tables"""
    try:
        print("🏗️ Creating database tables...")
        modules['database'].create_database()
        print("✅ Database tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        return False

def ingest_sample_data(modules):
    """Ingest sample data into the database"""
    try:
        print("📊 Ingesting sample data...")
        modules['ingest_data'].ingest_sample_data()
        print("✅ Sample data ingested successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to ingest sample data: {e}")
        return False

def verify_setup(modules):
    """Verify the database setup"""
    try:
        print("🔍 Verifying database setup...")
        db = modules['database'].SessionLocal()
        
        # Check if tables exist and have data
        device_count = db.query(modules['models'].Device).count()
        reading_count = db.query(modules['models'].PowerReading).count()
        alert_count = db.query(modules['models'].Alert).count()
        
        print(f"📱 Devices: {device_count}")
        print(f"📊 Power readings: {reading_count}")
        print(f"🚨 Alerts: {alert_count}")
        
        db.close()
        
        if device_count > 0 and reading_count > 0:
            print("✅ Database setup verification successful")
            return True
        else:
            print("❌ Database setup verification failed - missing data")
            return False
            
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

def reset_database(modules):
    """Reset the database (drop all tables and recreate)"""
    try:
        print("🗑️ Resetting database...")
        modules['models'].Base.metadata.drop_all(bind=modules['database'].engine)
        print("✅ Database reset complete")
        return True
    except Exception as e:
        print(f"❌ Failed to reset database: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 HackSky Database Setup Script")
    print("=" * 50)
    
    # Handle command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='Setup HackSky database')
    parser.add_argument('--reset', action='store_true', help='Reset database before setup')
    parser.add_argument('--verify', action='store_true', help='Only verify existing setup')
    args = parser.parse_args()
    
    # Setup imports
    original_cwd = setup_imports()
    
    try:
        # Import backend modules
        modules = import_backend_modules()
        if not modules:
            return False
        
        # Test database connection
        if not test_database_connection(modules['database']):
            return False
        
        # Handle verification only
        if args.verify:
            return verify_setup(modules)
        
        # Handle reset
        if args.reset:
            if not reset_database(modules):
                return False
        
        # Create tables
        if not create_tables(modules):
            return False
        
        # Ingest sample data
        if not ingest_sample_data(modules):
            return False
        
        # Verify setup
        if not verify_setup(modules):
            return False
        
        print("=" * 50)
        print("🎉 Database setup completed successfully!")
        print("🚀 You can now run the backend server:")
        print("   cd backend && python server.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Setup failed with unexpected error: {e}")
        return False
    
    finally:
        # Restore original working directory
        os.chdir(original_cwd)

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
