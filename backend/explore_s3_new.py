#!/usr/bin/env python3
import boto3
from botocore import UNSIGNED
from botocore.config import Config

def explore_new_structure():
    s3_client = boto3.client('s3', region_name='ap-southeast-2', config=Config(signature_version=UNSIGNED))

    print("Exploring NEW GeoNet S3 geomag structure...")

    # Get all geomag stations
    print('\n1. Available geomag stations:')
    try:
        response = s3_client.list_objects_v2(
            Bucket='geonet-open-data',
            Prefix='time-series/tilde/v1/domain=geomag/',
            Delimiter='/'
        )
        stations = []
        for obj in response.get('CommonPrefixes', []):
            station_path = obj["Prefix"]
            if 'station=' in station_path:
                station = station_path.split('station=')[1].rstrip('/')
                stations.append(station)
                print(f'  {station}')

        # Check what data types are available for a station
        if stations:
            sample_station = stations[0]
            print(f'\n2. Data types for station {sample_station}:')
            response = s3_client.list_objects_v2(
                Bucket='geonet-open-data',
                Prefix=f'time-series/tilde/v1/domain=geomag/station={sample_station}/',
                Delimiter='/'
            )
            for obj in response.get('CommonPrefixes', []):
                print(f'  {obj["Prefix"]}')

            # Check what's inside magnetic-field-component
            print(f'\n3. Magnetic field data for {sample_station}:')
            response = s3_client.list_objects_v2(
                Bucket='geonet-open-data',
                Prefix=f'time-series/tilde/v1/domain=geomag/station={sample_station}/name=magnetic-field-component/',
                MaxKeys=5
            )
            for obj in response.get('Contents', []):
                print(f'  {obj["Key"]}')

            # Try to download and examine one file
            if response.get('Contents'):
                sample_file = response['Contents'][0]['Key']
                print(f'\n4. Sample file content from {sample_file}:')
                try:
                    obj = s3_client.get_object(Bucket='geonet-open-data', Key=sample_file)
                    content = obj['Body'].read().decode('utf-8')
                    lines = content.split('\n')[:10]  # First 10 lines
                    for line in lines:
                        if line.strip():
                            print(f'  {line}')
                except Exception as e:
                    print(f'  Error reading file: {e}')

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    explore_new_structure()
