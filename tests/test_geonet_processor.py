#!/usr/bin/env python3
"""
Test suite for Enhanced GeoNet data processor
"""
import pytest
import pandas as pd
from datetime import datetime, timezone
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from geonet_data import EnhancedGeoNetProcessor

class TestEnhancedGeoNetProcessor:
    """Test cases for EnhancedGeoNetProcessor"""

    def test_processor_initialization(self):
        """Test that the processor initializes correctly"""
        processor = EnhancedGeoNetProcessor()
        assert processor.bucket_name == 'geonet-open-data'
        assert processor.s3_client is not None
        assert processor.station_discovery is not None

    def test_station_discovery(self):
        """Test that station discovery works"""
        processor = EnhancedGeoNetProcessor()
        stations = processor.get_stations()
        active_stations = processor.get_active_stations()

        assert isinstance(stations, dict)
        assert isinstance(active_stations, dict)
        assert len(active_stations) <= len(stations)

        # Check that active stations have required fields
        for station_code, station_info in active_stations.items():
            assert 'latitude' in station_info
            assert 'longitude' in station_info
            assert 'region' in station_info

    def test_calculate_enhanced_dbdt_with_empty_data(self):
        """Test enhanced dB/dt calculation with empty data"""
        processor = EnhancedGeoNetProcessor()

        # Empty DataFrame
        empty_df = pd.DataFrame()
        dbdt_value, dbdt_stats = processor.calculate_enhanced_dbdt(empty_df)
        assert dbdt_value == 0.0
        assert isinstance(dbdt_stats, dict)

        # DataFrame with single row
        single_row = pd.DataFrame({
            'value': [100.0],
            'timestamp': [datetime.now(timezone.utc)]
        })
        dbdt_value, dbdt_stats = processor.calculate_enhanced_dbdt(single_row)
        assert dbdt_value == 0.0

    def test_regional_thresholds(self):
        """Test that regional thresholds are properly configured"""
        processor = EnhancedGeoNetProcessor()

        assert hasattr(processor, 'base_thresholds')
        assert isinstance(processor.base_thresholds, dict)

        # Check that key regions are defined
        expected_regions = ['Auckland', 'Canterbury', 'Otago', 'Southland', 'Stewart Island']
        for region in expected_regions:
            assert region in processor.base_thresholds
            assert 'multiplier' in processor.base_thresholds[region]
            assert 'min_threshold' in processor.base_thresholds[region]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
