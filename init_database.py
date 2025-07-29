#!/usr/bin/env python3
"""
Initialize the database tables for HackSky project
"""

import sys
import os
sys.path.append('backend')

try:
    from backend.database import engine, Base
    from backend.models import Device, PowerReading, Alert
    
    print("Creating database tables...")
    print(f"Database URL: {engine.url}")
    
    # Drop all tables (careful in production!)
    print("Dropping existing tables...")
    Base.metadata.drop_all(bind=engine)
    
    # Create all tables
    print("Creating new tables...")
    Base.metadata.create_all(bind=engine)
    
    print("✓ Database tables created successfully!")
    
    # Verify tables were created with a new connection
    from sqlalchemy import text
    with engine.connect() as conn:
        result = conn.execute(text("SHOW TABLES"))
        tables = result.fetchall()
        print(f"Created tables: {[table[0] for table in tables]}")
        
        # Show table structure for devices table if it exists
        if tables:
            for table in tables:
                table_name = table[0]
                print(f"\nTable: {table_name}")
                result = conn.execute(text(f"DESCRIBE {table_name}"))
                columns = result.fetchall()
                for col in columns:
                    print(f"  {col[0]}: {col[1]}")
        
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
