#!/usr/bin/env python3
"""
Test script to check WADI dataset integration status
"""

import os
import sys

def test_wadi_integration():
    print("🔍 WADI Dataset Integration Status Check")
    print("=" * 50)
    
    # Check if WADI integration module exists
    try:
        from wadi_integration import WADIDataConnector
        print("✅ WADI integration code is available")
        
        # Initialize connector
        connector = WADIDataConnector()
        print(f"📁 WADI dataset path: {connector.dataset_path}")
        
        # Check for WADI directory
        wadi_dir = connector.dataset_path
        if os.path.exists(wadi_dir):
            print(f"✅ WADI directory exists: {wadi_dir}")
            files = os.listdir(wadi_dir)
            print(f"📂 Files found: {files}")
        else:
            print(f"❌ WADI directory NOT found: {wadi_dir}")
            print("   Need to create: mkdir -p data/wadi/")
        
        # Check for specific WADI files
        wadi_files = ['WADI_14days.csv', 'WADI_attackdata.csv']
        files_found = []
        files_missing = []
        
        for file in wadi_files:
            file_path = os.path.join(wadi_dir, file)
            if os.path.exists(file_path):
                files_found.append(file)
                size = os.path.getsize(file_path) / (1024*1024)  # MB
                print(f"✅ {file} found ({size:.1f} MB)")
            else:
                files_missing.append(file)
                print(f"❌ {file} NOT found")
        
        # Test data loading
        print("\n🔍 Testing WADI data loading...")
        
        normal_data = connector.load_wadi_data('normal')
        if normal_data is not None:
            print(f"✅ WADI normal data loaded: {len(normal_data)} records")
        else:
            print("❌ WADI normal data could not be loaded")
        
        attack_data = connector.load_wadi_data('attack')
        if attack_data is not None:
            print(f"✅ WADI attack data loaded: {len(attack_data)} records")
        else:
            print("❌ WADI attack data could not be loaded")
        
        # Test power equivalent data
        print("\n🔍 Testing power equivalent data generation...")
        power_data = connector.get_power_equivalent_data()
        print(f"📊 Power data points returned: {len(power_data)}")
        
        if power_data:
            print(f"📊 Sample data point: {power_data[0]}")
            
            # Check if it's using real WADI data or simulated
            if normal_data is not None or attack_data is not None:
                print("✅ Using REAL WADI dataset")
            else:
                print("⚠️  Using SIMULATED data (WADI files not found)")
        
        # Summary
        print("\n📋 SUMMARY:")
        if files_found:
            print(f"✅ WADI files found: {files_found}")
            print("✅ Your system is using REAL WADI data")
        else:
            print("❌ No WADI files found")
            print("❌ Your system is using SIMULATED data")
            print("\n📥 To use real WADI data:")
            print("1. Download from: https://itrust.sutd.edu.sg/itrust-labs_datasets/")
            print("2. Create directory: mkdir -p data/wadi/")
            print("3. Place files: WADI_14days.csv, WADI_attackdata.csv")
        
    except ImportError as e:
        print(f"❌ WADI integration not available: {e}")
        print("❌ Your system is using basic simulated data only")
    except Exception as e:
        print(f"❌ Error testing WADI integration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_wadi_integration() 