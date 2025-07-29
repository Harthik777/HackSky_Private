#!/usr/bin/env python3
"""
Test database connection for HackSky project
"""

import sys
import os
sys.path.append('backend')

try:
    from backend.database import engine
    print("✓ Successfully imported database module")
    
    # Test connection
    print("Testing database connection...")
    with engine.connect() as conn:
        from sqlalchemy import text
        result = conn.execute(text("SELECT 1 as test"))
        row = result.fetchone()
        if row[0] == 1:
            print("✓ Database connection successful!")
        else:
            print("✗ Database connection test failed")
    
    # Test database exists
    print("Testing if ics_monitoring database exists...")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DATABASE() as current_db"))
        current_db = result.fetchone()[0]
        print(f"✓ Connected to database: {current_db}")
        
        # Show tables
        result = conn.execute(text("SHOW TABLES"))
        tables = result.fetchall()
        print(f"Tables in database: {[table[0] for table in tables]}")
        
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

print("✓ All database tests passed!")
