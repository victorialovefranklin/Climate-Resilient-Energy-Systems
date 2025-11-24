# ⚡ Climate-Resilient Energy Systems Dashboard

**A Geospatial RAG-Enabled Digital Twin for Equity and Ecosystem Sustainability**

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 👤 Author

**Victoria Love Franklin**  
2nd Year PhD Pre-Candidate Data Science Student | GIS Scientist | CASPER Participant  
School of Applied Computational Science, Meharry Medical College

**Affiliations:**
- 🏛️ Tennessee Clinical Perfusionist Board (Governor Bill Lee Appointee)
- 🤝 HEJTC Board Member
- 📡 IEEE Student Member
- 🧪 APHL Wastewater Biosurveillance
- 💧 Water Environment Federation
- ⚙️ NSBE Professional Member

---

## 🚀 Quick Start

```bash
# 1. Install packages
pip install -r requirements.txt

# 2. Set your Claude API key (for RAG AI features)
# Windows:
set ANTHROPIC_API_KEY=your-api-key-here
# Mac/Linux:
export ANTHROPIC_API_KEY=your-api-key-here

# 3. Run dashboard
streamlit run dashboard_comprehensive.py

# Opens at http://localhost:8501
```

**Note:** The dashboard works without the API key - only RAG AI Insights requires it.

---

## 🔑 API KEYS

### 🤖 Claude API (Required for RAG AI Insights)

Set your Anthropic API key as an environment variable:

**Windows (Command Prompt):**
```bash
set ANTHROPIC_API_KEY=your-api-key-here
streamlit run dashboard_comprehensive.py
```

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY="your-api-key-here"
streamlit run dashboard_comprehensive.py
```

**Mac/Linux:**
```bash
export ANTHROPIC_API_KEY=your-api-key-here
streamlit run dashboard_comprehensive.py
```

**Using .env file:**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your key
ANTHROPIC_API_KEY=your-api-key-here
```

**Get your API key at:** https://console.anthropic.com

### ✅ FREE APIs (No Keys Required)
All data APIs are **completely free** and require **no registration**:

| API | URL | Description |
|-----|-----|-------------|
| **California OES Power Outages** | gis.data.ca.gov | Real-time power outage data |
| **Census TIGER/Line** | census.gov | County boundary shapefiles |
| **CalEnviroScreen 4.0** | oehha.ca.gov | Environmental justice screening |
| **EPA EJScreen** | epa.gov | Environmental justice data |
| **CDC Social Vulnerability Index** | cdc.gov/atsdr | Social vulnerability data |
| **NOAA Storm Events** | ncdc.noaa.gov | Climate and storm data |
| **CAL FIRE Incidents** | fire.ca.gov | Wildfire incidents |
| **EIA-861 Utility Data** | eia.gov | Utility customer data |

---

## 📊 Features

### 10 Interactive Pages:
1. 🏠 **Home & About** - Project overview and researcher profile
2. 📊 **Historic Dashboard** - EAGLE-I analysis (2014-2023)
3. 🔴 **Live Dashboard** - Real-time California outages
4. 🗺️ **Interactive Maps** - Folium geospatial visualizations
5. 📈 **EDA & Statistics** - Complete data analysis
6. ⚖️ **Environmental Justice** - Equity assessment
7. 🤖 **RAG AI Insights** - Claude-powered analysis
8. 🔬 **ML Models** - XGBoost, LightGBM predictions
9. 📋 **Federal Compliance** - DOE OE-417 assessment
10. ⚙️ **Settings & APIs** - Configuration and API info

### Key Capabilities:
- ⚡ Historic power outage analysis (10,000+ events)
- 🔴 Real-time California OES API integration
- 🤖 RAG-enabled AI insights with Claude
- 🗺️ Interactive maps with clustering and heatmaps
- 📊 Complete exploratory data analysis
- ⚖️ Environmental justice assessment
- 🔬 Machine learning predictions

---

## 📦 Installation

### Minimum Requirements:
```bash
pip install streamlit pandas numpy folium streamlit-folium plotly requests pillow anthropic
```

### Full Installation:
```bash
pip install -r requirements.txt
```

### Required Packages:
- streamlit >= 1.28.0
- pandas >= 2.0.0
- numpy >= 1.24.0
- folium >= 0.14.0
- streamlit-folium >= 0.15.0
- plotly >= 5.15.0
- requests >= 2.31.0
- pillow >= 10.0.0
- anthropic >= 0.7.0

### Optional (for ML features):
- scikit-learn >= 1.3.0
- xgboost >= 2.0.0
- lightgbm >= 4.0.0
- geopandas >= 0.13.0

---

## 🗺️ Maps Fixed!

The dashboard includes **working interactive maps**:
- **Live Outage Map** - CircleMarkers with clustering
- **Historic Heatmap** - Density visualization
- **County Analysis** - Bubble map by event count
- **Environmental Justice Overlay** - Coming soon

Maps use `folium_static()` for reliable rendering.

---

## 🎯 Usage

### 1. Load Data
On the home page, click:
- **"Load Historic Data"** - EAGLE-I 2014-2023
- **"Fetch Live Data"** - California OES API
- **"Load All Data"** - Both datasets

### 2. Explore Pages
Navigate through sidebar to explore all 10 pages.

### 3. Use RAG AI Insights
Go to 🤖 RAG AI Insights page and:
- Click sample questions, OR
- Type your own question
- Get Claude-powered analysis!

---

## 📝 Citation

```
Franklin, V.L. (2025). Toward Climate-Resilient Energy Systems: 
A Geospatial RAG-Enabled Digital Twin for Equity and Ecosystem Sustainability. 
School of Applied Computational Science, Meharry Medical College.
```

---

## 📁 Repository Structure

```
├── dashboard_comprehensive.py   # Main Streamlit application
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── LICENSE                      # MIT License
└── .gitignore                   # Git ignore file
```

---

## 🔬 Research Focus

- California energy resilience
- Climate change impacts
- Environmental justice
- Social vulnerability
- GIS & spatial analysis
- AI/ML predictions
- RAG systems
- Power grid modernization

---

## 📄 License

MIT License - See LICENSE file

---

## 🙏 Acknowledgments

- California Governor's Office of Emergency Services
- US Census Bureau
- California EPA (CalEnviroScreen)
- US EPA (EJScreen)
- CDC/ATSDR (Social Vulnerability Index)
- NOAA (Storm Events)
- CAL FIRE
- EIA (Energy Information Administration)

---

**Built with ❤️ for sustainable, resilient, and equitable communities**
