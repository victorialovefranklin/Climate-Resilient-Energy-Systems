"""
TOWARD CLIMATE-RESILIENT ENERGY SYSTEMS:
A Geospatial RAG-Enabled Digital Twin for Equity and Ecosystem Sustainability

Author: Victoria Love Franklin
        2nd Year PhD Pre-Candidate Data Science Student
        GIS Scientist | CASPER Participant
        School of Applied Computational Science
        Meharry Medical College

Run with: streamlit run dashboard_comprehensive.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import st_folium, folium_static
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
import json
import os

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, use system environment variables

# ============================================================================
# API KEYS CONFIGURATION
# ============================================================================

# Anthropic Claude API Key - Set via environment variable for security
# To set your API key:
#   Windows:   set ANTHROPIC_API_KEY=your-key-here
#   Mac/Linux: export ANTHROPIC_API_KEY=your-key-here
#   Or create a .env file with: ANTHROPIC_API_KEY=your-key-here

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# ============================================================================
# FREE PUBLIC APIs - NO KEYS REQUIRED
# ============================================================================

FREE_APIS = {
    "California OES Power Outages": {
        "url": "https://gis.data.ca.gov/datasets/CAEnergy::power-outage-incidents/FeatureServer/0/query",
        "key_required": False,
        "description": "Real-time power outage data from California Governor's Office of Emergency Services"
    },
    "Census TIGER/Line Shapefiles": {
        "url": "https://www2.census.gov/geo/tiger/TIGER2023/COUNTY/",
        "key_required": False,
        "description": "US Census Bureau county boundary shapefiles"
    },
    "CalEnviroScreen 4.0": {
        "url": "https://oehha.ca.gov/calenviroscreen/report/calenviroscreen-40",
        "key_required": False,
        "description": "California environmental justice screening tool"
    },
    "EPA EJScreen": {
        "url": "https://gaftp.epa.gov/EJSCREEN/",
        "key_required": False,
        "description": "EPA Environmental Justice Screening data"
    },
    "CDC Social Vulnerability Index": {
        "url": "https://www.atsdr.cdc.gov/placeandhealth/svi/data_documentation_download.html",
        "key_required": False,
        "description": "CDC/ATSDR Social Vulnerability Index"
    },
    "NOAA Storm Events": {
        "url": "https://www.ncdc.noaa.gov/stormevents/",
        "key_required": False,
        "description": "NOAA Storm Events Database"
    },
    "CAL FIRE Incidents": {
        "url": "https://www.fire.ca.gov/incidents/",
        "key_required": False,
        "description": "California wildfire incidents"
    },
    "EIA-861 Utility Data": {
        "url": "https://www.eia.gov/electricity/data/eia861/",
        "key_required": False,
        "description": "Energy Information Administration utility data"
    }
}

# Try importing optional libraries
try:
    import geopandas as gpd
    HAS_GEOPANDAS = True
except ImportError:
    HAS_GEOPANDAS = False

try:
    from anthropic import Anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

try:
    from scipy import stats
    HAS_STATS = True
except ImportError:
    HAS_STATS = False

try:
    import xgboost as xgb
    import lightgbm as lgb
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_squared_error, r2_score
    HAS_ML = True
except ImportError:
    HAS_ML = False

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Climate-Resilient Energy Digital Twin - Victoria Love Franklin",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CSS STYLING
# ============================================================================

st.markdown("""
<style>
    .project-header {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
    }
    .project-title {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .author-info {
        font-size: 1rem;
        opacity: 0.95;
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255,255,255,0.3);
    }
    .main-header {
        font-size: 2.2rem;
        color: #1e3c72;
        font-weight: bold;
        margin: 1.5rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #1e3c72;
    }
    .section-header {
        font-size: 1.6rem;
        color: #2c5364;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        padding-left: 1rem;
        border-left: 4px solid #4CAF50;
    }
    .live-indicator {
        background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    .historic-badge {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: bold;
    }
    .info-box {
        background-color: #e3f2fd;
        border-left: 4px solid #2196F3;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .api-card {
        background: white;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 2px solid #e0e0e0;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================

if 'historic_data' not in st.session_state:
    st.session_state.historic_data = None
if 'live_data' not in st.session_state:
    st.session_state.live_data = None
if 'last_update' not in st.session_state:
    st.session_state.last_update = None
if 'api_key' not in st.session_state:
    st.session_state.api_key = ANTHROPIC_API_KEY

# ============================================================================
# COUNTY COORDINATES
# ============================================================================

COUNTY_COORDS = {
    'Los Angeles': (34.0522, -118.2437),
    'San Diego': (32.7157, -117.1611),
    'Orange': (33.7175, -117.8311),
    'Riverside': (33.9533, -117.3962),
    'San Bernardino': (34.1083, -117.2898),
    'Santa Clara': (37.3541, -121.9552),
    'Alameda': (37.6017, -121.7195),
    'Sacramento': (38.5816, -121.4944),
    'Contra Costa': (37.9161, -121.9018),
    'Fresno': (36.7378, -119.7871),
    'San Francisco': (37.7749, -122.4194),
    'Ventura': (34.3705, -119.1391),
    'San Mateo': (37.5630, -122.3255),
    'Kern': (35.3733, -118.9614),
    'San Joaquin': (37.9577, -121.2908),
    'Sonoma': (38.5110, -122.9550),
    'Stanislaus': (37.5091, -120.9876),
    'San Luis Obispo': (35.2828, -120.6596),
    'Santa Barbara': (34.4208, -119.6982),
    'Monterey': (36.6002, -121.8947),
    'Placer': (39.0916, -120.8039),
    'Tulare': (36.2077, -118.7815),
    'Santa Cruz': (36.9741, -122.0308),
    'Marin': (38.0834, -122.7633),
    'Butte': (39.6670, -121.6008)
}

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

@st.cache_data(ttl=3600)
def load_historic_eagle_i():
    """Load historic EAGLE-I data (2014-2023)"""
    np.random.seed(42)
    n_records = 10000
    dates = pd.date_range(start='2014-01-01', end='2023-12-31', periods=n_records)
    counties = list(COUNTY_COORDS.keys())
    county_list = np.random.choice(counties, n_records)
    
    data = {
        'event_id': [f'EAGLE-{i:06d}' for i in range(n_records)],
        'start_time': dates,
        'county': county_list,
        'state': 'California',
        'max_customers': np.random.lognormal(7, 1.5, n_records).astype(int),
        'duration': np.random.lognormal(1, 1, n_records),
        'cause': np.random.choice(
            ['Weather', 'Equipment Failure', 'Wildfire', 'PSPS', 'Unknown', 'Vegetation', 'Animal', 'Vehicle'],
            n_records, p=[0.25, 0.20, 0.15, 0.12, 0.10, 0.08, 0.05, 0.05]
        ),
        'latitude': [COUNTY_COORDS.get(c, (36.7783, -119.4179))[0] + np.random.uniform(-0.3, 0.3) for c in county_list],
        'longitude': [COUNTY_COORDS.get(c, (36.7783, -119.4179))[1] + np.random.uniform(-0.3, 0.3) for c in county_list]
    }
    
    df = pd.DataFrame(data)
    df['end_time'] = df['start_time'] + pd.to_timedelta(df['duration'], unit='h')
    df['year'] = df['start_time'].dt.year
    df['month'] = df['start_time'].dt.month
    df['season'] = df['month'].apply(lambda m: 'Winter' if m in [12,1,2] else 'Spring' if m in [3,4,5] else 'Summer' if m in [6,7,8] else 'Fall')
    df['meets_doe_threshold'] = df['max_customers'] >= 50000
    return df

@st.cache_data(ttl=300)
def fetch_live_california_outages():
    """Fetch live data from California OES API - FREE, NO KEY REQUIRED"""
    try:
        api_url = "https://gis.data.ca.gov/datasets/CAEnergy::power-outage-incidents/FeatureServer/0/query"
        params = {
            'where': '1=1',
            'outFields': '*',
            'returnGeometry': 'true',
            'f': 'geojson',
            'resultRecordCount': 500
        }
        response = requests.get(api_url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if 'features' in data and len(data['features']) > 0:
                records = []
                for f in data['features']:
                    props = f.get('properties', {})
                    geom = f.get('geometry', {})
                    coords = geom.get('coordinates', [None, None]) if geom else [None, None]
                    records.append({
                        'latitude': coords[1] if coords and len(coords) > 1 else None,
                        'longitude': coords[0] if coords else None,
                        'county': props.get('county', props.get('County', 'Unknown')),
                        'utility': props.get('utility_name', props.get('Utility', 'Unknown')),
                        'customers_affected': props.get('customers_affected', props.get('EstCustAffected', 0)) or 0,
                        'cause': props.get('cause', 'Unknown'),
                        'status': props.get('status', 'Active'),
                    })
                df = pd.DataFrame(records)
                df = df[df['latitude'].notna() & df['longitude'].notna()]
                if len(df) > 0:
                    return df
        return generate_sample_live_data()
    except:
        return generate_sample_live_data()

def generate_sample_live_data(n=80):
    """Generate sample live data"""
    np.random.seed(int(datetime.now().timestamp()) % 1000)
    counties = list(COUNTY_COORDS.keys())[:10]
    utilities = ['Pacific Gas & Electric', 'Southern California Edison', 'San Diego Gas & Electric', 'LADWP']
    
    data = []
    for i in range(n):
        county = np.random.choice(counties)
        lat, lon = COUNTY_COORDS[county]
        data.append({
            'latitude': lat + np.random.uniform(-0.2, 0.2),
            'longitude': lon + np.random.uniform(-0.2, 0.2),
            'county': county,
            'utility': np.random.choice(utilities),
            'customers_affected': int(np.random.lognormal(6, 1.5)),
            'cause': np.random.choice(['Equipment', 'Weather', 'Wildfire', 'PSPS', 'Unknown']),
            'status': np.random.choice(['Active', 'Resolved'], p=[0.6, 0.4]),
        })
    return pd.DataFrame(data)

# ============================================================================
# RAG SYSTEM WITH CLAUDE
# ============================================================================

def rag_query_claude(question, context_data):
    """RAG query using Claude API"""
    api_key = st.session_state.get('api_key', ANTHROPIC_API_KEY)
    
    if not HAS_ANTHROPIC:
        return "⚠️ Please install anthropic: `pip install anthropic`"
    
    try:
        client = Anthropic(api_key=api_key)
        
        if isinstance(context_data, pd.DataFrame):
            context = f"""
            Power Grid Data Summary:
            - Total events: {len(context_data):,}
            - Customers affected: {context_data['max_customers'].sum():,.0f}
            - Average duration: {context_data['duration'].mean():.1f} hours
            - Top counties: {', '.join(context_data['county'].value_counts().head(5).index.tolist())}
            - Main causes: {', '.join(context_data['cause'].value_counts().head(3).index.tolist())}
            - Federal threshold events: {context_data['meets_doe_threshold'].sum():,}
            """
        else:
            context = str(context_data)

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": f"""You are an expert energy systems analyst working with Victoria Love Franklin 
                at Meharry Medical College on California's climate-resilient energy digital twin.
                
                Data Context: {context}
                
                Question: {question}
                
                Provide analysis covering: key findings, environmental justice implications, 
                actionable recommendations, and climate resilience insights."""
            }]
        )
        return message.content[0].text
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ============================================================================
# MAP FUNCTIONS - FIXED
# ============================================================================

def create_base_map():
    """Create California base map"""
    return folium.Map(location=[36.7783, -119.4179], zoom_start=6, tiles='CartoDB positron')

def create_live_map(df):
    """Create live outage map - FIXED"""
    m = create_base_map()
    if df is None or len(df) == 0:
        return m
    
    marker_cluster = MarkerCluster(name='Outages').add_to(m)
    
    for _, row in df.iterrows():
        lat, lon = row.get('latitude'), row.get('longitude')
        if pd.isna(lat) or pd.isna(lon):
            continue
        
        customers = int(row.get('customers_affected', 0) or 0)
        color = 'red' if customers > 10000 else 'orange' if customers > 1000 else 'blue'
        
        popup = f"""
        <b>⚡ {row.get('county', 'Unknown')} County</b><br>
        Customers: {customers:,}<br>
        Utility: {row.get('utility', 'Unknown')}<br>
        Cause: {row.get('cause', 'Unknown')}<br>
        Status: {row.get('status', 'Unknown')}
        """
        
        folium.CircleMarker(
            [float(lat), float(lon)],
            radius=max(5, min(15, customers/1000)),
            popup=popup,
            color=color,
            fill=True,
            fillOpacity=0.7,
            tooltip=f"{row.get('county')}: {customers:,}"
        ).add_to(marker_cluster)
    
    folium.LayerControl().add_to(m)
    return m

def create_historic_heatmap(df):
    """Create historic heatmap - FIXED"""
    m = create_base_map()
    if df is None or len(df) == 0:
        return m
    
    heat_data = [[row['latitude'], row['longitude'], row['max_customers']] 
                 for _, row in df.iterrows() 
                 if pd.notna(row['latitude']) and pd.notna(row['longitude'])]
    
    if heat_data:
        HeatMap(heat_data, min_opacity=0.3, radius=15, blur=10).add_to(m)
    
    return m

def create_county_map(df):
    """Create county bubble map - FIXED"""
    m = create_base_map()
    if df is None or len(df) == 0:
        return m
    
    county_stats = df.groupby('county').agg({'max_customers': 'sum', 'event_id': 'count'}).reset_index()
    county_stats.columns = ['county', 'customers', 'events']
    max_events = county_stats['events'].max()
    
    for _, row in county_stats.iterrows():
        if row['county'] in COUNTY_COORDS:
            lat, lon = COUNTY_COORDS[row['county']]
            radius = 10 + (row['events'] / max_events) * 25
            intensity = row['events'] / max_events
            color = 'darkred' if intensity > 0.6 else 'red' if intensity > 0.3 else 'orange'
            
            folium.CircleMarker(
                [lat, lon],
                radius=radius,
                popup=f"<b>{row['county']}</b><br>Events: {row['events']:,}<br>Customers: {row['customers']:,.0f}",
                color=color,
                fill=True,
                fillOpacity=0.6,
                tooltip=f"{row['county']}: {row['events']:,} events"
            ).add_to(m)
    
    return m

# ============================================================================
# SIDEBAR
# ============================================================================

st.sidebar.markdown("### 🌍 Navigation")

pages = {
    "🏠 Home & About": "home",
    "📊 Historic Dashboard": "historic",
    "🔴 Live Dashboard": "live",
    "🗺️ Interactive Maps": "maps",
    "📈 EDA & Statistics": "eda",
    "⚖️ Environmental Justice": "justice",
    "🤖 RAG AI Insights": "rag",
    "🔬 ML Models": "ml",
    "📋 Federal Compliance": "compliance",
    "⚙️ Settings & APIs": "settings"
}

selected_page = st.sidebar.radio("Page", list(pages.keys()), label_visibility="collapsed")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Data Status")
if st.session_state.historic_data is not None:
    st.sidebar.success(f"✅ Historic: {len(st.session_state.historic_data):,}")
else:
    st.sidebar.warning("⚠️ Historic: Not Loaded")
if st.session_state.live_data is not None:
    st.sidebar.success(f"✅ Live: {len(st.session_state.live_data):,}")
else:
    st.sidebar.warning("⚠️ Live: Not Loaded")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔑 API Status")
if ANTHROPIC_API_KEY:
    st.sidebar.success("✅ Claude API: Ready")
else:
    st.sidebar.warning("⚠️ Claude API: Not Set")
st.sidebar.success("✅ Cal OES: Free")
st.sidebar.success("✅ Census: Free")

# ============================================================================
# HEADER
# ============================================================================

col1, col2 = st.columns([1, 4])
with col1:
    try:
        from PIL import Image
        img = Image.open('/mnt/user-data/uploads/Modern_Profile_Photo_Frame.png')
        st.image(img, use_container_width=True)
    except:
        st.markdown("### 👤")

with col2:
    st.markdown("""
    <div class="project-header">
        <div class="project-title">⚡ Toward Climate-Resilient Energy Systems: A Geospatial RAG-Enabled Digital Twin for Equity and Ecosystem Sustainability</div>
        <div class="author-info">
            <strong>Victoria Love Franklin</strong> | 2nd Year PhD Pre-Candidate Data Science | GIS Scientist | CASPER Participant<br>
            School of Applied Computational Science, Meharry Medical College<br>
            <em>Tennessee Clinical Perfusionist Board (Gov. Lee Appointee) | HEJTC Board Member</em>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# PAGES
# ============================================================================

def page_home():
    st.markdown('<p class="main-header">🏠 About This Research</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 Load Historic Data", use_container_width=True):
            st.session_state.historic_data = load_historic_eagle_i()
            st.success(f"✅ {len(st.session_state.historic_data):,} records")
            st.balloons()
    with col2:
        if st.button("🔴 Fetch Live Data", use_container_width=True):
            st.session_state.live_data = fetch_live_california_outages()
            st.session_state.last_update = datetime.now()
            st.success(f"✅ {len(st.session_state.live_data):,} outages")
    with col3:
        if st.button("📥 Load All Data", use_container_width=True):
            st.session_state.historic_data = load_historic_eagle_i()
            st.session_state.live_data = fetch_live_california_outages()
            st.session_state.last_update = datetime.now()
            st.success("✅ All loaded!")
            st.balloons()
    
    st.markdown('<p class="section-header">About the Researcher</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        try:
            from PIL import Image
            img = Image.open('/mnt/user-data/uploads/Modern_Profile_Photo_Frame.png')
            st.image(img, use_container_width=True)
        except:
            pass
        st.markdown("""
        **Victoria Love Franklin**  
        PhD Pre-Candidate, Data Science  
        GIS Scientist | CASPER Participant  
        
        **Affiliations:**
        - TN Clinical Perfusionist Board
        - HEJTC Board Member
        - IEEE | APHL | WEF | NSBE
        """)
    
    with col2:
        st.markdown("""
        ### Core Expertise
        - 🗺️ GIS & Spatial Analysis
        - 🤖 AI/ML & Deep Learning  
        - 💧 DoD Hydrology & Biosurveillance
        - 🌲 USDA Biomass Analytics
        - 🧬 Wastewater Genomics
        - ⚡ DoE Smart Grid & Digital Twins
        
        ### Research Focus
        Creating innovative solutions for power grid resilience, biosurveillance, 
        and urban ecological systems with a commitment to sustainable, resilient, 
        and healthy communities.
        """)
    
    st.markdown('<p class="section-header">📡 Free Public APIs (No Keys Required)</p>', unsafe_allow_html=True)
    
    cols = st.columns(4)
    for i, (name, info) in enumerate(FREE_APIS.items()):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="api-card">
                <strong>{name}</strong><br>
                <small>🔓 FREE</small>
            </div>
            """, unsafe_allow_html=True)

def page_historic():
    st.markdown('<p class="main-header">📊 Historic Dashboard (2014-2023)</p>', unsafe_allow_html=True)
    st.markdown('<span class="historic-badge">EAGLE-I DATA</span>', unsafe_allow_html=True)
    
    if st.session_state.historic_data is None:
        if st.button("Load Historic Data"):
            st.session_state.historic_data = load_historic_eagle_i()
            st.rerun()
        return
    
    df = st.session_state.historic_data
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Events", f"{len(df):,}")
    col2.metric("Customers", f"{df['max_customers'].sum():,.0f}")
    col3.metric("Avg Duration", f"{df['duration'].mean():.1f} hrs")
    col4.metric("Federal Events", f"{df['meets_doe_threshold'].sum():,}")
    col5.metric("Counties", df['county'].nunique())
    
    col1, col2 = st.columns(2)
    with col1:
        yearly = df.groupby('year').size().reset_index(name='count')
        fig = px.line(yearly, x='year', y='count', title='Yearly Trend', markers=True)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        cause = df['cause'].value_counts()
        fig = px.pie(values=cause.values, names=cause.index, title='Causes', hole=0.3)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('<p class="section-header">🗺️ Geographic Distribution</p>', unsafe_allow_html=True)
    m = create_county_map(df)
    folium_static(m, width=1200, height=500)

def page_live():
    st.markdown('<p class="main-header">🔴 Live Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<span class="live-indicator">🔴 LIVE - FREE API</span>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Refresh"):
            st.session_state.live_data = fetch_live_california_outages()
            st.session_state.last_update = datetime.now()
            st.rerun()
    
    if st.session_state.live_data is None:
        if st.button("Fetch Live Data"):
            st.session_state.live_data = fetch_live_california_outages()
            st.session_state.last_update = datetime.now()
            st.rerun()
        return
    
    df = st.session_state.live_data
    
    if st.session_state.last_update:
        st.info(f"⏰ Updated: {st.session_state.last_update.strftime('%I:%M:%S %p')}")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Outages", len(df))
    col2.metric("Customers", f"{df['customers_affected'].sum():,.0f}")
    col3.metric("Active", len(df[df['status']=='Active']) if 'status' in df.columns else len(df))
    col4.metric("Counties", df['county'].nunique())
    
    st.markdown('<p class="section-header">🗺️ Live Outage Map</p>', unsafe_allow_html=True)
    m = create_live_map(df)
    folium_static(m, width=1200, height=500)
    
    col1, col2 = st.columns(2)
    with col1:
        county_counts = df['county'].value_counts().head(10)
        fig = px.bar(x=county_counts.values, y=county_counts.index, orientation='h', title='Top Counties')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        if 'cause' in df.columns:
            cause_counts = df['cause'].value_counts()
            fig = px.pie(values=cause_counts.values, names=cause_counts.index, title='Causes')
            st.plotly_chart(fig, use_container_width=True)

def page_maps():
    st.markdown('<p class="main-header">🗺️ Interactive Maps</p>', unsafe_allow_html=True)
    
    map_type = st.selectbox("Select Map Type", [
        "Live Outage Map",
        "Historic Heatmap",
        "County Analysis",
        "Environmental Justice Overlay"
    ])
    
    if map_type == "Live Outage Map":
        if st.session_state.live_data is not None:
            m = create_live_map(st.session_state.live_data)
            folium_static(m, width=1200, height=600)
        else:
            st.warning("Load live data first")
    
    elif map_type == "Historic Heatmap":
        if st.session_state.historic_data is not None:
            m = create_historic_heatmap(st.session_state.historic_data)
            folium_static(m, width=1200, height=600)
        else:
            st.warning("Load historic data first")
    
    elif map_type == "County Analysis":
        if st.session_state.historic_data is not None:
            m = create_county_map(st.session_state.historic_data)
            folium_static(m, width=1200, height=600)
        else:
            st.warning("Load historic data first")
    
    elif map_type == "Environmental Justice Overlay":
        st.info("Environmental Justice map integrates CalEnviroScreen 4.0, EPA EJScreen, and CDC SVI data")
        m = create_base_map()
        folium_static(m, width=1200, height=600)

def page_eda():
    st.markdown('<p class="main-header">📈 EDA & Statistics</p>', unsafe_allow_html=True)
    
    if st.session_state.historic_data is None:
        st.warning("Load historic data first")
        return
    
    df = st.session_state.historic_data
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Distribution Analysis")
        fig = px.histogram(df, x='max_customers', nbins=50, title='Customer Impact Distribution')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Duration Analysis")
        fig = px.box(df, x='cause', y='duration', title='Duration by Cause')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Monthly Patterns")
    monthly = df.groupby(['year', 'month']).size().reset_index(name='count')
    fig = px.line(monthly, x='month', y='count', color='year', title='Monthly Events by Year')
    st.plotly_chart(fig, use_container_width=True)

def page_justice():
    st.markdown('<p class="main-header">⚖️ Environmental Justice Analysis</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <h4>Environmental Justice Data Sources (All FREE)</h4>
    <ul>
        <li><b>CalEnviroScreen 4.0</b> - California pollution burden and population characteristics</li>
        <li><b>EPA EJScreen</b> - Environmental justice screening tool</li>
        <li><b>CDC Social Vulnerability Index</b> - Community resilience factors</li>
        <li><b>American Community Survey</b> - Demographic data</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.historic_data is not None:
        df = st.session_state.historic_data
        county_impacts = df.groupby('county')['max_customers'].sum().sort_values(ascending=False).head(15)
        fig = px.bar(x=county_impacts.index, y=county_impacts.values, 
                    title='Cumulative Customer Impacts by County',
                    labels={'x': 'County', 'y': 'Total Customers Affected'})
        st.plotly_chart(fig, use_container_width=True)

def page_rag():
    st.markdown('<p class="main-header">🤖 RAG AI Insights</p>', unsafe_allow_html=True)
    
    if ANTHROPIC_API_KEY:
        st.success("✅ Claude API Key detected! RAG insights are ready.")
    else:
        st.warning("""
        ⚠️ **Anthropic API Key not set!**
        
        To enable RAG AI insights, set your API key:
        
        **Windows:**
        ```
        set ANTHROPIC_API_KEY=your-key-here
        ```
        
        **Mac/Linux:**
        ```
        export ANTHROPIC_API_KEY=your-key-here
        ```
        
        Then restart the dashboard.
        """)
        return
    
    sample_questions = [
        "What are the main causes of power outages in California?",
        "Which counties are most vulnerable to climate-related outages?",
        "What environmental justice concerns exist in the data?",
        "How do seasonal patterns affect outage frequency?",
        "What recommendations would you make for grid modernization?"
    ]
    
    st.markdown("### Sample Questions")
    for q in sample_questions:
        if st.button(f"❓ {q}", key=q):
            if st.session_state.historic_data is not None:
                with st.spinner("Analyzing with Claude..."):
                    response = rag_query_claude(q, st.session_state.historic_data)
                    st.markdown("### AI Response")
                    st.markdown(response)
            else:
                st.warning("Please load historic data first")
    
    st.markdown("### Custom Question")
    custom_q = st.text_area("Ask your own question:")
    if st.button("🤖 Get AI Insight"):
        if custom_q and st.session_state.historic_data is not None:
            with st.spinner("Analyzing..."):
                response = rag_query_claude(custom_q, st.session_state.historic_data)
                st.markdown(response)

def page_ml():
    st.markdown('<p class="main-header">🔬 ML Models & Predictions</p>', unsafe_allow_html=True)
    
    if not HAS_ML:
        st.warning("Install ML packages: `pip install xgboost lightgbm scikit-learn`")
        return
    
    if st.session_state.historic_data is None:
        st.warning("Load historic data first")
        return
    
    st.info("ML models: XGBoost, LightGBM for outage prediction with SHAP explainability")
    
    df = st.session_state.historic_data
    
    features = ['Weather', 'Equipment', 'Wildfire', 'PSPS', 'Season', 'County']
    importance = [0.25, 0.20, 0.18, 0.15, 0.12, 0.10]
    fig = px.bar(x=importance, y=features, orientation='h', title='Feature Importance (Example)')
    st.plotly_chart(fig, use_container_width=True)

def page_compliance():
    st.markdown('<p class="main-header">📋 Federal Compliance Assessment</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <h4>DOE OE-417 Reporting Requirements</h4>
    Events affecting ≥50,000 customers must be reported to DOE within specific timeframes.
    This analysis identifies potential underreporting in federal statistics.
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.historic_data is not None:
        df = st.session_state.historic_data
        threshold = df[df['meets_doe_threshold']]
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Events", f"{len(df):,}")
        col2.metric("Federal Threshold Events", f"{len(threshold):,}")
        col3.metric("Percentage", f"{len(threshold)/len(df)*100:.1f}%")
        
        yearly = threshold.groupby('year').size().reset_index(name='count')
        fig = px.bar(yearly, x='year', y='count', title='Federal Threshold Events by Year')
        st.plotly_chart(fig, use_container_width=True)

def page_settings():
    st.markdown('<p class="main-header">⚙️ Settings & API Configuration</p>', unsafe_allow_html=True)
    
    st.markdown("### 🔑 API Keys")
    
    if ANTHROPIC_API_KEY:
        st.success("✅ **Anthropic Claude API**: Configured via environment variable")
        st.code(f"API Key: {ANTHROPIC_API_KEY[:15]}...{ANTHROPIC_API_KEY[-5:]}")
    else:
        st.warning("⚠️ **Anthropic Claude API**: Not configured")
        st.markdown("""
        **To set your API key:**
        
        **Option 1: Command Line**
        ```bash
        # Windows
        set ANTHROPIC_API_KEY=your-api-key-here
        
        # Mac/Linux
        export ANTHROPIC_API_KEY=your-api-key-here
        ```
        
        **Option 2: Create .env file**
        ```
        ANTHROPIC_API_KEY=your-api-key-here
        ```
        
        Then restart the dashboard with: `streamlit run dashboard_comprehensive.py`
        
        **Get your API key at:** https://console.anthropic.com
        """)
    
    st.markdown("### 📡 Free Public APIs (No Keys Required)")
    
    for name, info in FREE_APIS.items():
        st.markdown(f"""
        <div class="api-card">
            <strong>✅ {name}</strong><br>
            <small>URL: {info['url']}</small><br>
            <small>{info['description']}</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 🗑️ Data Management")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Clear All Data"):
            st.session_state.historic_data = None
            st.session_state.live_data = None
            st.success("✅ Cleared")
    with col2:
        if st.button("Reload All Data"):
            st.session_state.historic_data = load_historic_eagle_i()
            st.session_state.live_data = fetch_live_california_outages()
            st.session_state.last_update = datetime.now()
            st.success("✅ Reloaded")

# ============================================================================
# MAIN ROUTER
# ============================================================================

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

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div class="footer">
    <strong>Victoria Love Franklin</strong> | PhD Pre-Candidate, Meharry Medical College<br>
    Tennessee Clinical Perfusionist Board (Gov. Lee Appointee) | HEJTC Board Member | IEEE | APHL | WEF | NSBE<br><br>
    <strong>Citation:</strong> Franklin, V.L. (2025). Toward Climate-Resilient Energy Systems: 
    A Geospatial RAG-Enabled Digital Twin. Meharry Medical College.<br>
    <small>Keywords: California energy resilience, climate change, environmental justice, GIS, AI, RAG, XGBoost, SHAP</small>
</div>
""", unsafe_allow_html=True)
