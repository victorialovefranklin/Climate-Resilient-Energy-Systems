# ⚡ EAGLE-I Environmental Justice & Grid Resilience Analyzer v3.0

## 🔬 REAL DATA Analysis Tool - California Power Outages 2014-2023

### 📊 Data Sources (REAL DATA)

| Dataset | Records | Source | Description |
|---------|---------|--------|-------------|
| **EAGLE-I Outages** | 159,605 | DoE EAGLE-I | Power outage events with duration, customers, location |
| **DOE-417 Events** | 399 | DoE OE | Major reported electric disturbances |
| **EIA-861 Utilities** | 2,454 | EIA | Utility service territory and customer data |
| **CalEnviroScreen** | 58 counties | CA OEHHA | Environmental justice indicators |
| **CDC SVI** | 58 counties | CDC/ATSDR | Social vulnerability metrics |

---

## 🏛️ Project Information

**Project Title:** Toward Climate-Resilient Energy Systems: A Geospatial RAG-Enabled Digital Twin Approach for Equity and Ecosystem Sustainability

**Funding:** U.S. Department of Energy (DoE) - Savannah River National Laboratory (SRNL)

---

## 👥 Authors

| Author | Role | Email |
|--------|------|-------|
| **Victoria Love Franklin¹²*** | Ph.D. Pre-Candidate, GIS Scientist, DoE SRNL Researcher | victoria.franklin@mmc.edu |
| **Dr. Sajid Hussain¹** | Department Chair and Professor | sajid.hussain@mmc.edu |
| **Dr. Lei Qian¹** | Associate Professor, Principal Investigator | lei.qian@mmc.edu |

**Affiliations:**
- ¹ Meharry Medical College, School of Applied Computational Sciences, Nashville, TN
- ² U.S. Department of Energy - Savannah River National Laboratory (SRNL)
- \* Corresponding Author

---

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements_v3.txt

# Run the application
streamlit run eagle_i_ej_analyzer_v3_complete.py
```

### Required Data Files

Place these files in the same directory as the Python script:
- `eaglei_transformed.csv` (159,605 records)
- `DOE_standardized_power_outages.csv` (399 records)
- `EIA861_CA_Combined_Data.csv` (2,454 records)

---

## 📱 Application Pages

| Page | Description |
|------|-------------|
| 🏠 **Home** | Project overview, data summary, research team |
| 📊 **EAGLE-I Outages** | Historic outage analysis with trends, maps, downloads |
| ⚖️ **Environmental Justice** | EJ indicators with interactive maps and legends |
| 🔗 **EJ-Outage Correlation** | Disparity analysis between vulnerability and outages |
| 📋 **AI Report** | Auto-generated comprehensive analysis report |
| 📥 **Data Sources** | Documentation of all FREE public data sources |

---

## 🔗 Key Features

### ✅ REAL DATA Integration
- 159,605 actual EAGLE-I outage events
- 399 DOE-417 major event reports
- 2,454 EIA-861 utility records

### 📊 Enhanced Visualizations
- Interactive Folium maps with **legends showing counts & percentages**
- Risk category distribution charts
- Correlation heatmaps

### 🧭 Spatial Statistics
- Moran's I global autocorrelation
- LISA cluster analysis (hotspots/coldspots)

### ⚖️ Environmental Justice Analysis
- CalEnviroScreen 4.0 integration
- CDC Social Vulnerability Index
- EPA EJScreen indicators
- Composite EJ Score calculation

### 🌬️ EPA Air Quality (API Ready)
- PM2.5 and Ozone monitoring
- AQI category mapping
- EPA AQS API integration

---

## 📈 EJ-Outage Correlation Formula

```
Outage Rate per 1,000 = (Outage Count / Population) × 1,000

Composite EJ Score = (CES × 0.35) + (SVI × 0.35) + (Health × 0.20) + (Fire × 0.10)
```

---

## 📚 Citation

```
Franklin, V.L., Hussain, S., & Qian, L. (2025). EAGLE-I Environmental Justice 
& Grid Resilience Analyzer: A Geospatial Tool for Climate-Resilient Energy 
Systems. Meharry Medical College, School of Applied Computational Sciences. 
Funded by U.S. Department of Energy - Savannah River National Laboratory.
```

---

## 🔗 API Endpoints

| API | Endpoint | Auth |
|-----|----------|------|
| EPA AQS | `aqs.epa.gov/data/api/annualData/byState` | Free Key |
| EPA Envirofacts | `data.epa.gov/efservice/{table}/JSON` | None |
| AirNow | `airnowapi.org/aq/observation/zipCode/current/` | Free Key |

---

## 📄 License

© 2025 Meharry Medical College. All data sources are publicly available.

---

## 🙏 Acknowledgments

This research was funded by the U.S. Department of Energy through Savannah River National Laboratory (SRNL). We thank the California Office of Environmental Health Hazard Assessment (OEHHA), U.S. EPA, CDC/ATSDR, and EIA for providing publicly available environmental justice and energy data.
