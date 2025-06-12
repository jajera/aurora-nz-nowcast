#!/usr/bin/env python3
"""
Test script for GeoNet aurora nowcasting functionality.
Useful for development and debugging.
"""

import sys
import json
from pathlib import Path
from geonet_data import GeoNetDataProcessor, MAGNETOMETER_STATIONS

def test_s3_connection():
    """Test basic S3 connection to GeoNet bucket."""
    print("Testing S3 connection to GeoNet bucket...")

    processor = GeoNetDataProcessor()

    try:
        # Try to list some objects in the new geomag structure
        response = processor.s3_client.list_objects_v2(
            Bucket=processor.bucket_name,
            Prefix='time-series/tilde/v1/domain=geomag/',
            MaxKeys=5
        )

        if 'Contents' in response:
            print(f"✅ Successfully connected to {processor.bucket_name}")
            print(f"Found {len(response['Contents'])} objects in geomag directory")
            return True
        else:
            print("⚠️  Connected but no objects found")
            return False

    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        return False

def test_data_fetch():
    """Test fetching data from a specific station."""
    print("\nTesting data fetch for magnetometer stations...")

    processor = GeoNetDataProcessor()
    successful_fetches = 0

    for station_code in MAGNETOMETER_STATIONS.keys():
        print(f"\nTesting station {station_code}:")

        try:
            # Use longer time period since data is at 60s intervals
            data = processor.fetch_magnetometer_data(station_code, hours_back=24)

            if data is not None and not data.empty:
                print(f"  ✅ Fetched {len(data)} data points")
                print(f"  📊 Columns: {list(data.columns)}")

                # Calculate dB/dt
                dbdt = processor.calculate_dbdt(data)
                print(f"  📈 dB/dt: {dbdt:.2f} nT/min")
                successful_fetches += 1

            else:
                print(f"  ⚠️  No data available")

        except Exception as e:
            print(f"  ❌ Error: {e}")

    # Return True if at least one station had data
    return successful_fetches > 0

def test_full_processing():
    """Test the complete data processing pipeline."""
    print("\nTesting full processing pipeline...")

    processor = GeoNetDataProcessor()

    try:
        status_data = processor.generate_status_json()

        print("✅ Successfully generated status data")
        print(f"📊 Regions processed: {list(status_data['regions'].keys())}")

        # Print summary
        print("\n📈 Regional Status Summary:")
        for region, data in status_data['regions'].items():
            print(f"  {region}: {data['status']} (dB/dt: {data['dbdt_value']} nT/min)")

        # Save test output
        test_output = Path('test_status.json')
        with open(test_output, 'w') as f:
            json.dump(status_data, f, indent=2)
        print(f"\n💾 Test output saved to {test_output}")

        return True

    except Exception as e:
        print(f"❌ Processing failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 GeoNet Aurora Nowcasting Test Suite")
    print("=" * 50)

    tests = [
        ("S3 Connection", test_s3_connection),
        ("Data Fetch", test_data_fetch),
        ("Full Processing", test_full_processing)
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} test...")
        try:
            result = test_func()
            # Handle functions that don't return anything (assume success if no exception)
            if result is None:
                result = True
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Results Summary:")

    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1

        print(f"\n🎯 {passed}/{len(results)} tests passed")

    if passed == len(results):
        print("🎉 All tests passed! The system is ready.")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
