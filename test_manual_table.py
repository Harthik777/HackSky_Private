#!/usr/bin/env python3
"""
Manual database table creation test
"""

import sys
sys.path.append('backend')

try:
    from backend.database import engine
    from sqlalchemy import text
    
    print("Testing manual table creation...")
    
    with engine.connect() as conn:
        # Create a simple test table
        print("Creating test table...")
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS test_table (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255)
            )
        """))
        conn.commit()
        
        # Check if table was created
        result = conn.execute(text("SHOW TABLES"))
        tables = result.fetchall()
        print(f"Tables after manual creation: {[table[0] for table in tables]}")
        
        # Drop test table
        conn.execute(text("DROP TABLE IF EXISTS test_table"))
        conn.commit()
        print("Test table dropped")
        
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
