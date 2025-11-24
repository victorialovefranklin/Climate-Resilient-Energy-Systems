# ⚡ EAGLE-I Environmental Justice & Grid Resilience Analyzer

## A Geospatial Tool for Climate-Resilient Energy Systems

---

### 🏛️ Project Information

**PROJECT:** Toward Climate-Resilient Energy Systems: A Geospatial RAG-Enabled Digital Twin Approach for Equity and Ecosystem Sustainability

**FUNDING:** U.S. Department of Energy (DoE) - Savannah River National Laboratory (SRNL)

---

### 👥 Authors

| Author | Role | Email |
|--------|------|-------|
| **Victoria Love Franklin**¹²* | Ph.D. Pre-Candidate Data Science, GIS Scientist, DoE SRNL Researcher | victoria.franklin@mmc.edu |
| **Dr. Sajid Hussain**¹ | Department Chair and Professor | sajid.hussain@mmc.edu |
| **Dr. Lei Qian**¹ | Associate Professor, Discipline Coordinator, Principal Investigator | lei.qian@mmc.edu |

**Affiliations:**
- ¹ Meharry Medical College, School of Applied Computational Sciences, Nashville, TN
- ² U.S. Department of Energy - Savannah River National Laboratory (SRNL)
- \* Corresponding Author

---

### 📄 Abstract

Climate change poses unprecedented challenges to energy infrastructure, disproportionately affecting vulnerable communities through power disruptions that exacerbate existing inequities. This research presents an innovative Geospatial RAG-Enabled Digital Twin framework that integrates real-time grid monitoring with environmental justice indicators to advance equitable climate resilience.

The EAGLE-I Environmental Justice & Grid Resilience Analyzer synthesizes power outage data from the Department of Energy's EAGLE-I system with CalEnviroScreen 4.0, EPA EJScreen, and CDC Social Vulnerability Index to identify communities facing compound vulnerabilities. Through spatial autocorrelation analysis (Moran's I, LISA clustering) and machine learning models, we quantify disparities in outage frequency, duration, and restoration times across sociodemographic gradients.

**Keywords:** Environmental Justice, Power Grid Resilience, Digital Twin, Climate Adaptation, Social Vulnerability Index, Geospatial Analysis, EAGLE-I, CalEnviroScreen, Energy Equity, RAG, Machine Learning

---

### 🚀 Quick Start

#### Option 1: Run Locally

```bash
# 1. Install dependencies
pip install -r requirements_eagle_i.txt

# 2. Run the application
streamlit run eagle_i_ej_analyzer_complete.py
```

#### Option 2: Deploy to Streamlit Cloud

1. Upload `eagle_i_ej_analyzer_complete.py` and `requirements_eagle_i.txt` to GitHub
2. Connect your repo to [Streamlit Cloud](https://share.streamlit.io/)
3. Deploy!

---

### 📊 Features

#### 🏠 Home & About
- Project overview and abstract
- Study focus areas
- Research team information
- Funding acknowledgment

#### 📊 EAGLE-I Historic Data
- **15,000+ outage events** (2014-2023)
- **38 California counties**
- Temporal trends and visualizations
- Cause analysis and seasonal patterns
- Interactive heatmaps
- CSV download

#### ⚖️ Environmental Justice
- **CalEnviroScreen 4.0** indicators
- **CDC Social Vulnerability Index** metrics
- **EPA EJScreen** data
- Interactive vulnerability maps
- Correlation analysis
- Risk assessment

#### 🔗 EJ-Outage Correlation
- Merged EJ + outage analysis
- Disparity detection
- SVI vs outage rate correlation
- Poverty vs duration analysis
- Equity metrics

#### 📋 AI Analysis Report
- **Comprehensive AI-generated report**
- Executive summary
- Detailed statistics
- Recommendations
- **PDF export capability**
- **TXT export**

#### 📥 Data Sources
- Complete documentation of all FREE data sources
- No API keys required

---

### 📁 Data Sources (All FREE)

| Source | Provider | URL |
|--------|----------|-----|
| EAGLE-I Power Outage Data | U.S. Department of Energy | https://eagle-i.doe.gov/ |
| CalEnviroScreen 4.0 | California OEHHA | https://oehha.ca.gov/calenviroscreen |
| EPA EJScreen | U.S. Environmental Protection Agency | https://www.epa.gov/ejscreen |
| CDC Social Vulnerability Index | CDC/ATSDR | https://www.atsdr.cdc.gov/placeandhealth/svi/ |
| American Community Survey | U.S. Census Bureau | https://data.census.gov |

---

### 📈 Environmental Justice Indicators

#### CalEnviroScreen 4.0
- Pollution Burden Score
- PM2.5, Ozone, Diesel PM
- Drinking Water Quality
- Pesticides, Toxic Releases
- Traffic Density

#### CDC Social Vulnerability Index (SVI)
- Poverty Rate
- Unemployment
- No High School Diploma
- Uninsured Rate
- Age Demographics (65+, 17-)
- Disability Rate
- Single Parent Households
- Minority Population %
- Limited English Proficiency
- No Vehicle Access

#### Health Burden
- Asthma Rate
- Cardiovascular Disease
- Low Birth Weight

#### Climate Risk
- Fire Risk Score

---

### 🧮 Composite EJ Score Formula

```
Composite EJ Score = (CES Score × 0.35) + (SVI Score × 0.35) + 
                     (Health Burden × 0.20) + (Fire Risk × 0.10)
```

---

### 📋 Citation

```
Franklin, V.L., Hussain, S., & Qian, L. (2025). EAGLE-I Environmental Justice 
& Grid Resilience Analyzer: A Geospatial Tool for Climate-Resilient Energy 
Systems. Meharry Medical College, School of Applied Computational Sciences. 
Funded by U.S. Department of Energy, Savannah River National Laboratory (SRNL).
```

---

### 📄 License

This tool was developed as part of research funded by the U.S. Department of Energy through the Savannah River National Laboratory. All data sources used are publicly available.

---

### 🙏 Acknowledgments

This research was supported by the U.S. Department of Energy through the Savannah River National Laboratory (SRNL). The authors thank Meharry Medical College's School of Applied Computational Sciences for institutional support.

---

**© 2025 Meharry Medical College. All rights reserved.**
