#!/usr/bin/env python3
"""
Debug models import and table creation
"""

import sys
sys.path.append('backend')

try:
    print("Importing database components...")
    from backend.database import engine, Base
    print("✓ Database imported")
    
    print("Importing models...")
    from backend.models import Device, PowerReading, Alert
    print("✓ Models imported")
    
    print("Checking Base metadata...")
    print(f"Tables in metadata: {list(Base.metadata.tables.keys())}")
    
    if not Base.metadata.tables:
        print("✗ No tables found in metadata!")
        print("Let's check what's in the models module...")
        import backend.models as models
        for attr in dir(models):
            if not attr.startswith('_'):
                obj = getattr(models, attr)
                print(f"  {attr}: {type(obj)}")
    else:
        print("✓ Tables found in metadata, proceeding with creation...")
        Base.metadata.create_all(bind=engine)
        
        # Check created tables
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("SHOW TABLES"))
            tables = result.fetchall()
            print(f"Created tables: {[table[0] for table in tables]}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
