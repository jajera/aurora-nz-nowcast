# Aurora Nowcast NZ 🌌

An open-source project to track and visualize aurora visibility in New Zealand using real-time geomagnetic data from GeoNet.

[![Aurora Data Update](https://github.com/jajera/aurora-nz-nowcast/actions/workflows/aurora-data-update.yml/badge.svg)](https://github.com/jajera/aurora-nz-nowcast/actions/workflows/aurora-data-update.yml)
[![GitHub Pages](https://github.com/jajera/aurora-nz-nowcast/actions/workflows/pages.yml/badge.svg)](https://github.com/jajera/aurora-nz-nowcast/actions/workflows/pages.yml)

## 🎯 Overview

This application provides real-time aurora visibility alerts for New Zealand regions by monitoring geomagnetic disturbances using GeoNet's magnetometer data. When the Earth's magnetic field changes rapidly (high dB/dt values), it indicates geomagnetic storms that can produce visible auroras.

**🔗 Live App**: [https://jajera.github.io/aurora-nz-nowcast/](https://jajera.github.io/aurora-nz-nowcast/)

## ✨ Features

- **Real-time Monitoring**: Fetches 1Hz magnetometer data from GeoNet every 15 minutes
- **Regional Predictions**: Customized thresholds for Canterbury, Otago, Southland, and Stewart Island
- **Beautiful UI**: Modern responsive design with dark/light mode toggle
- **Automatic Updates**: GitHub Actions workflow processes data automatically
- **No API Dependencies**: Static deployment on GitHub Pages

## 🏗️ Architecture

### Backend (Python)

- Fetches magnetometer data from GeoNet's public S3 bucket (`s3://geonet-open-data`)
- Calculates dB/dt (rate of magnetic field change) from high-resolution data
- Applies regional thresholds based on magnetic latitude
- Generates static `status.json` file every 15 minutes via GitHub Actions

### Frontend (React)

- Single-page application using React (via CDN)
- Fetches pre-processed `status.json` file
- Responsive design with Tailwind CSS
- Local storage for theme preferences
- Automatic refresh every 15 minutes

## 🌍 Regional Thresholds

Different regions require different magnetic activity levels for aurora visibility:

| Region | Threshold Multiplier | Possible Aurora | Strong Activity |
|--------|---------------------|-----------------|-----------------|
| Canterbury | 1.5× | ≥30 nT/min | ≥75 nT/min |
| Otago | 1.2× | ≥24 nT/min | ≥60 nT/min |
| Southland | 1.0× | ≥20 nT/min | ≥50 nT/min |
| Stewart Island | 0.8× | ≥16 nT/min | ≥40 nT/min |

## 🛠️ Development Setup

### Prerequisites

- Python 3.11+
- pip

### Local Development

1. **Clone the repository**:

   ```bash
   git clone https://github.com/jajera/aurora-nz-nowcast.git
   cd aurora-nz-nowcast
   ```

2. **Install Python dependencies**:

   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Test the data processor**:

   ```bash
   cd backend
   python test_geonet.py
   ```

4. **Run the data processor manually**:

   ```bash
   cd backend
   python geonet_data.py
   ```

5. **Serve the frontend locally**:

   ```bash
   cd docs
   python -m http.server 8000
   # Open http://localhost:8000 in your browser
   ```

### Testing Data Access

The test script verifies that the system can access GeoNet's data:

```bash
cd backend
python test_geonet.py
```

This will test:

- S3 connection to GeoNet bucket
- Data fetching from magnetometer stations
- Full processing pipeline

## 📊 Data Sources

### GeoNet Magnetometer Stations

- **EYR (Eyrewell)**: -43.42°, 172.35° (Canterbury)
- **MCH (Christchurch)**: -43.60°, 172.72° (Canterbury)

Data is accessed from GeoNet's public S3 bucket using the path structure:

```plaintext
s3://geonet-open-data/time-series/tilde/MAG/[STATION]/[YEAR]/[MONTH]/[DAY]/
```

### Data Processing

1. **Fetch**: Download recent 1Hz magnetometer data (CSV format)
2. **Calculate**: Compute dB/dt from magnetic field components (X, Y, Z or H, D, Z)
3. **Analyze**: Find maximum dB/dt in the last 15 minutes
4. **Classify**: Apply regional thresholds to determine activity level
5. **Generate**: Create status.json with all regional predictions

## 🤖 Automation

The system runs automatically via GitHub Actions:

- **Schedule**: Every 15 minutes (`*/15 * * * *`)
- **Process**: Fetches new data and updates status.json
- **Deploy**: Commits changes to trigger GitHub Pages update
- **Artifacts**: Saves logs for debugging

## 🎨 Frontend Features

- **🌓 Theme Toggle**: Automatic dark/light mode based on system preference
- **📱 Responsive**: Works on desktop, tablet, and mobile
- **♿ Accessible**: Proper ARIA labels and keyboard navigation
- **⚡ Fast**: Static files with minimal dependencies
- **💾 Offline-ready**: Caches theme preferences locally

## 📈 Status Levels

### 🔴 Strong Activity Detected

- High geomagnetic disturbance (dB/dt ≥ regional threshold)
- Auroras likely visible to the naked eye
- Good conditions for photography

### 🟡 Possible Aurora

- Moderate geomagnetic activity
- Auroras may be visible, especially with camera
- Worth checking outside in dark locations

### ⚪ No Activity

- Low geomagnetic activity
- Auroras unlikely to be visible
- Normal magnetic field conditions

## 🔧 Configuration

### Adding New Stations

To add more magnetometer stations, update `backend/geonet_data.py`:

```python
MAGNETOMETER_STATIONS = {
    'NEW': {
        'name': 'New Station Name',
        'latitude': -XX.XX,
        'longitude': XXX.XX,
        'region': 'Region Name'
    }
}
```

### Adjusting Thresholds

Modify thresholds in `backend/geonet_data.py`:

```python
THRESHOLDS = {
    'no_activity': 20,    # Base threshold in nT/min
    'possible': 50        # Strong activity threshold
}

REGION_MAPPING = {
    'Region Name': {
        'visibility_threshold_multiplier': 1.0,
        'display_name': 'Display Name'
    }
}
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **GeoNet**: For providing open access to geomagnetic data
- **New Zealand Government**: For supporting open data initiatives
- **Aurora Community**: For feedback and testing

## 🐛 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For questions or issues:

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/jajera/aurora-nz-nowcast/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/jajera/aurora-nz-nowcast/discussions)
- 📧 **Contact**: Create an issue for general questions

---

**Note**: This is an experimental system for educational and research purposes. Always check multiple sources before making travel decisions for aurora viewing.
