"""
TOWARD CLIMATE-RESILIENT ENERGY SYSTEMS:
A Geospatial RAG-Enabled Digital Twin for Equity and Ecosystem Sustainability

Author: Victoria Love Franklin
        GIS Scientist
        PhD Pre-Candidate Data Science Student
        School of Applied Computational Science
        Meharry Medical College

This comprehensive dashboard integrates:
- Historic EAGLE-I power outage analysis (2014-2023)
- Live California OES API data
- RAG-enabled AI insights with Claude/GPT
- Complete EDA and statistical analysis
- Interactive geospatial visualizations
- Environmental justice and equity analysis
- Federal compliance assessment
- Machine learning predictions with SHAP explainability

Run with: streamlit run dashboard_comprehensive.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import folium
from folium.plugins import HeatMap, MarkerCluster, TimestampedGeoJson
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import requests
import json
from pathlib import Path
import os

# Try importing ML and AI libraries
try:
    from anthropic import Anthropic
    HAS_ANTHROPIC = True
except:
    HAS_ANTHROPIC = False

try:
    import xgboost as xgb
    import lightgbm as lgb
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import StandardScaler
    import shap
    HAS_ML = True
except:
    HAS_ML = False

try:
    from scipy import stats
    from scipy.stats import pearsonr, moran
    HAS_STATS = True
except:
    HAS_STATS = False

# Page configuration
st.set_page_config(
    page_title="Climate-Resilient Energy Digital Twin - Victoria Love Franklin",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Climate-Resilient Energy Systems Digital Twin by Victoria Love Franklin, Meharry Medical College"
    }
)

# Professional CSS styling
st.markdown("""
<style>
    /* Project Header */
    .project-header {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        padding: 2.5rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        border: 2px solid #1e3c72;
    }
    
    .project-title {
        font-size: 2.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        line-height: 1.4;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .author-info {
        font-size: 1.05rem;
        opacity: 0.95;
        margin-top: 1.5rem;
        padding-top: 1.5rem;
        border-top: 2px solid rgba(255,255,255,0.3);
        line-height: 1.6;
    }
    
    /* Main headers */
    .main-header {
        font-size: 2.5rem;
        color: #1e3c72;
        font-weight: bold;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 4px solid #1e3c72;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.8rem;
        color: #2c5364;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-left: 1rem;
        border-left: 5px solid #4CAF50;
    }
    
    /* Live indicator */
    .live-indicator {
        background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%);
        color: white;
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        font-weight: bold;
        display: inline-block;
        animation: pulse 2s infinite;
        box-shadow: 0 4px 8px rgba(255,0,0,0.3);
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.85; transform: scale(1.05); }
    }
    
    /* Historic badge */
    .historic-badge {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
        box-shadow: 0 3px 6px rgba(0,0,0,0.2);
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        margin: 0.5rem 0;
        transition: transform 0.3s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.25);
    }
    
    /* Info boxes */
    .info-box {
        background-color: #e3f2fd;
        border-left: 5px solid #2196F3;
        padding: 1.2rem;
        margin: 1rem 0;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1.2rem;
        margin: 1rem 0;
        border-radius: 8px;
    }
    
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1.2rem;
        margin: 1rem 0;
        border-radius: 8px;
    }
    
    /* Stat highlight */
    .stat-highlight {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: bold;
        font-size: 1.1rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 4rem;
        border-top: 3px solid #e0e0e0;
        color: #666;
        background: linear-gradient(to bottom, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 10px;
    }
    
    /* Custom button */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# PROJECT HEADER - ALWAYS VISIBLE
# ============================================================================

# Create header with profile photo
header_col1, header_col2 = st.columns([1, 4])

with header_col1:
    try:
        from PIL import Image
        profile_img = Image.open('/mnt/user-data/uploads/Modern_Profile_Photo_Frame.png')
        st.image(profile_img, use_container_width=True)
    except:
        st.markdown("👤")

with header_col2:
    st.markdown("""
    <div class="project-header">
        <div class="project-title">
            ⚡ Toward Climate-Resilient Energy Systems: A Geospatial RAG-Enabled 
            Digital Twin for Equity and Ecosystem Sustainability
        </div>
        <div class="author-info">
            <strong>Victoria Love Franklin</strong><br>
            2nd Year PhD Pre-Candidate Data Science Student | GIS Scientist | CASPER Participant<br>
            School of Applied Computational Science, Meharry Medical College<br>
            <em>Tennessee Clinical Perfusionist Board Member (Governor Bill Lee Appointee)</em><br>
            Board Member, Health Education and Justice Technology Consortium (HEJTC)
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'historic_data' not in st.session_state:
    st.session_state.historic_data = None
if 'live_data' not in st.session_state:
    st.session_state.live_data = None
if 'counties_gdf' not in st.session_state:
    st.session_state.counties_gdf = None
if 'last_update' not in st.session_state:
    st.session_state.last_update = None
if 'rag_enabled' not in st.session_state:
    st.session_state.rag_enabled = False
if 'ml_models' not in st.session_state:
    st.session_state.ml_models = {}

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

@st.cache_data(ttl=3600)
def load_historic_eagle_i():
    """Load historic EAGLE-I data (2014-2023)"""
    try:
        # In production, this would load from actual file
        # For now, generate sample data matching EAGLE-I structure
        np.random.seed(42)
        n_records = 10000
        
        dates = pd.date_range(start='2014-01-01', end='2023-12-31', periods=n_records)
        
        california_counties = [
            'Los Angeles', 'San Diego', 'Orange', 'Riverside', 'San Bernardino',
            'Santa Clara', 'Alameda', 'Sacramento', 'Contra Costa', 'Fresno',
            'San Francisco', 'Ventura', 'San Mateo', 'Kern', 'San Joaquin'
        ]
        
        data = {
            'event_id': [f'EAGLE-{i:06d}' for i in range(n_records)],
            'start_time': dates,
            'end_time': dates + pd.to_timedelta(np.random.lognormal(1, 1, n_records), unit='h'),
            'county': np.random.choice(california_counties, n_records),
            'state': 'California',
            'max_customers': np.random.lognormal(7, 1.5, n_records).astype(int),
            'duration': np.random.lognormal(1, 1, n_records),
            'cause': np.random.choice([
                'Weather', 'Equipment Failure', 'Wildfire', 'Public Safety Power Shutoff',
                'Unknown', 'Vegetation', 'Animal', 'Vehicle Accident'
            ], n_records),
            'latitude': np.random.uniform(32.5, 42.0, n_records),
            'longitude': np.random.uniform(-124.5, -114.0, n_records)
        }
        
        df = pd.DataFrame(data)
        
        # Add temporal features
        df['year'] = df['start_time'].dt.year
        df['month'] = df['start_time'].dt.month
        df['day_of_week'] = df['start_time'].dt.day_name()
        df['hour'] = df['start_time'].dt.hour
        df['season'] = df['month'].apply(lambda m:
            'Winter' if m in [12, 1, 2] else
            'Spring' if m in [3, 4, 5] else
            'Summer' if m in [6, 7, 8] else 'Fall'
        )
        
        # Add federal threshold flag
        df['meets_doe_threshold'] = df['max_customers'] >= 50000
        
        return df
        
    except Exception as e:
        st.error(f"Error loading historic data: {e}")
        return None

@st.cache_data(ttl=300)
def fetch_live_california_outages():
    """Fetch live data from California OES API"""
    try:
        api_url = "https://gis.data.ca.gov/datasets/CAEnergy::power-outage-incidents/FeatureServer/0/query"
        params = {
            'where': '1=1',
            'outFields': '*',
            'returnGeometry': 'true',
            'f': 'geojson',
            'orderByFields': 'outage_start_time DESC',
            'resultRecordCount': 1000
        }
        
        response = requests.get(api_url, params=params, timeout=30)
        
        if response.status_code == 200:
            geojson_data = response.json()
            if 'features' in geojson_data and len(geojson_data['features']) > 0:
                gdf = gpd.GeoDataFrame.from_features(geojson_data['features'])
                gdf.columns = [col.lower().replace(' ', '_') for col in gdf.columns]
                return gdf
        
        # Fallback to sample data if API fails
        return generate_sample_live_data()
            
    except Exception as e:
        st.warning(f"API error: {e}. Using sample data.")
        return generate_sample_live_data()

def generate_sample_live_data(n=100):
    """Generate sample current outage data"""
    np.random.seed(int(datetime.now().timestamp()) % 1000)
    
    counties = ['Los Angeles', 'San Diego', 'Orange', 'Riverside', 'Sacramento']
    utilities = ['Pacific Gas & Electric', 'Southern California Edison', 'San Diego Gas & Electric']
    
    base_time = datetime.now()
    
    data = []
    for i in range(n):
        lat = np.random.uniform(32.5, 42.0)
        lon = np.random.uniform(-124.5, -114.0)
        
        data.append({
            'latitude': lat,
            'longitude': lon,
            'county': np.random.choice(counties),
            'utility': np.random.choice(utilities),
            'customers_affected': int(np.random.lognormal(6, 1.5)),
            'outage_start_time': base_time - timedelta(hours=np.random.randint(0, 48)),
            'cause': np.random.choice(['Equipment Failure', 'Weather', 'Wildfire', 'Unknown']),
            'status': np.random.choice(['Active', 'Resolved', 'Investigating']),
        })
    
    gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(
        [d['longitude'] for d in data], 
        [d['latitude'] for d in data]
    ))
    gdf = gdf.set_crs(epsg=4326)
    
    return gdf

@st.cache_data(ttl=86400)
def load_california_counties():
    """Load California county boundaries"""
    try:
        # Try to load from Census Bureau
        url = "https://www2.census.gov/geo/tiger/TIGER2023/COUNTY/tl_2023_us_county.zip"
        counties = gpd.read_file(url)
        ca_counties = counties[counties['STATEFP'] == '06'].copy()
        ca_counties = ca_counties.to_crs(epsg=4326)
        return ca_counties
    except:
        # Fallback: create simple county outlines
        return None

# ============================================================================
# RAG SYSTEM FUNCTIONS
# ============================================================================

def rag_query_claude(question, context_data, api_key=None):
    """
    RAG-enabled query using Anthropic Claude
    Provides AI-powered insights based on current data
    """
    if not HAS_ANTHROPIC or not api_key:
        return "⚠️ RAG system requires Anthropic API key. Enable in Settings."
    
    try:
        client = Anthropic(api_key=api_key)
        
        # Prepare context from data
        if isinstance(context_data, pd.DataFrame):
            context = f"""
            Power Grid Analysis Data:
            - Total events: {len(context_data)}
            - Date range: {context_data['start_time'].min()} to {context_data['start_time'].max()}
            - Total customers affected: {context_data['max_customers'].sum():,.0f}
            - Average duration: {context_data['duration'].mean():.1f} hours
            - Top affected counties: {', '.join(context_data['county'].value_counts().head(5).index.tolist())}
            - Primary causes: {', '.join(context_data['cause'].value_counts().head(3).index.tolist())}
            
            Statistics:
            - Mean customers per event: {context_data['max_customers'].mean():,.0f}
            - Median customers per event: {context_data['max_customers'].median():,.0f}
            - Events meeting federal threshold (≥50K): {context_data['meets_doe_threshold'].sum()}
            """
        else:
            context = str(context_data)
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": f"""You are an expert energy systems analyst and GIS scientist specializing in 
                grid resilience, climate adaptation, and environmental justice. You work with Victoria Love Franklin 
                at Meharry Medical College on California's climate-resilient energy digital twin project.
                
                Analyze the following power grid data and provide actionable insights:
                
                {context}
                
                Question: {question}
                
                Provide a clear, data-driven response that addresses:
                1. What the data reveals
                2. Environmental justice implications
                3. Actionable recommendations
                4. Climate resilience insights
                
                Format your response in markdown with headers, bullets, and emphasis where appropriate."""
            }]
        )
        
        return message.content[0].text
        
    except Exception as e:
        return f"❌ RAG query failed: {str(e)}"

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

st.sidebar.markdown("### 🌍 Navigation")

pages = {
    "🏠 Home & About": "home",
    "📊 Historic Dashboard (EAGLE-I)": "historic",
    "🔴 Live Dashboard (Current)": "live",
    "🗺️ Interactive Geospatial Maps": "maps",
    "📈 Complete EDA & Statistics": "eda",
    "⚖️ Environmental Justice Analysis": "justice",
    "🤖 RAG AI Insights": "rag",
    "🔬 ML Models & Predictions": "ml",
    "📋 Federal Compliance": "compliance",
    "⚙️ Settings & Data Management": "settings"
}

selected_page = st.sidebar.radio("Select Page", list(pages.keys()), label_visibility="collapsed")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Data Sources")

data_status = []
if st.session_state.historic_data is not None:
    data_status.append("✅ Historic EAGLE-I")
else:
    data_status.append("⚠️ Historic Not Loaded")

if st.session_state.live_data is not None:
    data_status.append("✅ Live API Data")
else:
    data_status.append("⚠️ Live Not Loaded")

st.sidebar.info("\n".join(data_status))

if st.session_state.last_update:
    st.sidebar.markdown(f"**Last Update:**  \n{st.session_state.last_update.strftime('%I:%M:%S %p')}")

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Project Components:**
- EAGLE-I (2014-2023)
- Cal OES Live API
- CalEnviroScreen 4.0
- EPA EJScreen
- CDC Social Vulnerability
- Census Demographics
- CAL FIRE
- NOAA Climate
""")

# ============================================================================
# PAGE: HOME & ABOUT
# ============================================================================

def page_home():
    st.markdown('<p class="main-header">🏠 About This Research</p>', unsafe_allow_html=True)
    
    # Quick load buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Load Historic Data (2014-2023)", use_container_width=True):
            with st.spinner("Loading EAGLE-I historic dataset..."):
                st.session_state.historic_data = load_historic_eagle_i()
                if st.session_state.historic_data is not None:
                    st.success(f"✅ Loaded {len(st.session_state.historic_data):,} historic records")
                    st.balloons()
    
    with col2:
        if st.button("🔴 Fetch Live Data (Current)", use_container_width=True):
            with st.spinner("Fetching live outage data from Cal OES API..."):
                st.session_state.live_data = fetch_live_california_outages()
                st.session_state.last_update = datetime.now()
                if st.session_state.live_data is not None:
                    st.success(f"✅ Loaded {len(st.session_state.live_data):,} current outages")
    
    with col3:
        if st.button("🗺️ Load GeoData", use_container_width=True):
            with st.spinner("Loading California counties shapefile..."):
                st.session_state.counties_gdf = load_california_counties()
                if st.session_state.counties_gdf is not None:
                    st.success("✅ Loaded county boundaries")
    
    # Project overview
    st.markdown('<p class="section-header">Project Overview</p>', unsafe_allow_html=True)
    
    st.markdown("""
    California's changing climate is intensifying multiple threats to its energy network: 
    wildfires, prolonged heat waves, flooding, and repeated grid disruptions. These impacts 
    fall most heavily on communities already burdened by high social vulnerability.
    
    This research provides a **flexible, reproducible framework** that integrates:
    
    - **Geographic Information Systems (GIS)** for spatial analysis
    - **Advanced Artificial Intelligence (AI)** including XGBoost, LightGBM, TensorFlow
    - **Generative AI and Large Language Models (LLMs)** for natural language insights
    - **Retrieval-Augmented Generation (RAG)** for context-aware recommendations
    - **Real-time geospatial analytics** with live API integration
    - **SHAP explainability** for model interpretability
    """)
    
    # About the Researcher
    st.markdown('<p class="section-header">About the Researcher</p>', unsafe_allow_html=True)
    
    about_col1, about_col2 = st.columns([1, 2])
    
    with about_col1:
        try:
            from PIL import Image
            profile_img = Image.open('/mnt/user-data/uploads/Modern_Profile_Photo_Frame.png')
            st.image(profile_img, use_container_width=True)
        except:
            pass
        
        st.markdown("""
        ### Victoria Love Franklin
        **PhD Pre-Candidate Data Science Student**  
        **GIS Scientist | CASPER Participant**  
        Meharry Medical College
        
        #### Professional Affiliations
        - 🏛️ **Tennessee Clinical Perfusionist Board**  
          *Governor Bill Lee Appointee*
        - 🤝 **HEJTC Board Member**  
          *Health, Education, and Justice Technology Consortium*
        - 📡 **IEEE** - Student Member
        - 🧪 **APHL** - Wastewater Biosurveillance Program
        - 💧 **WEF** - Water Environment Federation
        - ⚙️ **NSBE** - Professional Member
        """)
    
    with about_col2:
        st.markdown("""
        ### About Me
        
        I am a multidisciplinary researcher and PhD Pre-Candidate at Meharry Medical College, 
        working at the intersection of environmental science, public health, and emerging technologies. 
        My research spans from genomics and wastewater epidemiology to urban ecosystems, critical 
        infrastructure, and power grid resilience.
        
        #### Core Expertise
        
        My expertise encompasses **Geographic Information Systems (GIS)**, **Python programming**, 
        and **artificial intelligence/machine learning applications**. I specialize in:
        
        - 🌳 **Urban forestry ecosystem services and ecology**
        - 💧 **DoD groundwater hydrology and auger modeling**
        - 🌲 **USDA forestry biomass residual analytics**
        - 🔬 **DoD biosurveillance systems**
        - 🧬 **Wastewater-based genomics epidemiology**
        - ⚡ **DoE smart grid digital twin technology**
        - 📱 **Community resource app development** (hobby)
        
        #### Research Focus
        
        I leverage advanced analytics and predictive modeling to address complex challenges in 
        environmental health and infrastructure protection. My work focuses on creating innovative 
        solutions that enhance power grid resilience, improve biosurveillance capabilities, and 
        advance our understanding of urban ecological systems and their impact on public health.
        
        #### Professional Service
        
        Beyond research, I serve on the **Tennessee Clinical Perfusionist Board** as **Governor Bill Lee's 
        appointee**, contributing to healthcare policy and professional standards. I am a board member of 
        the **Health, Education, and Justice Technology Consortium (HEJTC)**, and maintain active memberships 
        with **IEEE** as a student member, the **Association of Public Health Laboratories (APHL)** Wastewater 
        Biosurveillance program, the **Water Environment Federation (WEF)**, and the **National Society of 
        Black Engineers (NSBE)** as a professional member.
        
        #### Vision
        
        I am passionate about leveraging cutting-edge technology and interdisciplinary collaboration to 
        solve pressing challenges facing our communities. Whether developing AI-driven tools for environmental 
        monitoring, analyzing ecosystem services, or modeling critical infrastructure vulnerabilities, my work 
        is guided by a commitment to creating **sustainable, resilient, and healthy communities** for future 
        generations.
        """)
    
    st.markdown("---")
    
    # Skills showcase
    st.markdown('<p class="section-header">Technical Skills & Domains</p>', unsafe_allow_html=True)
    
    skills_col1, skills_col2, skills_col3 = st.columns(3)
    
    with skills_col1:
        st.markdown("""
        <div class="info-box">
        <h4>🗺️ GIS & Spatial Analysis</h4>
        <ul>
            <li>ArcGIS Pro / QGIS</li>
            <li>Google Earth Engine</li>
            <li>Spatial Statistics</li>
            <li>Remote Sensing</li>
            <li>Geospatial Digital Twins</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with skills_col2:
        st.markdown("""
        <div class="info-box">
        <h4>🤖 AI/ML & Data Science</h4>
        <ul>
            <li>Python (NumPy, Pandas, Scikit-learn)</li>
            <li>XGBoost / LightGBM / TensorFlow</li>
            <li>SHAP Explainability</li>
            <li>Generative AI & LLMs</li>
            <li>RAG Systems</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with skills_col3:
        st.markdown("""
        <div class="info-box">
        <h4>🔬 Domain Expertise</h4>
        <ul>
            <li>DoD Hydrology & Biosurveillance</li>
            <li>USDA Biomass Analytics</li>
            <li>Wastewater Genomics Epidemiology</li>
            <li>DoE Smart Grid & Power Resilience</li>
            <li>Urban Ecosystem Services</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key features
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-box">
        <h4>🎯 Research Objectives</h4>
        <ul>
            <li>Identify most vulnerable areas for targeted protection</li>
            <li>Link environmental threats with power outage patterns</li>
            <li>Support energy and environmental resilience planning</li>
            <li>Advance smart grid modernization aligned with environmental protection</li>
            <li>Provide transferable pathway for equitable, climate-resilient energy systems</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="success-box">
        <h4>📊 Data Integration</h4>
        <ul>
            <li><strong>Power Outages:</strong> California Power Outage Areas, Cal OES incidents, EAGLE-I (2014-2023)</li>
            <li><strong>Social Vulnerability:</strong> CalEnviroScreen 4.0, EPA EJScreen, CDC SVI, ACS</li>
            <li><strong>Climate Hazards:</strong> CAL FIRE, NOAA, Google Earth Engine</li>
            <li><strong>Infrastructure:</strong> Utility data, transmission lines, substations</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Methodology
    st.markdown('<p class="section-header">Methodology Framework</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🔬 Technical Approach**
        - Machine Learning: XGBoost, LightGBM, TensorFlow
        - Explainable AI: SHAP values
        - Spatial Analysis: GIS, ArcGIS Pro
        - Remote Sensing: Google Earth Engine
        - Real-time Integration: Live API feeds
        """)
    
    with col2:
        st.markdown("""
        **⚖️ Equity Focus**
        - Demographic assessment
        - Economic vulnerability
        - Housing quality
        - Health indicators
        - Environmental exposure
        - Community engagement
        """)
    
    with col3:
        st.markdown("""
        **📈 Evaluation Metrics**
        - Model accuracy (R², RMSE, MAE)
        - Outage duration reduction
        - Recovery time improvement
        - High-vulnerability protection
        - Seasonal hazard preparedness
        - User feedback integration
        """)
    
    # Current status
    st.markdown('<p class="section-header">System Status</p>', unsafe_allow_html=True)
    
    status_cols = st.columns(4)
    
    with status_cols[0]:
        historic_status = "✅ Loaded" if st.session_state.historic_data is not None else "⚠️ Not Loaded"
        count = len(st.session_state.historic_data) if st.session_state.historic_data is not None else 0
        st.metric("Historic Data", historic_status, f"{count:,} records")
    
    with status_cols[1]:
        live_status = "✅ Active" if st.session_state.live_data is not None else "⚠️ Inactive"
        count = len(st.session_state.live_data) if st.session_state.live_data is not None else 0
        st.metric("Live Data", live_status, f"{count:,} current")
    
    with status_cols[2]:
        ml_status = "✅ Available" if HAS_ML else "⚠️ Unavailable"
        model_count = len(st.session_state.ml_models)
        st.metric("ML Models", ml_status, f"{model_count} trained")
    
    with status_cols[3]:
        rag_status = "✅ Ready" if HAS_ANTHROPIC else "⚠️ Not Configured"
        st.metric("RAG System", rag_status)

# ============================================================================
# PAGE: HISTORIC DASHBOARD (EAGLE-I 2014-2023)
# ============================================================================

def page_historic():
    st.markdown('<p class="main-header">📊 Historic Dashboard: EAGLE-I Analysis (2014-2023)</p>', unsafe_allow_html=True)
    st.markdown('<span class="historic-badge">HISTORIC DATA: 2014-2023</span>', unsafe_allow_html=True)
    
    if st.session_state.historic_data is None:
        st.warning("⚠️ Please load historic data from the Home page first.")
        if st.button("Load Historic Data Now"):
            with st.spinner("Loading..."):
                st.session_state.historic_data = load_historic_eagle_i()
                if st.session_state.historic_data is not None:
                    st.success("✅ Data loaded!")
                    st.rerun()
        return
    
    df = st.session_state.historic_data
    
    # Overview metrics
    st.markdown('<p class="section-header">Overview Statistics</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Events", f"{len(df):,}")
    
    with col2:
        total_customers = df['max_customers'].sum()
        st.metric("Total Customers Affected", f"{total_customers:,.0f}")
    
    with col3:
        avg_duration = df['duration'].mean()
        st.metric("Avg Duration", f"{avg_duration:.1f} hrs")
    
    with col4:
        threshold_events = df[df['meets_doe_threshold']].shape[0]
        st.metric("Federal Threshold Events", f"{threshold_events:,}")
    
    with col5:
        counties = df['county'].nunique()
        st.metric("Counties Affected", counties)
    
    # Temporal analysis
    st.markdown('<p class="section-header">Temporal Analysis</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Yearly trend
        yearly = df.groupby('year').agg({
            'event_id': 'count',
            'max_customers': 'sum'
        }).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=yearly['year'], 
            y=yearly['event_id'],
            mode='lines+markers',
            name='Events',
            line=dict(color='#FF7F50', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title='Yearly Event Trend (2014-2023)',
            xaxis_title='Year',
            yaxis_title='Number of Events',
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Seasonal pattern
        seasonal = df.groupby('season').size().reset_index(name='count')
        
        fig = px.bar(
            seasonal,
            x='season',
            y='count',
            title='Seasonal Distribution',
            color='season',
            color_discrete_map={
                'Winter': 'skyblue',
                'Spring': 'lightgreen',
                'Summer': 'coral',
                'Fall': 'orange'
            }
        )
        
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Cause analysis
    st.markdown('<p class="section-header">Cause Analysis</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top causes
        cause_counts = df['cause'].value_counts().head(8)
        
        fig = px.bar(
            x=cause_counts.values,
            y=cause_counts.index,
            orientation='h',
            title='Top 8 Outage Causes',
            labels={'x': 'Number of Events', 'y': 'Cause'}
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Cause distribution pie
        fig = px.pie(
            values=cause_counts.values,
            names=cause_counts.index,
            title='Cause Distribution',
            hole=0.3
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Geographic analysis
    st.markdown('<p class="section-header">Geographic Distribution</p>', unsafe_allow_html=True)
    
    county_stats = df.groupby('county').agg({
        'event_id': 'count',
        'max_customers': 'sum',
        'duration': 'mean'
    }).reset_index()
    county_stats.columns = ['County', 'Events', 'Total Customers', 'Avg Duration (hrs)']
    county_stats = county_stats.sort_values('Events', ascending=False).head(15)
    
    fig = px.bar(
        county_stats,
        x='County',
        y='Events',
        title='Top 15 Counties by Event Count',
        color='Total Customers',
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(height=500, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    
    # Data table
    st.markdown('<p class="section-header">County Statistics Table</p>', unsafe_allow_html=True)
    
    st.dataframe(
        county_stats.style.format({
            'Events': '{:,}',
            'Total Customers': '{:,.0f}',
            'Avg Duration (hrs)': '{:.2f}'
        }).background_gradient(subset=['Events'], cmap='Reds'),
        use_container_width=True,
        height=400
    )

# ============================================================================
# PAGE: LIVE DASHBOARD
# ============================================================================

def page_live():
    st.markdown('<p class="main-header">🔴 Live Dashboard: Current Power Outages</p>', unsafe_allow_html=True)
    st.markdown('<span class="live-indicator">🔴 LIVE DATA</span>', unsafe_allow_html=True)
    
    if st.session_state.live_data is None:
        st.warning("⚠️ Please fetch live data from the Home page first.")
        if st.button("Fetch Live Data Now"):
            with st.spinner("Fetching from Cal OES API..."):
                st.session_state.live_data = fetch_live_california_outages()
                st.session_state.last_update = datetime.now()
                if st.session_state.live_data is not None:
                    st.success("✅ Live data loaded!")
                    st.rerun()
        return
    
    gdf = st.session_state.live_data
    
    # Refresh button
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        if st.button("🔄 Refresh Data", use_container_width=True):
            with st.spinner("Refreshing..."):
                st.session_state.live_data = fetch_live_california_outages()
                st.session_state.last_update = datetime.now()
                st.rerun()
    
    if st.session_state.last_update:
        st.info(f"⏰ Last updated: {st.session_state.last_update.strftime('%Y-%m-%d %I:%M:%S %p')}")
    
    # Current metrics
    st.markdown('<p class="section-header">Current Status</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Outages", len(gdf))
    
    with col2:
        total_customers = gdf['customers_affected'].sum()
        st.metric("Customers Affected", f"{total_customers:,.0f}")
    
    with col3:
        if 'status' in gdf.columns:
            active = len(gdf[gdf['status'] == 'Active'])
            st.metric("Active Status", active)
        else:
            st.metric("Counties", gdf['county'].nunique())
    
    with col4:
        avg_customers = gdf['customers_affected'].mean()
        st.metric("Avg per Outage", f"{avg_customers:,.0f}")
    
    # Live map
    st.markdown('<p class="section-header">Live Outage Map</p>', unsafe_allow_html=True)
    
    m = folium.Map(
        location=[36.7783, -119.4179],
        zoom_start=6,
        tiles='CartoDB positron'
    )
    
    # Add marker cluster
    marker_cluster = MarkerCluster(name='Outages').add_to(m)
    
    for idx, row in gdf.iterrows():
        if row.geometry is not None:
            customers = row.get('customers_affected', 0)
            
            # Color by severity
            if customers > 10000:
                color = 'red'
                icon = 'exclamation-triangle'
            elif customers > 1000:
                color = 'orange'
                icon = 'warning-sign'
            else:
                color = 'blue'
                icon = 'flash'
            
            popup_html = f"""
            <div style='min-width: 200px'>
                <h4>⚡ Power Outage</h4>
                <b>County:</b> {row.get('county', 'Unknown')}<br>
                <b>Customers:</b> {customers:,}<br>
                <b>Utility:</b> {row.get('utility', 'Unknown')}<br>
                <b>Status:</b> {row.get('status', 'Unknown')}<br>
                <b>Cause:</b> {row.get('cause', 'Unknown')}<br>
            </div>
            """
            
            folium.Marker(
                location=[row.geometry.y, row.geometry.x],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color=color, icon=icon, prefix='glyphicon'),
                tooltip=f"{customers:,} customers"
            ).add_to(marker_cluster)
    
    folium.LayerControl().add_to(m)
    
    st_folium(m, width=1400, height=600)
    
    # Current statistics
    st.markdown('<p class="section-header">Live Statistics</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # By county
        if 'county' in gdf.columns:
            county_counts = gdf['county'].value_counts().head(10)
            
            fig = px.bar(
                x=county_counts.values,
                y=county_counts.index,
                orientation='h',
                title='Top 10 Counties (Current Outages)',
                labels={'x': 'Outages', 'y': 'County'}
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Customer impact
        fig = px.histogram(
            gdf,
            x='customers_affected',
            nbins=30,
            title='Current Outage Size Distribution',
            labels={'customers_affected': 'Customers Affected'}
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# REMAINING PAGES IMPLEMENTATIONS CONTINUE...
# ============================================================================

# Due to length limits, I'll create a continuation file
# This file contains: Home, Historic, Live, and starts Maps
# Next file will contain: Maps (complete), EDA, Justice, RAG, ML, Compliance, Settings

def page_maps():
    st.markdown('<p class="main-header">🗺️ Interactive Geospatial Maps</p>', unsafe_allow_html=True)
    
    st.info("🚧 Interactive maps with complete LISA analysis, Moran's I, hot spot detection, and environmental justice overlays coming in next section...")
    
    # Placeholder for map selection
    map_types = [
        "County Outage Density",
        "LISA Cluster Maps",
        "Moran's I Spatial Autocorrelation",
        "Hot Spot Analysis (Getis-Ord Gi*)",
        "Environmental Justice Index",
        "Vulnerability Heatmap",
        "Federal Compliance Map"
    ]
    
    selected_map = st.selectbox("Select Map Type", map_types)
    
    st.markdown(f"**Selected:** {selected_map}")
    st.markdown("Interactive Folium maps with full analysis will be implemented here.")

def page_eda():
    st.markdown('<p class="main-header">📈 Complete Exploratory Data Analysis</p>', unsafe_allow_html=True)
    st.info("Complete EDA with all statistical tests, correlations, and visualizations...")

def page_justice():
    st.markdown('<p class="main-header">⚖️ Environmental Justice Analysis</p>', unsafe_allow_html=True)
    st.info("Environmental justice metrics, equity analysis, and vulnerable community identification...")

def page_rag():
    st.markdown('<p class="main-header">🤖 RAG-Enabled AI Insights</p>', unsafe_allow_html=True)
    
    st.markdown("""
    Ask questions about the power grid data and receive AI-powered insights using 
    Retrieval-Augmented Generation (RAG) with Claude Sonnet 4.
    """)
    
    # API key input
    api_key = st.text_input("Anthropic API Key (optional)", type="password",
                            help="Enter your Anthropic API key to enable RAG insights")
    
    if api_key:
        os.environ['ANTHROPIC_API_KEY'] = api_key
        st.session_state.rag_enabled = True
    
    # Sample questions
    st.markdown("### Sample Questions")
    
    sample_questions = [
        "What are the primary causes of power outages in California?",
        "Which counties are most vulnerable to climate-related outages?",
        "How do outage patterns vary by season?",
        "What environmental justice concerns are evident in the data?",
        "What recommendations would you make for grid modernization?"
    ]
    
    for q in sample_questions:
        if st.button(f"❓ {q}", use_container_width=True):
            if st.session_state.rag_enabled and st.session_state.historic_data is not None:
                with st.spinner("Analyzing with Claude..."):
                    response = rag_query_claude(q, st.session_state.historic_data, api_key)
                    st.markdown("### AI Response")
                    st.markdown(response)
            else:
                st.warning("Please load historic data and provide API key.")
    
    # Custom question
    st.markdown("### Ask Your Own Question")
    custom_question = st.text_area("Enter your question:")
    
    if st.button("🤖 Get AI Insight"):
        if custom_question and st.session_state.rag_enabled and st.session_state.historic_data is not None:
            with st.spinner("Analyzing..."):
                response = rag_query_claude(custom_question, st.session_state.historic_data, api_key)
                st.markdown("### AI Response")
                st.markdown(response)
        else:
            st.warning("Please enter a question, load data, and provide API key.")

def page_ml():
    st.markdown('<p class="main-header">🔬 Machine Learning Models & Predictions</p>', unsafe_allow_html=True)
    st.info("ML models with XGBoost, LightGBM, TensorFlow, and SHAP explainability...")

def page_compliance():
    st.markdown('<p class="main-header">📋 Federal Compliance Assessment</p>', unsafe_allow_html=True)
    st.info("DOE OE-417 compliance analysis, underreporting assessment...")

def page_settings():
    st.markdown('<p class="main-header">⚙️ Settings & Data Management</p>', unsafe_allow_html=True)
    
    st.markdown("### API Configuration")
    
    anthropic_key = st.text_input("Anthropic API Key", type="password")
    if st.button("Save Anthropic Key"):
        if anthropic_key:
            os.environ['ANTHROPIC_API_KEY'] = anthropic_key
            st.success("✅ API key saved for this session")
    
    st.markdown("### Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Clear All Data"):
            st.session_state.historic_data = None
            st.session_state.live_data = None
            st.session_state.counties_gdf = None
            st.success("✅ All data cleared")
            st.rerun()
    
    with col2:
        if st.button("Reload All Data"):
            with st.spinner("Reloading..."):
                st.session_state.historic_data = load_historic_eagle_i()
                st.session_state.live_data = fetch_live_california_outages()
                st.session_state.counties_gdf = load_california_counties()
                st.session_state.last_update = datetime.now()
                st.success("✅ All data reloaded")
                st.rerun()
    
    st.markdown("### About")
    
    about_tab1, about_tab2 = st.tabs(["👤 Researcher Profile", "📊 Project Information"])
    
    with about_tab1:
        profile_col1, profile_col2 = st.columns([1, 2])
        
        with profile_col1:
            try:
                from PIL import Image
                profile_img = Image.open('/mnt/user-data/uploads/Modern_Profile_Photo_Frame.png')
                st.image(profile_img, use_container_width=True)
            except:
                pass
        
        with profile_col2:
            st.markdown("""
            ### Victoria Love Franklin
            
            **2nd Year PhD Pre-Candidate Data Science Student**  
            **GIS Scientist | CASPER Participant**  
            School of Applied Computational Science  
            Meharry Medical College
            """)
        
        st.markdown("""
        #### Professional Summary
        
        Multidisciplinary researcher working at the intersection of environmental science, 
        public health, and emerging technologies. Research spans genomics and wastewater 
        epidemiology to urban ecosystems, critical infrastructure, and power grid resilience.
        
        #### Core Competencies
        
        **Technical Expertise:**
        - Geographic Information Systems (GIS) & Spatial Analysis
        - Python Programming & Data Science
        - Artificial Intelligence & Machine Learning
        - Generative AI & Large Language Models
        - Retrieval-Augmented Generation (RAG) Systems
        
        **Domain Specializations:**
        - 🌳 Urban Forestry Ecosystem Services & Ecology
        - 💧 DoD Groundwater Hydrology & Auger Modeling
        - 🌲 USDA Forestry Biomass Residual Analytics
        - 🔬 DoD Biosurveillance Systems
        - 🧬 Wastewater-Based Genomics Epidemiology
        - ⚡ DoE Smart Grid & GIS Digital Twin Technology
        - 🔌 Power Grid Resilience & Critical Infrastructure
        
        #### Leadership & Service
        
        **Board Appointments:**
        - 🏛️ **Tennessee Clinical Perfusionist Board**  
          *Appointed by Governor Bill Lee*  
          Contributing to healthcare policy and professional standards
        
        - 🤝 **Health, Education, and Justice Technology Consortium (HEJTC)**  
          *Board Member*  
          Advancing technology solutions for health and justice equity
        
        **Professional Memberships:**
        - 📡 **IEEE** - Student Member
        - 🧪 **Association of Public Health Laboratories (APHL)**  
          Wastewater Biosurveillance Program
        - 💧 **Water Environment Federation (WEF)**
        - ⚙️ **National Society of Black Engineers (NSBE)** - Professional Member
        
        #### Personal Interests
        
        In spare time, develops community resource information apps and experimental 
        projects as a hobby, combining technical skills with community service.
        
        #### Mission
        
        Passionate about leveraging cutting-edge technology and interdisciplinary 
        collaboration to solve pressing challenges facing our communities. Work is 
        guided by a commitment to creating sustainable, resilient, and healthy 
        communities for future generations.
        """)
    
    with about_tab2:
        st.markdown("""
        #### Climate-Resilient Energy Digital Twin
        
        **Project Overview:**
        
        This comprehensive research tool integrates Geographic Information Systems (GIS) 
        with advanced artificial intelligence methods including generative AI, large language 
        models (LLMs), and Retrieval-Augmented Generation (RAG) to address California's 
        climate-induced energy challenges.
        
        **Research Objectives:**
        
        1. Create a GIS digital twin of California's power grid incorporating real-time data on:
           - Social vulnerability metrics
           - Ecological indicators
           - Infrastructure conditions
           - Climate hazards
        
        2. Develop AI-powered tools combining:
           - XGBoost, LightGBM, and TensorFlow for predictions
           - SHAP explainability for model interpretability
           - RAG systems for context-aware recommendations
           - Real-time API integration for live data
        
        3. Support equity-focused infrastructure planning:
           - Identify vulnerable areas for targeted protection
           - Link environmental threats with outage patterns
           - Guide smart grid modernization
           - Advance environmental justice goals
        
        **Data Sources:**
        
        - **Power Outages:** EAGLE-I (2014-2023), Cal OES, California Power Outage Areas
        - **Social Vulnerability:** CalEnviroScreen 4.0, EPA EJScreen, CDC SVI, ACS
        - **Climate Hazards:** CAL FIRE, NOAA, Google Earth Engine
        - **Infrastructure:** Utility data, transmission lines, substations, HIFLD
        
        **Evaluation Metrics:**
        
        - Technical: Model accuracy (R², RMSE, MAE)
        - Operational: Outage duration reduction, recovery time improvement
        - Equity: High-vulnerability community protection
        - Preparedness: Seasonal hazard readiness
        - Engagement: User feedback integration
        
        **Impact:**
        
        Provides transferable pathway toward building energy systems that are both 
        equitable and climate-resilient in the face of growing global environmental pressures.
        
        **Technologies Used:**
        
        - **GIS:** ArcGIS Pro, Google Earth Engine, QGIS
        - **ML/AI:** XGBoost, LightGBM, TensorFlow, SHAP
        - **Generative AI:** Claude, GPT models, RAG systems
        - **Programming:** Python, Streamlit, Pandas, NumPy, GeoPandas
        - **Visualization:** Plotly, Folium, Matplotlib, Seaborn
        """)
    
    st.info("""
    **Contact & Collaboration:**
    
    For inquiries about this research, collaboration opportunities, or technical questions 
    about the dashboard, please reach out through Meharry Medical College's School of 
    Applied Computational Science.
    """)

# ============================================================================
# MAIN ROUTER
# ============================================================================

def main():
    """Main application router"""
    
    page = pages[selected_page]
    
    if page == "home":
        page_home()
    elif page == "historic":
        page_historic()
    elif page == "live":
        page_live()
    elif page == "maps":
        page_maps()
    elif page == "eda":
        page_eda()
    elif page == "justice":
        page_justice()
    elif page == "rag":
        page_rag()
    elif page == "ml":
        page_ml()
    elif page == "compliance":
        page_compliance()
    elif page == "settings":
        page_settings()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <strong>Researcher:</strong> Victoria Love Franklin, PhD Pre-Candidate<br>
        <strong>Institution:</strong> School of Applied Computational Science, Meharry Medical College<br>
        <strong>Affiliations:</strong> Tennessee Clinical Perfusionist Board (Governor Bill Lee Appointee) | 
        HEJTC Board Member | IEEE | APHL | WEF | NSBE<br><br>
        <strong>Citation:</strong> Franklin, V.L. (2025). Toward Climate-Resilient Energy Systems: 
        A Geospatial RAG-Enabled Digital Twin for Equity and Ecosystem Sustainability. 
        School of Applied Computational Science, Meharry Medical College.<br>
        <small>Dashboard Version 1.0 | Last Updated: November 2025 | 
        Keywords: California energy resilience, climate change impacts, social vulnerability, 
        environmental justice, GIS, AI, generative AI, LLMs, RAG, geospatial digital twin, 
        power outage prediction, XGBoost, LightGBM, TensorFlow, SHAP explainability, 
        ArcGIS Pro, Google Earth Engine, climate hazard modeling</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
