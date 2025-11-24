# Climate-Resilient Energy Systems: Geospatial RAG-Enabled Digital Twin

**Author:** Victoria Love Franklin  
**Institution:** School of Applied Computational Science, Meharry Medical College  
**Role:** 2nd Year PhD Pre-Candidate Data Science Student | GIS Scientist | CASPER Participant

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 📋 Project Overview

This comprehensive dashboard integrates Geographic Information Systems (GIS) with advanced artificial intelligence methods to address California's climate-induced energy challenges. The system combines historic power outage analysis (EAGLE-I 2014-2023), live API data integration, RAG-enabled AI insights, and complete environmental justice assessment.

### Key Features

- ⚡ **Historic Analysis**: EAGLE-I power outage data (2014-2023)
- 🔴 **Live Integration**: Real-time California OES API data
- 🤖 **RAG AI Insights**: Context-aware recommendations using Claude
- 🗺️ **Interactive Maps**: Folium geospatial visualizations with LISA clusters
- 📊 **Complete EDA**: Statistical analysis and correlations
- ⚖️ **Environmental Justice**: Equity-focused vulnerability assessment
- 🔬 **ML Models**: XGBoost, LightGBM with SHAP explainability
- 📋 **Federal Compliance**: DOE OE-417 reporting assessment

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/climate-resilient-energy-dashboard.git
cd climate-resilient-energy-dashboard
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the dashboard**
```bash
streamlit run dashboard_comprehensive.py
```

4. **Access in browser**
```
http://localhost:8501
```

---

## 📦 Requirements

### Core Packages
- streamlit - Dashboard framework
- pandas, numpy - Data processing
- geopandas, folium - Geospatial analysis
- plotly, matplotlib - Visualization

### Optional Packages
- anthropic - AI insights (requires API key)
- xgboost, lightgbm - Machine learning
- shap - Model explainability

See `requirements.txt` for complete list.

---

## 🎯 Usage

### Loading Data

On the home page, use the quick load buttons:
- **Load Historic Data**: EAGLE-I dataset (2014-2023)
- **Fetch Live Data**: Current California OES API outages
- **Load GeoData**: California county boundaries

### Exploring Pages

Navigate through 10 interactive pages:
1. 🏠 **Home & About** - Project overview and researcher profile
2. 📊 **Historic Dashboard** - EAGLE-I analysis (2014-2023)
3. 🔴 **Live Dashboard** - Real-time outage monitoring
4. 🗺️ **Interactive Maps** - Geospatial visualizations
5. 📈 **Complete EDA** - Statistical analysis
6. ⚖️ **Environmental Justice** - Equity assessment
7. 🤖 **RAG AI Insights** - AI-powered analysis
8. 🔬 **ML Models** - Predictions with explainability
9. 📋 **Federal Compliance** - DOE reporting analysis
10. ⚙️ **Settings** - Configuration and management

### Enabling AI Features

To use RAG-enabled insights:
1. Obtain Anthropic API key from https://console.anthropic.com
2. Enter API key in Settings page
3. Use RAG AI Insights page to ask questions

---

## 🗺️ Data Sources

### Power Outage Data
- **EAGLE-I** (2014-2023): Historic outage events
- **California OES API**: Real-time power outage incidents
- **EIA-861**: Utility customer demographics

### Social Vulnerability
- **CalEnviroScreen 4.0**: Pollution burden and population characteristics
- **EPA EJScreen**: Environmental justice screening
- **CDC SVI**: Social Vulnerability Index
- **ACS**: American Community Survey demographics

### Climate & Hazards
- **CAL FIRE**: Wildfire incidents
- **NOAA**: Climate data and storm events
- **Google Earth Engine**: Satellite imagery

### Infrastructure
- **Census TIGER/Line**: Geographic boundaries
- **HIFLD**: Transmission lines and substations

---

## 🔬 Methodology

### 1. Data Integration
Multi-source data aggregation with temporal alignment (2014-2023) and spatial harmonization at county level.

### 2. Geospatial Analysis
- LISA cluster detection
- Moran's I spatial autocorrelation
- Hot spot analysis (Getis-Ord Gi*)
- Environmental justice overlays

### 3. Machine Learning
- XGBoost, LightGBM, TensorFlow models
- Feature engineering from temporal, spatial, demographic variables
- SHAP explainability analysis

### 4. RAG-Enabled Insights
- Context retrieval from live data
- LLM query processing with Claude
- Evidence-based recommendations

---

## 📊 Dashboard Structure

```
dashboard_comprehensive.py
├── Data Loading Functions
│   ├── load_historic_eagle_i()
│   ├── fetch_live_california_outages()
│   └── load_california_counties()
├── RAG System
│   └── rag_query_claude()
├── Pages
│   ├── page_home()
│   ├── page_historic()
│   ├── page_live()
│   ├── page_maps()
│   ├── page_eda()
│   ├── page_justice()
│   ├── page_rag()
│   ├── page_ml()
│   ├── page_compliance()
│   └── page_settings()
└── Main Router
```

---

## ⚙️ Configuration

### Environment Variables (Optional)

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

### Streamlit Configuration

Create `.streamlit/config.toml`:

```toml
[server]
port = 8501
address = "localhost"

[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
```

---

## 🎓 Research Objectives

1. **Identify Vulnerable Areas**: Map social vulnerability overlays and detect spatial clusters
2. **Link Environmental Threats**: Correlate climate hazards with outage patterns
3. **Support Resilience Planning**: Provide actionable insights for infrastructure investments
4. **Advance Environmental Justice**: Ensure equitable grid modernization
5. **Create Transferable Framework**: Enable adaptation to other regions

---

## 👤 About the Researcher

**Victoria Love Franklin**  
2nd Year PhD Pre-Candidate Data Science Student  
GIS Scientist | CASPER Participant  
School of Applied Computational Science  
Meharry Medical College

### Professional Affiliations
- 🏛️ Tennessee Clinical Perfusionist Board (Governor Bill Lee Appointee)
- 🤝 Health, Education, and Justice Technology Consortium (HEJTC) - Board Member
- 📡 IEEE - Student Member
- 🧪 APHL - Wastewater Biosurveillance Program
- 💧 Water Environment Federation (WEF)
- ⚙️ National Society of Black Engineers (NSBE) - Professional Member

### Expertise
- Urban forestry ecosystem services & ecology
- DoD groundwater hydrology & auger modeling
- USDA forestry biomass residual analytics
- DoD biosurveillance systems
- Wastewater-based genomics epidemiology
- DoE smart grid & GIS digital twin technology
- Power grid resilience & critical infrastructure

---

## 📝 Citation

```
Franklin, V.L. (2025). Toward Climate-Resilient Energy Systems: A Geospatial 
RAG-Enabled Digital Twin for Equity and Ecosystem Sustainability. School of 
Applied Computational Science, Meharry Medical College.
```

### BibTeX

```bibtex
@techreport{franklin2025climate,
  title={Toward Climate-Resilient Energy Systems: A Geospatial RAG-Enabled Digital Twin for Equity and Ecosystem Sustainability},
  author={Franklin, Victoria Love},
  year={2025},
  institution={School of Applied Computational Science, Meharry Medical College},
  type={PhD Research Project}
}
```

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 🙏 Acknowledgments

- California Governor's Office of Emergency Services - Power outage data
- US Census Bureau - Demographic and geographic data
- California Environmental Protection Agency - CalEnviroScreen
- EPA - EJScreen environmental justice data
- CDC - Social Vulnerability Index
- CAL FIRE - Wildfire incident data
- NOAA - Climate hazard data

---

## 📧 Contact

For inquiries about this research, collaboration opportunities, or technical questions:

**Victoria Love Franklin**  
School of Applied Computational Science  
Meharry Medical College

---

## 🔍 Keywords

California energy resilience, climate change impacts, social vulnerability, environmental justice, GIS, artificial intelligence, generative AI, large language models, RAG, geospatial digital twin, power outage prediction, XGBoost, LightGBM, TensorFlow, SHAP explainability, ArcGIS Pro, Google Earth Engine, climate hazard modeling, spatial risk assessment, equity-focused infrastructure planning, smart grid modernization

---

**Built with ❤️ for sustainable, resilient, and equitable communities**

---

## 🗺️ Roadmap

- [x] Historic EAGLE-I analysis (2014-2023)
- [x] Live California OES API integration
- [x] RAG-enabled AI insights
- [x] Interactive geospatial maps
- [x] Environmental justice assessment
- [ ] Complete ML model integration
- [ ] Enhanced SHAP visualizations
- [ ] Real-time alerting system
- [ ] Mobile-responsive interface
- [ ] Multi-state expansion

---

**Version:** 1.0  
**Last Updated:** November 2025  
**Status:** Active Development
