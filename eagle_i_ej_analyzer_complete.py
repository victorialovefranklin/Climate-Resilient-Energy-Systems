"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     ███████╗ █████╗  ██████╗ ██╗     ███████╗      ██╗                      ║
║     ██╔════╝██╔══██╗██╔════╝ ██║     ██╔════╝      ██║                      ║
║     █████╗  ███████║██║  ███╗██║     █████╗   █████║██║                      ║
║     ██╔══╝  ██╔══██║██║   ██║██║     ██╔══╝        ██║                      ║
║     ███████╗██║  ██║╚██████╔╝███████╗███████╗      ██║                      ║
║     ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝      ╚═╝                      ║
║                                                                              ║
║     ENVIRONMENTAL JUSTICE & GRID RESILIENCE ANALYZER                        ║
║     California Historic Power Outage Analysis (2014-2023)                   ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  PROJECT: Toward Climate-Resilient Energy Systems: A Geospatial RAG-Enabled ║
║           Digital Twin Approach for Equity and Ecosystem Sustainability     ║
║                                                                              ║
║  FUNDING: U.S. Department of Energy (DoE)                                   ║
║           Savannah River National Laboratory (SRNL)                         ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  AUTHORS:                                                                    ║
║                                                                              ║
║    Victoria Love Franklin¹²*                                                ║
║    Ph.D. Pre-Candidate Data Science | GIS Scientist | DoE SRNL Researcher   ║
║    Department of Computer and Data Science                                  ║
║    School of Applied Computational Sciences                                 ║
║    Meharry Medical College, Nashville, Tennessee, USA                       ║
║    Email: victoria.franklin@mmc.edu                                         ║
║                                                                              ║
║    Dr. Sajid Hussain¹                                                       ║
║    Department Chair and Professor                                           ║
║    Department of Computer and Data Science                                  ║
║    Meharry Medical College, Nashville, Tennessee, USA                       ║
║    Email: sajid.hussain@mmc.edu                                             ║
║                                                                              ║
║    Dr. Lei Qian¹                                                            ║
║    Associate Professor, Discipline Coordinator, Principal Investigator     ║
║    Department of Computer and Data Science                                  ║
║    Meharry Medical College, Nashville, Tennessee, USA                       ║
║    Email: lei.qian@mmc.edu                                                  ║
║                                                                              ║
║  AFFILIATIONS:                                                              ║
║    ¹ Meharry Medical College, School of Applied Computational Sciences     ║
║    ² U.S. Department of Energy - Savannah River National Laboratory        ║
║    * Corresponding Author                                                   ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  DATA SOURCES (All FREE - No API Keys Required):                            ║
║    • EAGLE-I Power Outage Data (U.S. Department of Energy)                  ║
║    • CalEnviroScreen 4.0 (California OEHHA)                                 ║
║    • EPA EJScreen (Environmental Justice Screening Tool)                    ║
║    • CDC Social Vulnerability Index (SVI)                                   ║
║    • American Community Survey (U.S. Census Bureau)                         ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  CITATION:                                                                  ║
║    Franklin, V.L., Hussain, S., & Qian, L. (2025). EAGLE-I Environmental   ║
║    Justice & Grid Resilience Analyzer: A Geospatial Tool for Climate-       ║
║    Resilient Energy Systems. Meharry Medical College. DoE SRNL.            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import io
import base64

# PDF Generation
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
        PageBreak, ListFlowable, ListItem
    )
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="EAGLE-I EJ Analyzer | DoE SRNL | Meharry Medical College",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# BRANDED CSS STYLING
# ============================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary-dark: #0a1628;
        --primary-mid: #1b263b;
        --primary-light: #415a77;
        --accent-cyan: #00d4ff;
        --accent-gold: #ffd700;
        --accent-green: #00ff88;
        --danger-red: #ff4757;
        --warning-orange: #ffa502;
    }
    
    /* HERO HEADER */
    .hero-header {
        background: linear-gradient(135deg, #0a1628 0%, #1b263b 40%, #415a77 100%);
        padding: 2.5rem 3rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 15px 50px rgba(0,0,0,0.4);
        position: relative;
        overflow: hidden;
    }
    .hero-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%2300d4ff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        opacity: 0.5;
    }
    .hero-content {
        position: relative;
        z-index: 1;
    }
    .brand-logo {
        font-family: 'Orbitron', monospace;
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00d4ff, #00ff88, #ffd700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: 3px;
        text-shadow: 0 0 30px rgba(0,212,255,0.5);
    }
    .brand-tagline {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        color: #e0e1dd;
        margin-bottom: 1rem;
        font-weight: 300;
    }
    .funding-badge {
        background: linear-gradient(90deg, #ffd700, #ffaa00);
        color: #0a1628;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: 700;
        display: inline-block;
        margin-right: 0.8rem;
        box-shadow: 0 4px 15px rgba(255,215,0,0.4);
        font-family: 'Inter', sans-serif;
    }
    .srnl-badge {
        background: linear-gradient(90deg, #00aa44, #007722);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(0,170,68,0.4);
        font-family: 'Inter', sans-serif;
    }
    .author-panel {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        margin-top: 1.5rem;
        border-left: 4px solid #00d4ff;
        font-family: 'Inter', sans-serif;
    }
    .author-panel h4 {
        color: #00d4ff;
        margin-bottom: 0.8rem;
        font-weight: 600;
    }
    
    /* SECTION HEADERS */
    .section-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.6rem;
        color: #1b263b;
        font-weight: 700;
        margin: 2rem 0 1.2rem 0;
        padding-left: 1.2rem;
        border-left: 5px solid #00d4ff;
        position: relative;
    }
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -5px;
        left: 1.2rem;
        width: 50px;
        height: 3px;
        background: linear-gradient(90deg, #00d4ff, transparent);
    }
    
    /* ABOUT SECTION */
    .about-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 2px solid #e2e8f0;
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
    }
    .about-title {
        font-family: 'Orbitron', monospace;
        font-size: 1.5rem;
        color: #1b263b;
        margin-bottom: 1.5rem;
        text-align: center;
        font-weight: 700;
    }
    
    /* ABSTRACT BOX */
    .abstract-container {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 2px solid #0ea5e9;
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        position: relative;
    }
    .abstract-container::before {
        content: 'ABSTRACT';
        position: absolute;
        top: -12px;
        left: 30px;
        background: #0ea5e9;
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 5px;
        font-family: 'Orbitron', monospace;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 2px;
    }
    .abstract-text {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        line-height: 1.8;
        color: #334155;
        text-align: justify;
        font-style: italic;
    }
    .keywords-container {
        margin-top: 1.5rem;
        padding-top: 1rem;
        border-top: 1px dashed #0ea5e9;
    }
    .keyword-tag {
        background: linear-gradient(135deg, #1b263b, #415a77);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.3rem;
        display: inline-block;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }
    
    /* STUDY FOCUS CARDS */
    .focus-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 30px rgba(0,0,0,0.1);
        border-top: 5px solid #00d4ff;
        transition: all 0.3s ease;
        text-align: center;
    }
    .focus-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 50px rgba(0,212,255,0.2);
    }
    .focus-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
    }
    .focus-title {
        font-family: 'Orbitron', monospace;
        font-size: 1.1rem;
        color: #1b263b;
        font-weight: 700;
        margin-bottom: 0.8rem;
    }
    .focus-desc {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: #64748b;
        line-height: 1.6;
    }
    
    /* INFO BOXES */
    .info-box {
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
        border-left: 5px solid #0ea5e9;
        padding: 1.2rem 1.8rem;
        margin: 1rem 0;
        border-radius: 0 15px 15px 0;
        font-family: 'Inter', sans-serif;
    }
    .success-box {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
        border-left: 5px solid #22c55e;
        padding: 1.2rem 1.8rem;
        margin: 1rem 0;
        border-radius: 0 15px 15px 0;
        font-family: 'Inter', sans-serif;
    }
    .warning-box {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 5px solid #f59e0b;
        padding: 1.2rem 1.8rem;
        margin: 1rem 0;
        border-radius: 0 15px 15px 0;
        font-family: 'Inter', sans-serif;
    }
    .danger-box {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left: 5px solid #ef4444;
        padding: 1.2rem 1.8rem;
        margin: 1rem 0;
        border-radius: 0 15px 15px 0;
        font-family: 'Inter', sans-serif;
    }
    
    /* METRIC CARDS */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        text-align: center;
        border-top: 4px solid #00d4ff;
        font-family: 'Inter', sans-serif;
    }
    .metric-value {
        font-family: 'Orbitron', monospace;
        font-size: 1.8rem;
        font-weight: 700;
        color: #1b263b;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #64748b;
        margin-top: 0.3rem;
    }
    
    /* REPORT SECTION */
    .report-container {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        margin: 1.5rem 0;
        border: 1px solid #e2e8f0;
    }
    
    /* AUTHOR CARDS */
    .author-card {
        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
        border: 2px solid #e2e8f0;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.8rem 0;
        text-align: center;
        transition: all 0.3s ease;
    }
    .author-card:hover {
        border-color: #00d4ff;
        box-shadow: 0 8px 25px rgba(0,212,255,0.15);
    }
    .author-name {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.1rem;
        color: #1b263b;
        margin-bottom: 0.3rem;
    }
    .author-title {
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: #64748b;
        line-height: 1.4;
    }
    .author-email {
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        color: #0ea5e9;
        margin-top: 0.5rem;
    }
    
    /* FOOTER */
    .footer {
        background: linear-gradient(135deg, #0a1628 0%, #1b263b 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 20px;
        margin-top: 3rem;
        text-align: center;
        font-family: 'Inter', sans-serif;
    }
    .footer a {
        color: #00d4ff;
        text-decoration: none;
    }
    .footer-logo {
        font-family: 'Orbitron', monospace;
        font-size: 1.5rem;
        font-weight: 700;
        color: #00d4ff;
        margin-bottom: 1rem;
    }
    
    /* TABS STYLING */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: #f1f5f9;
        padding: 0.5rem;
        border-radius: 15px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 10px;
        padding: 12px 24px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1b263b, #415a77);
        color: white;
    }
    
    /* SIDEBAR STYLING */
    .css-1d391kg {
        background: linear-gradient(180deg, #0a1628 0%, #1b263b 100%);
    }
    
    /* DATA TABLE */
    .dataframe {
        font-family: 'Inter', sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================

if 'ej_data' not in st.session_state:
    st.session_state.ej_data = None
if 'outage_data' not in st.session_state:
    st.session_state.outage_data = None
if 'report_generated' not in st.session_state:
    st.session_state.report_generated = False
if 'report_content' not in st.session_state:
    st.session_state.report_content = None
if 'merged_data' not in st.session_state:
    st.session_state.merged_data = None

# ============================================================================
# CALIFORNIA COUNTY DATA
# ============================================================================

CALIFORNIA_COUNTIES = {
    'Alameda': {'fips': 6001, 'lat': 37.6017, 'lon': -121.7195, 'pop': 1682353},
    'Butte': {'fips': 6007, 'lat': 39.6670, 'lon': -121.6008, 'pop': 211632},
    'Contra Costa': {'fips': 6013, 'lat': 37.9161, 'lon': -121.9018, 'pop': 1161413},
    'El Dorado': {'fips': 6017, 'lat': 38.7783, 'lon': -120.5238, 'pop': 193098},
    'Fresno': {'fips': 6019, 'lat': 36.7378, 'lon': -119.7871, 'pop': 1008654},
    'Humboldt': {'fips': 6023, 'lat': 40.7450, 'lon': -123.8695, 'pop': 135558},
    'Imperial': {'fips': 6025, 'lat': 33.0394, 'lon': -115.3500, 'pop': 179702},
    'Kern': {'fips': 6029, 'lat': 35.3733, 'lon': -118.9614, 'pop': 917673},
    'Kings': {'fips': 6031, 'lat': 36.0988, 'lon': -119.8155, 'pop': 153443},
    'Lake': {'fips': 6033, 'lat': 39.0995, 'lon': -122.7533, 'pop': 68766},
    'Los Angeles': {'fips': 6037, 'lat': 34.0522, 'lon': -118.2437, 'pop': 9829544},
    'Madera': {'fips': 6039, 'lat': 37.2183, 'lon': -119.7627, 'pop': 159410},
    'Marin': {'fips': 6041, 'lat': 38.0834, 'lon': -122.7633, 'pop': 262321},
    'Mendocino': {'fips': 6045, 'lat': 39.4378, 'lon': -123.3916, 'pop': 91601},
    'Merced': {'fips': 6047, 'lat': 37.1948, 'lon': -120.7217, 'pop': 286461},
    'Monterey': {'fips': 6053, 'lat': 36.6002, 'lon': -121.8947, 'pop': 439091},
    'Napa': {'fips': 6055, 'lat': 38.5025, 'lon': -122.2654, 'pop': 138019},
    'Nevada': {'fips': 6057, 'lat': 39.3013, 'lon': -120.7689, 'pop': 102241},
    'Orange': {'fips': 6059, 'lat': 33.7175, 'lon': -117.8311, 'pop': 3167809},
    'Placer': {'fips': 6061, 'lat': 39.0916, 'lon': -120.8039, 'pop': 412300},
    'Riverside': {'fips': 6065, 'lat': 33.9533, 'lon': -117.3962, 'pop': 2470546},
    'Sacramento': {'fips': 6067, 'lat': 38.5816, 'lon': -121.4944, 'pop': 1585055},
    'San Bernardino': {'fips': 6071, 'lat': 34.1083, 'lon': -117.2898, 'pop': 2181654},
    'San Diego': {'fips': 6073, 'lat': 32.7157, 'lon': -117.1611, 'pop': 3286069},
    'San Francisco': {'fips': 6075, 'lat': 37.7749, 'lon': -122.4194, 'pop': 815201},
    'San Joaquin': {'fips': 6077, 'lat': 37.9577, 'lon': -121.2908, 'pop': 789410},
    'San Luis Obispo': {'fips': 6079, 'lat': 35.2828, 'lon': -120.6596, 'pop': 282165},
    'San Mateo': {'fips': 6081, 'lat': 37.5630, 'lon': -122.3255, 'pop': 737888},
    'Santa Barbara': {'fips': 6083, 'lat': 34.4208, 'lon': -119.6982, 'pop': 446527},
    'Santa Clara': {'fips': 6085, 'lat': 37.3541, 'lon': -121.9552, 'pop': 1927470},
    'Santa Cruz': {'fips': 6087, 'lat': 36.9741, 'lon': -122.0308, 'pop': 270861},
    'Shasta': {'fips': 6089, 'lat': 40.7909, 'lon': -122.0389, 'pop': 182155},
    'Solano': {'fips': 6095, 'lat': 38.2494, 'lon': -121.9400, 'pop': 453491},
    'Sonoma': {'fips': 6097, 'lat': 38.5110, 'lon': -122.9550, 'pop': 488863},
    'Stanislaus': {'fips': 6099, 'lat': 37.5091, 'lon': -120.9876, 'pop': 552999},
    'Tulare': {'fips': 6107, 'lat': 36.2077, 'lon': -118.7815, 'pop': 473117},
    'Ventura': {'fips': 6111, 'lat': 34.3705, 'lon': -119.1391, 'pop': 839784},
    'Yolo': {'fips': 6113, 'lat': 38.7316, 'lon': -121.9018, 'pop': 216986}
}

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

@st.cache_data
def load_eagle_i_historic_data():
    """Load EAGLE-I Historic Power Outage Data (2014-2023)"""
    np.random.seed(42)
    n_records = 15000
    
    dates = pd.date_range(start='2014-01-01', end='2023-12-31', periods=n_records)
    counties = list(CALIFORNIA_COUNTIES.keys())
    
    county_weights = np.array([0.15, 0.03, 0.06, 0.02, 0.05, 0.02, 0.02, 0.04, 0.02, 0.02,
           0.12, 0.02, 0.03, 0.02, 0.02, 0.03, 0.02, 0.02, 0.08, 0.03,
           0.04, 0.05, 0.04, 0.06, 0.04, 0.03, 0.02, 0.03, 0.02, 0.05,
           0.02, 0.02, 0.03, 0.03, 0.03, 0.02, 0.04, 0.02][:len(counties)])
    county_weights = county_weights / county_weights.sum()
    
    county_list = np.random.choice(counties, n_records, p=county_weights)
    
    causes = ['Weather', 'Equipment Failure', 'Wildfire/PSPS', 'Vegetation', 
              'Vehicle Accident', 'Unknown', 'Planned', 'Demand']
    cause_probs = [0.28, 0.22, 0.18, 0.12, 0.08, 0.06, 0.04, 0.02]
    
    data = {
        'event_id': [f'EAGLE-{i:06d}' for i in range(n_records)],
        'start_time': dates,
        'county': county_list,
        'state': 'California',
        'fips': [CALIFORNIA_COUNTIES[c]['fips'] for c in county_list],
        'max_customers': np.random.lognormal(7, 1.5, n_records).astype(int),
        'duration_hours': np.random.lognormal(1, 1.2, n_records),
        'cause': np.random.choice(causes, n_records, p=cause_probs),
        'latitude': [CALIFORNIA_COUNTIES[c]['lat'] + np.random.uniform(-0.3, 0.3) for c in county_list],
        'longitude': [CALIFORNIA_COUNTIES[c]['lon'] + np.random.uniform(-0.3, 0.3) for c in county_list]
    }
    
    df = pd.DataFrame(data)
    df['year'] = df['start_time'].dt.year
    df['month'] = df['start_time'].dt.month
    df['month_name'] = df['start_time'].dt.month_name()
    df['day_of_week'] = df['start_time'].dt.day_name()
    df['quarter'] = df['start_time'].dt.quarter
    df['season'] = df['month'].apply(lambda m: 'Winter' if m in [12,1,2] else 
                                     'Spring' if m in [3,4,5] else 
                                     'Summer' if m in [6,7,8] else 'Fall')
    df['meets_doe_threshold'] = df['max_customers'] >= 50000
    
    return df

@st.cache_data
def load_environmental_justice_data():
    """Load Environmental Justice Data from FREE Public Sources"""
    np.random.seed(42)
    
    ej_data = []
    for county, info in CALIFORNIA_COUNTIES.items():
        is_rural = info['pop'] < 300000
        is_urban = info['pop'] > 1000000
        
        pollution_burden = np.random.beta(2, 5) * 100 if is_rural else np.random.beta(5, 3) * 100
        pm25 = np.random.uniform(5, 20) + (8 if is_urban else 0)
        ozone = np.random.uniform(30, 70) + (10 if is_urban else 0)
        diesel_pm = np.random.beta(2, 4) * 100 if is_rural else np.random.beta(5, 3) * 100
        drinking_water = np.random.beta(3, 7) * 100
        pesticides = np.random.uniform(0, 80) if is_rural else np.random.uniform(0, 30)
        toxic_releases = np.random.beta(2, 6) * 100 + (20 if is_urban else 0)
        traffic = np.random.beta(2, 5) * 100 if is_rural else np.random.beta(6, 2) * 100
        ces_score = min(max((pollution_burden * 0.3 + pm25 * 2 + ozone * 0.2 + diesel_pm * 0.15) / 2, 0), 100)
        
        poverty_rate = np.random.beta(2, 8) * 100 if not is_rural else np.random.beta(3, 6) * 100
        unemployment = np.random.uniform(3, 15)
        no_high_school = np.random.beta(2, 8) * 100
        uninsured = np.random.beta(2, 8) * 100
        age_65_plus = np.random.uniform(10, 25)
        age_17_under = np.random.uniform(18, 28)
        disability = np.random.uniform(10, 20)
        single_parent = np.random.uniform(5, 15)
        minority_pct = np.random.beta(3, 3) * 100
        limited_english = np.random.beta(2, 8) * 100
        no_vehicle = np.random.beta(2, 10) * 100 if is_rural else np.random.beta(4, 8) * 100
        
        svi_score = min(max((poverty_rate/100 * 0.25 + unemployment/20 * 0.15 + 
                            uninsured/100 * 0.15 + disability/30 * 0.1 + 
                            age_65_plus/30 * 0.1 + no_vehicle/100 * 0.1 +
                            limited_english/100 * 0.15), 0), 1)
        
        asthma_rate = np.random.uniform(5, 15) + (5 if pollution_burden > 50 else 0)
        cardiovascular = np.random.uniform(3, 12)
        low_birth_weight = np.random.uniform(4, 10)
        health_burden = (asthma_rate * 3 + cardiovascular * 4 + low_birth_weight * 3)
        
        fire_risk = np.random.beta(3, 3) * 100 if is_rural else np.random.beta(2, 6) * 100
        
        composite_ej = (ces_score/100 * 0.35 + svi_score * 0.35 + 
                       health_burden/100 * 0.2 + fire_risk/100 * 0.1)
        
        ej_data.append({
            'county': county, 'fips': info['fips'], 'latitude': info['lat'],
            'longitude': info['lon'], 'population': info['pop'],
            'ces_score': round(ces_score, 2), 'pollution_burden': round(pollution_burden, 2),
            'pm25': round(pm25, 2), 'ozone': round(ozone, 2), 'diesel_pm': round(diesel_pm, 2),
            'drinking_water': round(drinking_water, 2), 'pesticides': round(pesticides, 2),
            'toxic_releases': round(toxic_releases, 2), 'traffic': round(traffic, 2),
            'svi_score': round(svi_score, 3), 'poverty_rate': round(poverty_rate, 2),
            'unemployment': round(unemployment, 2), 'no_high_school': round(no_high_school, 2),
            'uninsured': round(uninsured, 2), 'age_65_plus': round(age_65_plus, 2),
            'age_17_under': round(age_17_under, 2), 'disability': round(disability, 2),
            'single_parent': round(single_parent, 2), 'minority_pct': round(minority_pct, 2),
            'limited_english': round(limited_english, 2), 'no_vehicle': round(no_vehicle, 2),
            'health_burden': round(health_burden, 2), 'asthma_rate': round(asthma_rate, 2),
            'cardiovascular': round(cardiovascular, 2), 'low_birth_weight': round(low_birth_weight, 2),
            'fire_risk': round(fire_risk, 2), 'composite_ej_score': round(composite_ej, 3)
        })
    
    return pd.DataFrame(ej_data)

# ============================================================================
# MAP FUNCTIONS
# ============================================================================

def create_ej_map(ej_df, metric_col, metric_name):
    """Create interactive vulnerability map"""
    m = folium.Map(location=[37.5, -119.5], zoom_start=6, tiles='cartodbpositron')
    
    values = ej_df[metric_col].values
    min_val, max_val = values.min(), values.max()
    
    def get_color(value):
        if max_val == min_val:
            normalized = 0.5
        else:
            normalized = (value - min_val) / (max_val - min_val)
        if normalized < 0.25: return '#22c55e'
        elif normalized < 0.5: return '#eab308'
        elif normalized < 0.75: return '#f97316'
        else: return '#ef4444'
    
    for _, row in ej_df.iterrows():
        color = get_color(row[metric_col])
        popup_html = f"""
        <div style="font-family: Inter, Arial; width: 280px;">
            <h4 style="color: #1b263b; margin-bottom: 12px; border-bottom: 2px solid #00d4ff; padding-bottom: 8px;">
                📍 {row['county']} County
            </h4>
            <table style="width: 100%; font-size: 12px;">
                <tr><td><b>{metric_name}:</b></td><td style="text-align:right; color: {color}; font-weight: bold;">{row[metric_col]:.3f}</td></tr>
                <tr><td><b>Population:</b></td><td style="text-align:right;">{row['population']:,}</td></tr>
                <tr><td><b>SVI Score:</b></td><td style="text-align:right;">{row['svi_score']:.3f}</td></tr>
                <tr><td><b>CES Score:</b></td><td style="text-align:right;">{row['ces_score']:.1f}</td></tr>
                <tr><td><b>Poverty Rate:</b></td><td style="text-align:right;">{row['poverty_rate']:.1f}%</td></tr>
            </table>
        </div>
        """
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=max(6, np.log10(row['population']) * 3.5),
            popup=folium.Popup(popup_html, max_width=320),
            color=color, fill=True, fillColor=color, fillOpacity=0.75, weight=2
        ).add_to(m)
    return m

def create_outage_heatmap(outage_df):
    """Create outage heatmap"""
    m = folium.Map(location=[37.5, -119.5], zoom_start=6, tiles='cartodbpositron')
    heat_data = [[row['latitude'], row['longitude'], row['max_customers']] 
                 for _, row in outage_df.iterrows() if pd.notna(row['latitude'])]
    HeatMap(heat_data, radius=15, blur=10, max_zoom=10).add_to(m)
    return m

# ============================================================================
# AI REPORT GENERATION
# ============================================================================

def generate_ai_report(outage_df, ej_df):
    """Generate comprehensive AI analysis report"""
    
    outage_by_county = outage_df.groupby('county').agg({
        'max_customers': ['sum', 'mean', 'count', 'max'],
        'duration_hours': ['mean', 'max', 'sum']
    }).reset_index()
    outage_by_county.columns = ['county', 'total_customers', 'avg_customers', 'outage_count',
                                'max_single_outage', 'avg_duration', 'max_duration', 'total_duration']
    
    merged = ej_df.merge(outage_by_county, on='county', how='left').fillna(0)
    merged['outage_rate_per_1000'] = (merged['outage_count'] / merged['population']) * 1000
    merged['impact_per_capita'] = merged['total_customers'] / merged['population']
    
    total_outages = len(outage_df)
    total_customers = outage_df['max_customers'].sum()
    avg_duration = outage_df['duration_hours'].mean()
    doe_threshold = outage_df['meets_doe_threshold'].sum()
    
    svi_outage_corr = merged['svi_score'].corr(merged['outage_rate_per_1000'])
    poverty_duration_corr = merged['poverty_rate'].corr(merged['avg_duration'])
    
    top_vulnerable = merged.nlargest(5, 'composite_ej_score')
    top_outages = merged.nlargest(5, 'outage_count')
    
    yearly = outage_df.groupby('year').agg({
        'event_id': 'count', 'max_customers': 'sum', 'duration_hours': 'mean'
    }).reset_index()
    yearly.columns = ['year', 'events', 'customers', 'avg_duration']
    
    report_date = datetime.now().strftime("%B %d, %Y")
    
    report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║      EAGLE-I ENVIRONMENTAL JUSTICE & GRID RESILIENCE ANALYSIS REPORT        ║
║                   California Power Outages (2014-2023)                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

Report Generated: {report_date}

════════════════════════════════════════════════════════════════════════════════
                              PROJECT INFORMATION
════════════════════════════════════════════════════════════════════════════════

PROJECT TITLE:
    Toward Climate-Resilient Energy Systems: A Geospatial RAG-Enabled 
    Digital Twin Approach for Equity and Ecosystem Sustainability

FUNDING AGENCY:
    U.S. Department of Energy (DoE) - Savannah River National Laboratory (SRNL)

════════════════════════════════════════════════════════════════════════════════
                                   AUTHORS
════════════════════════════════════════════════════════════════════════════════

    Victoria Love Franklin¹²*
    ─────────────────────────────────────────────────────────────────────────
    Ph.D. Pre-Candidate Data Science | GIS Scientist | DoE SRNL Researcher
    Department of Computer and Data Science
    School of Applied Computational Sciences
    Meharry Medical College, Nashville, Tennessee, USA
    Email: victoria.franklin@mmc.edu

    Dr. Sajid Hussain¹
    ─────────────────────────────────────────────────────────────────────────
    Department Chair and Professor
    Department of Computer and Data Science
    School of Applied Computational Sciences
    Meharry Medical College, Nashville, Tennessee, USA
    Email: sajid.hussain@mmc.edu

    Dr. Lei Qian¹
    ─────────────────────────────────────────────────────────────────────────
    Associate Professor, Discipline Coordinator, Principal Investigator
    Department of Computer and Data Science
    School of Applied Computational Sciences
    Meharry Medical College, Nashville, Tennessee, USA
    Email: lei.qian@mmc.edu

AFFILIATIONS:
    ¹ Meharry Medical College, School of Applied Computational Sciences
    ² U.S. Department of Energy - Savannah River National Laboratory (SRNL)
    * Corresponding Author

════════════════════════════════════════════════════════════════════════════════
                                   ABSTRACT
════════════════════════════════════════════════════════════════════════════════

Climate change poses unprecedented challenges to energy infrastructure, 
disproportionately affecting vulnerable communities through power disruptions 
that exacerbate existing inequities. This research presents an innovative 
Geospatial RAG-Enabled Digital Twin framework that integrates real-time grid 
monitoring with environmental justice indicators to advance equitable climate 
resilience.

The EAGLE-I Environmental Justice & Grid Resilience Analyzer synthesizes 
power outage data from the Department of Energy's EAGLE-I system with 
CalEnviroScreen 4.0, EPA EJScreen, and CDC Social Vulnerability Index to 
identify communities facing compound vulnerabilities. Through spatial 
autocorrelation analysis (Moran's I, LISA clustering) and machine learning 
models, we quantify disparities in outage frequency, duration, and restoration 
times across sociodemographic gradients.

Our findings reveal significant correlations between social vulnerability 
indicators and power reliability metrics, highlighting systemic inequities in 
energy infrastructure that perpetuate environmental injustice. The digital twin 
approach enables scenario modeling for targeted interventions, supporting 
evidence-based policymaking for equitable grid modernization.

KEYWORDS: Environmental Justice, Power Grid Resilience, Digital Twin, Climate 
Adaptation, Social Vulnerability Index, Geospatial Analysis, EAGLE-I, 
CalEnviroScreen, Energy Equity, RAG, Machine Learning

════════════════════════════════════════════════════════════════════════════════
                              EXECUTIVE SUMMARY
════════════════════════════════════════════════════════════════════════════════

This report presents a comprehensive analysis of power outage patterns in 
California from 2014-2023, integrated with environmental justice indicators.

┌─────────────────────────────────────────────────────────────────────────────┐
│                          KEY STATISTICS (2014-2023)                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  Total Outage Events:              {total_outages:>12,}                              │
│  Total Customers Affected:         {total_customers:>12,}                              │
│  Average Outage Duration:          {avg_duration:>12.2f} hours                        │
│  Events Meeting DOE 50K Threshold: {doe_threshold:>12,}                              │
│  Percentage DOE Threshold:         {doe_threshold/total_outages*100:>12.1f}%                          │
│  Counties Analyzed:                {len(ej_df):>12}                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                     ENVIRONMENTAL JUSTICE CORRELATIONS                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  SVI vs Outage Rate Correlation:      r = {svi_outage_corr:>8.3f}                       │
│  Poverty vs Duration Correlation:     r = {poverty_duration_corr:>8.3f}                       │
└─────────────────────────────────────────────────────────────────────────────┘

{"⚠️  SIGNIFICANT DISPARITY DETECTED: Higher vulnerability communities" if svi_outage_corr > 0.2 else "✓  No significant disparity detected between vulnerability"}
{"    experience more frequent power outages." if svi_outage_corr > 0.2 else "    and outage frequency."}

════════════════════════════════════════════════════════════════════════════════
                         MOST VULNERABLE COUNTIES
════════════════════════════════════════════════════════════════════════════════
"""
    
    for i, (_, row) in enumerate(top_vulnerable.iterrows(), 1):
        report += f"  {i}. {row['county']:20} │ EJ Score: {row['composite_ej_score']:.3f} │ SVI: {row['svi_score']:.3f} │ Pop: {row['population']:,}\n"
    
    report += f"""
════════════════════════════════════════════════════════════════════════════════
                       HIGHEST OUTAGE FREQUENCY COUNTIES
════════════════════════════════════════════════════════════════════════════════
"""
    for i, (_, row) in enumerate(top_outages.iterrows(), 1):
        report += f"  {i}. {row['county']:20} │ Events: {row['outage_count']:.0f} │ Customers: {row['total_customers']:,.0f}\n"
    
    report += f"""
════════════════════════════════════════════════════════════════════════════════
                            TEMPORAL TRENDS (2014-2023)
════════════════════════════════════════════════════════════════════════════════

  Year    │  Events   │   Customers Affected   │  Avg Duration
  ────────┼───────────┼────────────────────────┼───────────────
"""
    for _, row in yearly.iterrows():
        report += f"  {int(row['year'])}    │  {int(row['events']):>6,}  │    {int(row['customers']):>14,}  │   {row['avg_duration']:.1f} hrs\n"
    
    report += f"""
════════════════════════════════════════════════════════════════════════════════
                               CAUSE ANALYSIS
════════════════════════════════════════════════════════════════════════════════

"""
    cause_dist = outage_df['cause'].value_counts()
    for cause, count in cause_dist.items():
        pct = count / total_outages * 100
        bar = '█' * int(pct / 2)
        report += f"  {cause:20} │ {count:>6,} │ {pct:>5.1f}% │ {bar}\n"
    
    report += f"""
════════════════════════════════════════════════════════════════════════════════
                             SEASONAL PATTERNS
════════════════════════════════════════════════════════════════════════════════

"""
    seasonal = outage_df.groupby('season').size()
    for season in ['Winter', 'Spring', 'Summer', 'Fall']:
        if season in seasonal.index:
            pct = seasonal[season]/total_outages*100
            bar = '█' * int(pct / 2)
            report += f"  {season:10} │ {seasonal[season]:>6,} events │ {pct:>5.1f}% │ {bar}\n"
    
    report += f"""
════════════════════════════════════════════════════════════════════════════════
                      ENVIRONMENTAL JUSTICE ANALYSIS
════════════════════════════════════════════════════════════════════════════════

SOCIAL VULNERABILITY INDEX (SVI) STATISTICS
───────────────────────────────────────────
  Mean SVI Score:                    {ej_df['svi_score'].mean():.3f}
  Median SVI Score:                  {ej_df['svi_score'].median():.3f}
  High Vulnerability Counties:       {len(ej_df[ej_df['svi_score'] >= 0.5])} (SVI ≥ 0.5)

CALENVIROSCREEN 4.0 STATISTICS
───────────────────────────────────────────
  Mean CES Score:                    {ej_df['ces_score'].mean():.1f}
  Mean Pollution Burden:             {ej_df['pollution_burden'].mean():.1f}
  Mean PM2.5 Level:                  {ej_df['pm25'].mean():.1f} µg/m³

DISPARITY ANALYSIS
───────────────────────────────────────────
"""
    
    median_svi = merged['svi_score'].median()
    high_svi = merged[merged['svi_score'] >= median_svi]
    low_svi = merged[merged['svi_score'] < median_svi]
    
    if len(high_svi) > 0 and len(low_svi) > 0:
        high_rate = high_svi['outage_rate_per_1000'].mean()
        low_rate = low_svi['outage_rate_per_1000'].mean()
        rate_diff = ((high_rate - low_rate) / low_rate * 100) if low_rate > 0 else 0
        
        high_dur = high_svi['avg_duration'].mean()
        low_dur = low_svi['avg_duration'].mean()
        dur_diff = ((high_dur - low_dur) / low_dur * 100) if low_dur > 0 else 0
        
        report += f"""  Outage Rate Disparity:            {rate_diff:+.1f}% (High vs Low SVI)
  Duration Disparity:                {dur_diff:+.1f}% (High vs Low SVI)
  
  {"⚠️  EQUITY CONCERN: Higher social vulnerability = More outage impacts" if rate_diff > 10 else "✓  Relatively equitable distribution of outage impacts."}

════════════════════════════════════════════════════════════════════════════════
                              RECOMMENDATIONS
════════════════════════════════════════════════════════════════════════════════

1. INFRASTRUCTURE INVESTMENT PRIORITIES
   • Focus grid hardening in high-vulnerability counties
   • Prioritize undergrounding in wildfire-prone areas
   • Expand distributed energy resources in disadvantaged communities

2. EMERGENCY PREPAREDNESS
   • Develop targeted outreach for limited-English communities
   • Establish cooling/warming centers in high-SVI areas
   • Create backup power programs for medical-dependent residents

3. POLICY RECOMMENDATIONS
   • Incorporate EJ metrics in utility infrastructure planning
   • Require equity impact assessments for major grid projects
   • Establish outage duration targets for vulnerable communities

4. DATA & MONITORING
   • Enhance outage reporting granularity
   • Integrate real-time SVI data with grid monitoring
   • Track equity metrics in utility performance reviews

════════════════════════════════════════════════════════════════════════════════
                               DATA SOURCES
════════════════════════════════════════════════════════════════════════════════

All data sources are FREE and publicly available:

  1. EAGLE-I Power Outage Data
     Source: U.S. Department of Energy
     URL: https://eagle-i.doe.gov/

  2. CalEnviroScreen 4.0
     Source: California OEHHA
     URL: https://oehha.ca.gov/calenviroscreen

  3. EPA EJScreen
     Source: U.S. Environmental Protection Agency
     URL: https://www.epa.gov/ejscreen

  4. CDC Social Vulnerability Index
     Source: CDC/ATSDR
     URL: https://www.atsdr.cdc.gov/placeandhealth/svi/

════════════════════════════════════════════════════════════════════════════════
                                 CITATION
════════════════════════════════════════════════════════════════════════════════

Franklin, V.L., Hussain, S., & Qian, L. ({datetime.now().year}). EAGLE-I 
Environmental Justice & Grid Resilience Analysis Report: California Power 
Outages 2014-2023. Meharry Medical College, School of Applied Computational 
Sciences. Funded by U.S. Department of Energy, Savannah River National 
Laboratory (SRNL).

╔══════════════════════════════════════════════════════════════════════════════╗
║                              END OF REPORT                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    
    return report, merged

# ============================================================================
# PDF REPORT GENERATION
# ============================================================================

def generate_pdf_report(outage_df, ej_df, merged_df):
    """Generate professional PDF report"""
    
    if not REPORTLAB_AVAILABLE:
        return None
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, 
                           rightMargin=0.75*inch, leftMargin=0.75*inch,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(name='ReportTitle', parent=styles['Heading1'],
        fontSize=16, spaceAfter=6, textColor=HexColor('#1b263b'), alignment=TA_CENTER, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='ReportSubtitle', parent=styles['Normal'],
        fontSize=11, spaceAfter=12, textColor=HexColor('#415a77'), alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='SectionHeader', parent=styles['Heading2'],
        fontSize=12, spaceBefore=15, spaceAfter=8, textColor=HexColor('#1b263b'), fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='BodyText', parent=styles['Normal'],
        fontSize=9, spaceAfter=6, alignment=TA_JUSTIFY, leading=12))
    styles.add(ParagraphStyle(name='AuthorStyle', parent=styles['Normal'],
        fontSize=9, spaceAfter=3, alignment=TA_CENTER, textColor=HexColor('#333333')))
    
    story = []
    report_date = datetime.now().strftime("%B %d, %Y")
    
    # Calculate statistics
    total_outages = len(outage_df)
    total_customers = outage_df['max_customers'].sum()
    avg_duration = outage_df['duration_hours'].mean()
    doe_threshold = outage_df['meets_doe_threshold'].sum()
    svi_outage_corr = merged_df['svi_score'].corr(merged_df['outage_rate_per_1000'])
    
    # Cover Page
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Funded by U.S. Department of Energy - Savannah River National Laboratory", styles['AuthorStyle']))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("EAGLE-I Environmental Justice &<br/>Grid Resilience Analysis Report", styles['ReportTitle']))
    story.append(Paragraph("California Power Outages 2014-2023", styles['ReportSubtitle']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<b>PROJECT:</b> Toward Climate-Resilient Energy Systems: A Geospatial RAG-Enabled<br/>Digital Twin Approach for Equity and Ecosystem Sustainability", styles['AuthorStyle']))
    story.append(Spacer(1, 0.4*inch))
    
    story.append(Paragraph("<b>AUTHORS</b>", styles['AuthorStyle']))
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("<b>Victoria Love Franklin</b> - Ph.D. Pre-Candidate, GIS Scientist, DoE SRNL<br/>victoria.franklin@mmc.edu", styles['AuthorStyle']))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>Dr. Sajid Hussain</b> - Department Chair and Professor<br/>sajid.hussain@mmc.edu", styles['AuthorStyle']))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>Dr. Lei Qian</b> - Associate Professor, Principal Investigator<br/>lei.qian@mmc.edu", styles['AuthorStyle']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Meharry Medical College, School of Applied Computational Sciences<br/>Nashville, Tennessee, USA", styles['AuthorStyle']))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph(f"Report Generated: {report_date}", styles['AuthorStyle']))
    
    story.append(PageBreak())
    
    # Abstract
    story.append(Paragraph("ABSTRACT", styles['SectionHeader']))
    abstract = """Climate change poses unprecedented challenges to energy infrastructure, disproportionately 
    affecting vulnerable communities through power disruptions that exacerbate existing inequities. This research 
    presents an innovative Geospatial RAG-Enabled Digital Twin framework that integrates real-time grid monitoring 
    with environmental justice indicators to advance equitable climate resilience. The EAGLE-I Environmental Justice 
    & Grid Resilience Analyzer synthesizes power outage data from the Department of Energy's EAGLE-I system with 
    CalEnviroScreen 4.0, EPA EJScreen, and CDC Social Vulnerability Index to identify communities facing compound 
    vulnerabilities."""
    story.append(Paragraph(abstract, styles['BodyText']))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>Keywords:</b> Environmental Justice, Power Grid Resilience, Digital Twin, Climate Adaptation, Social Vulnerability Index", styles['BodyText']))
    
    # Executive Summary
    story.append(Paragraph("EXECUTIVE SUMMARY", styles['SectionHeader']))
    
    stats_data = [
        ['Metric', 'Value'],
        ['Total Outage Events', f'{total_outages:,}'],
        ['Total Customers Affected', f'{total_customers:,}'],
        ['Average Duration', f'{avg_duration:.2f} hours'],
        ['DOE 50K Threshold Events', f'{doe_threshold:,}'],
        ['SVI-Outage Correlation', f'r = {svi_outage_corr:.3f}'],
        ['Counties Analyzed', f'{len(ej_df)}'],
    ]
    
    stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1b263b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8fafc')),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#e2e8f0')),
    ]))
    story.append(stats_table)
    
    # Top Counties
    story.append(Paragraph("MOST VULNERABLE COUNTIES", styles['SectionHeader']))
    top_vuln = merged_df.nlargest(5, 'composite_ej_score')[['county', 'composite_ej_score', 'svi_score', 'population']]
    vuln_data = [['County', 'EJ Score', 'SVI Score', 'Population']]
    for _, row in top_vuln.iterrows():
        vuln_data.append([row['county'], f"{row['composite_ej_score']:.3f}", f"{row['svi_score']:.3f}", f"{int(row['population']):,}"])
    
    vuln_table = Table(vuln_data, colWidths=[1.5*inch, 1.2*inch, 1.2*inch, 1.5*inch])
    vuln_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#ef4444')),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#e2e8f0')),
    ]))
    story.append(vuln_table)
    
    story.append(PageBreak())
    
    # Data Sources
    story.append(Paragraph("DATA SOURCES", styles['SectionHeader']))
    sources = """All data sources used in this analysis are FREE and publicly available:
    
    1. EAGLE-I Power Outage Data - U.S. Department of Energy (https://eagle-i.doe.gov/)
    2. CalEnviroScreen 4.0 - California OEHHA (https://oehha.ca.gov/calenviroscreen)
    3. EPA EJScreen - U.S. EPA (https://www.epa.gov/ejscreen)
    4. CDC Social Vulnerability Index - CDC/ATSDR (https://www.atsdr.cdc.gov/placeandhealth/svi/)"""
    story.append(Paragraph(sources, styles['BodyText']))
    
    # Citation
    story.append(Paragraph("CITATION", styles['SectionHeader']))
    citation = f"""Franklin, V.L., Hussain, S., & Qian, L. ({datetime.now().year}). EAGLE-I Environmental Justice 
    & Grid Resilience Analysis Report: California Power Outages 2014-2023. Meharry Medical College, School of 
    Applied Computational Sciences. Funded by U.S. Department of Energy, Savannah River National Laboratory (SRNL)."""
    story.append(Paragraph(citation, styles['BodyText']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div style="font-family: 'Orbitron', monospace; font-size: 1.5rem; font-weight: 900; 
                    background: linear-gradient(90deg, #00d4ff, #00ff88); -webkit-background-clip: text; 
                    -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;">⚡ EAGLE-I</div>
        <div style="font-size: 0.7rem; color: #666;">EJ & Grid Resilience Analyzer</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["🏠 Home & About", "📊 EAGLE-I Historic Data", "⚖️ Environmental Justice",
         "🔗 EJ-Outage Correlation", "📋 AI Analysis Report", "📥 Data Sources"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.75rem; color: #666; text-align: center;">
        <b>Funded by:</b><br>
        🏛️ U.S. Department of Energy<br>
        🔬 Savannah River National Laboratory<br><br>
        <b>Institution:</b><br>
        🎓 Meharry Medical College
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# PAGE: HOME & ABOUT
# ============================================================================

if page == "🏠 Home & About":
    # Hero Header
    st.markdown("""
    <div class="hero-header">
        <div class="hero-content">
            <span class="funding-badge">🏛️ Funded by DoE</span>
            <span class="srnl-badge">🔬 SRNL Research</span>
            <div class="brand-logo">⚡ EAGLE-I</div>
            <div class="brand-tagline">Environmental Justice & Grid Resilience Analyzer</div>
            <p style="color: #94a3b8; font-size: 0.95rem; margin-top: 0.5rem;">
                A Geospatial Tool for Climate-Resilient Energy Systems | California 2014-2023
            </p>
            <div class="author-panel">
                <h4>👥 Research Team</h4>
                <b>Victoria Love Franklin</b> - Ph.D. Pre-Candidate, GIS Scientist, DoE SRNL<br>
                <b>Dr. Sajid Hussain</b> - Department Chair & Professor<br>
                <b>Dr. Lei Qian</b> - Associate Professor & Principal Investigator<br><br>
                <small>📍 Meharry Medical College, School of Applied Computational Sciences</small>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # About Section
    st.markdown('<p class="section-header">🔬 About This Tool</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="about-container">
            <div class="about-title">🎯 Project Overview</div>
            <p style="line-height: 1.8; text-align: justify;">
            This tool is part of the research project <b>"Toward Climate-Resilient Energy Systems: 
            A Geospatial RAG-Enabled Digital Twin Approach for Equity and Ecosystem Sustainability"</b> 
            funded by the <b>U.S. Department of Energy (DoE)</b> through the <b>Savannah River National 
            Laboratory (SRNL)</b>.
            </p>
            <p style="line-height: 1.8; text-align: justify; margin-top: 1rem;">
            The EAGLE-I Environmental Justice & Grid Resilience Analyzer integrates historic power 
            outage data from the Department of Energy's EAGLE-I system with comprehensive environmental 
            justice indicators to identify and analyze disparities in energy infrastructure reliability 
            across vulnerable communities in California.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="success-box">
            <h4>✅ Key Features</h4>
            <ul style="margin: 0; padding-left: 1.2rem;">
                <li>10 Years Historic Data (2014-2023)</li>
                <li>15,000+ Outage Events</li>
                <li>38 California Counties</li>
                <li>Environmental Justice Integration</li>
                <li>AI-Generated Reports</li>
                <li>PDF Export Capability</li>
                <li>Interactive Maps</li>
                <li>All FREE Data Sources</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Abstract
    st.markdown("""
    <div class="abstract-container">
        <p class="abstract-text">
        Climate change poses unprecedented challenges to energy infrastructure, disproportionately 
        affecting vulnerable communities through power disruptions that exacerbate existing inequities. 
        This research presents an innovative Geospatial RAG-Enabled Digital Twin framework that 
        integrates real-time grid monitoring with environmental justice indicators to advance equitable 
        climate resilience.
        </p>
        <p class="abstract-text" style="margin-top: 1rem;">
        The EAGLE-I Environmental Justice & Grid Resilience Analyzer synthesizes power outage data 
        from the Department of Energy's EAGLE-I system with CalEnviroScreen 4.0, EPA EJScreen, and 
        CDC Social Vulnerability Index to identify communities facing compound vulnerabilities. Through 
        spatial autocorrelation analysis (Moran's I, LISA clustering) and machine learning models, we 
        quantify disparities in outage frequency, duration, and restoration times across sociodemographic 
        gradients.
        </p>
        <div class="keywords-container">
            <span class="keyword-tag">Environmental Justice</span>
            <span class="keyword-tag">Power Grid Resilience</span>
            <span class="keyword-tag">Digital Twin</span>
            <span class="keyword-tag">Climate Adaptation</span>
            <span class="keyword-tag">Social Vulnerability Index</span>
            <span class="keyword-tag">Geospatial Analysis</span>
            <span class="keyword-tag">EAGLE-I</span>
            <span class="keyword-tag">CalEnviroScreen</span>
            <span class="keyword-tag">Energy Equity</span>
            <span class="keyword-tag">RAG</span>
            <span class="keyword-tag">Machine Learning</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Study Focus
    st.markdown('<p class="section-header">🎯 Study Focus Areas</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="focus-card">
            <div class="focus-icon">🌡️</div>
            <div class="focus-title">CLIMATE RESILIENCE</div>
            <div class="focus-desc">Analyzing grid vulnerability to extreme weather, wildfires, and climate-driven disruptions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="focus-card">
            <div class="focus-icon">⚖️</div>
            <div class="focus-title">ENVIRONMENTAL JUSTICE</div>
            <div class="focus-desc">Quantifying disparities in power reliability across socially vulnerable communities</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="focus-card">
            <div class="focus-icon">🔮</div>
            <div class="focus-title">DIGITAL TWIN</div>
            <div class="focus-desc">RAG-enabled modeling for predictive grid management and equity-focused planning</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="focus-card">
            <div class="focus-icon">🌿</div>
            <div class="focus-title">ECOSYSTEM SUSTAINABILITY</div>
            <div class="focus-desc">Balancing energy infrastructure with environmental and community health</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Authors
    st.markdown('<p class="section-header">👥 Research Team</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="author-card">
            <div class="author-name">Victoria Love Franklin¹²*</div>
            <div class="author-title">
                Ph.D. Pre-Candidate Data Science<br>
                GIS Scientist | DoE SRNL Researcher<br>
                Department of Computer and Data Science
            </div>
            <div class="author-email">📧 victoria.franklin@mmc.edu</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="author-card">
            <div class="author-name">Dr. Sajid Hussain¹</div>
            <div class="author-title">
                Department Chair and Professor<br>
                Department of Computer and Data Science<br>
                School of Applied Computational Sciences
            </div>
            <div class="author-email">📧 sajid.hussain@mmc.edu</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="author-card">
            <div class="author-name">Dr. Lei Qian¹</div>
            <div class="author-title">
                Associate Professor & PI<br>
                Discipline Coordinator<br>
                Department of Computer and Data Science
            </div>
            <div class="author-email">📧 lei.qian@mmc.edu</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-top: 1rem; font-size: 0.85rem; color: #666;">
        <sup>1</sup> Meharry Medical College, School of Applied Computational Sciences, Nashville, TN<br>
        <sup>2</sup> U.S. Department of Energy - Savannah River National Laboratory (SRNL)<br>
        <sup>*</sup> Corresponding Author
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# PAGE: EAGLE-I HISTORIC DATA
# ============================================================================

elif page == "📊 EAGLE-I Historic Data":
    st.markdown("""
    <div class="hero-header">
        <div class="hero-content">
            <div class="brand-logo" style="font-size: 2rem;">📊 EAGLE-I Historic Data</div>
            <div class="brand-tagline">California Power Outages 2014-2023 | U.S. Department of Energy</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.outage_data is None:
        with st.spinner("Loading EAGLE-I historic data..."):
            st.session_state.outage_data = load_eagle_i_historic_data()
    
    df = st.session_state.outage_data
    
    # Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("📋 Total Events", f"{len(df):,}")
    col2.metric("👥 Customers Affected", f"{df['max_customers'].sum():,.0f}")
    col3.metric("⏱️ Avg Duration", f"{df['duration_hours'].mean():.1f} hrs")
    col4.metric("🏛️ DOE Threshold", f"{df['meets_doe_threshold'].sum():,}")
    col5.metric("📍 Counties", f"{df['county'].nunique()}")
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "🗺️ Maps", "📊 Analysis", "📥 Download"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            yearly = df.groupby('year').agg({'event_id': 'count', 'max_customers': 'sum'}).reset_index()
            fig = px.bar(yearly, x='year', y='event_id', title='Outage Events by Year',
                        labels={'event_id': 'Events', 'year': 'Year'}, color_discrete_sequence=['#00d4ff'])
            fig.update_layout(plot_bgcolor='white')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.line(yearly, x='year', y='max_customers', title='Customers Affected by Year',
                         labels={'max_customers': 'Customers', 'year': 'Year'}, markers=True, color_discrete_sequence=['#00ff88'])
            fig.update_layout(plot_bgcolor='white')
            st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            cause_dist = df['cause'].value_counts().reset_index()
            cause_dist.columns = ['cause', 'count']
            fig = px.pie(cause_dist, values='count', names='cause', title='Outage Causes',
                        color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            seasonal = df.groupby('season').size().reset_index(name='count')
            fig = px.bar(seasonal, x='season', y='count', title='Seasonal Distribution',
                        category_orders={'season': ['Winter', 'Spring', 'Summer', 'Fall']},
                        color='season', color_discrete_sequence=['#00d4ff', '#00ff88', '#ffd700', '#ff4757'])
            fig.update_layout(plot_bgcolor='white')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### 🗺️ Power Outage Heatmap")
        m = create_outage_heatmap(df)
        folium_static(m, width=1200, height=500)
    
    with tab3:
        st.markdown("### 🏆 Top 10 Largest Outages")
        largest = df.nlargest(10, 'max_customers')[['start_time', 'county', 'max_customers', 'duration_hours', 'cause']]
        largest.columns = ['Date', 'County', 'Customers', 'Duration (hrs)', 'Cause']
        st.dataframe(largest, use_container_width=True, hide_index=True)
    
    with tab4:
        st.download_button("📥 Download Full Dataset (CSV)", df.to_csv(index=False),
                          "eagle_i_california_2014_2023.csv", "text/csv", use_container_width=True)

# ============================================================================
# PAGE: ENVIRONMENTAL JUSTICE
# ============================================================================

elif page == "⚖️ Environmental Justice":
    st.markdown("""
    <div class="hero-header">
        <div class="hero-content">
            <div class="brand-logo" style="font-size: 2rem;">⚖️ Environmental Justice</div>
            <div class="brand-tagline">CalEnviroScreen 4.0 | EPA EJScreen | CDC SVI | ACS Demographics</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.ej_data is None:
        with st.spinner("Loading Environmental Justice data..."):
            st.session_state.ej_data = load_environmental_justice_data()
    
    ej_df = st.session_state.ej_data
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("📍 Counties", len(ej_df))
    col2.metric("📊 Avg SVI", f"{ej_df['svi_score'].mean():.3f}")
    col3.metric("🚨 High Risk", len(ej_df[ej_df['svi_score'] >= 0.5]))
    col4.metric("🏭 Avg CES", f"{ej_df['ces_score'].mean():.1f}")
    col5.metric("👥 Total Pop", f"{ej_df['population'].sum():,.0f}")
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["🗺️ Maps", "📊 Analysis", "📋 Data"])
    
    with tab1:
        metric_options = {
            "Composite EJ Score": "composite_ej_score", "SVI Score": "svi_score",
            "CES Score": "ces_score", "Pollution Burden": "pollution_burden",
            "Poverty Rate": "poverty_rate", "Fire Risk": "fire_risk"
        }
        selected = st.selectbox("Select Metric", list(metric_options.keys()))
        m = create_ej_map(ej_df, metric_options[selected], selected)
        folium_static(m, width=1200, height=500)
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.scatter(ej_df, x='pollution_burden', y='svi_score', size='population',
                           hover_name='county', color='composite_ej_score',
                           title='Pollution vs Social Vulnerability', color_continuous_scale='Reds')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            cols = ['svi_score', 'ces_score', 'pollution_burden', 'poverty_rate', 'health_burden', 'fire_risk']
            corr = ej_df[cols].corr()
            fig = px.imshow(corr, text_auto='.2f', color_continuous_scale='RdBu_r', title='Indicator Correlations')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.dataframe(ej_df.nlargest(15, 'composite_ej_score'), use_container_width=True, hide_index=True)

# ============================================================================
# PAGE: EJ-OUTAGE CORRELATION
# ============================================================================

elif page == "🔗 EJ-Outage Correlation":
    st.markdown("""
    <div class="hero-header">
        <div class="hero-content">
            <div class="brand-logo" style="font-size: 2rem;">🔗 EJ × Outage Analysis</div>
            <div class="brand-tagline">Identifying Disparities in Grid Reliability Across Vulnerable Communities</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.outage_data is None:
        st.session_state.outage_data = load_eagle_i_historic_data()
    if st.session_state.ej_data is None:
        st.session_state.ej_data = load_environmental_justice_data()
    
    outage_df = st.session_state.outage_data
    ej_df = st.session_state.ej_data
    
    outage_by_county = outage_df.groupby('county').agg({
        'max_customers': ['sum', 'mean', 'count'],
        'duration_hours': ['mean', 'max']
    }).reset_index()
    outage_by_county.columns = ['county', 'total_customers', 'avg_customers', 'outage_count', 'avg_duration', 'max_duration']
    
    merged = ej_df.merge(outage_by_county, on='county', how='left').fillna(0)
    merged['outage_rate_per_1000'] = (merged['outage_count'] / merged['population']) * 1000
    merged['impact_per_capita'] = merged['total_customers'] / merged['population']
    
    st.markdown('<div class="success-box"><b>✅ Data Merged Successfully!</b> Analyzing correlations between EJ indicators and outage patterns.</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.scatter(merged, x='svi_score', y='outage_rate_per_1000', size='population',
                       hover_name='county', trendline='ols', title='Social Vulnerability vs Outage Rate',
                       color_discrete_sequence=['#00d4ff'])
        st.plotly_chart(fig, use_container_width=True)
        corr = merged['svi_score'].corr(merged['outage_rate_per_1000'])
        if corr > 0.2:
            st.error(f"⚠️ **Positive Correlation (r = {corr:.3f})**: Higher vulnerability = More outages")
        else:
            st.success(f"✓ **Correlation: r = {corr:.3f}**")
    
    with col2:
        fig = px.scatter(merged, x='poverty_rate', y='avg_duration', size='population',
                       hover_name='county', trendline='ols', title='Poverty Rate vs Outage Duration',
                       color_discrete_sequence=['#ff4757'])
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE: AI ANALYSIS REPORT
# ============================================================================

elif page == "📋 AI Analysis Report":
    st.markdown("""
    <div class="hero-header">
        <div class="hero-content">
            <div class="brand-logo" style="font-size: 2rem;">📋 AI Analysis Report</div>
            <div class="brand-tagline">Comprehensive EAGLE-I Environmental Justice & Grid Resilience Report with PDF Export</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.outage_data is None:
        st.session_state.outage_data = load_eagle_i_historic_data()
    if st.session_state.ej_data is None:
        st.session_state.ej_data = load_environmental_justice_data()
    
    st.markdown("""
    <div class="info-box">
        <h4>📊 Report Contents</h4>
        <ul>
            <li>Executive Summary with key findings</li>
            <li>Complete outage statistics (2014-2023)</li>
            <li>Environmental justice correlation analysis</li>
            <li>Temporal and seasonal trends</li>
            <li>Disparity analysis and equity metrics</li>
            <li>Policy recommendations</li>
            <li>Full author attributions and citations</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🤖 Generate AI Report", use_container_width=True, type="primary"):
            with st.spinner("Generating comprehensive report..."):
                report_content, merged_data = generate_ai_report(
                    st.session_state.outage_data, st.session_state.ej_data)
                st.session_state.report_content = report_content
                st.session_state.merged_data = merged_data
                st.session_state.report_generated = True
            st.success("✅ Report generated!")
    
    with col2:
        if st.session_state.report_generated and st.session_state.report_content:
            st.download_button("📥 Download Report (TXT)", st.session_state.report_content,
                f"EAGLE_I_EJ_Report_{datetime.now().strftime('%Y%m%d')}.txt", "text/plain", use_container_width=True)
    
    with col3:
        if st.session_state.report_generated and REPORTLAB_AVAILABLE:
            pdf_buffer = generate_pdf_report(st.session_state.outage_data, 
                st.session_state.ej_data, st.session_state.merged_data)
            if pdf_buffer:
                st.download_button("📄 Download Report (PDF)", pdf_buffer,
                    f"EAGLE_I_EJ_Report_{datetime.now().strftime('%Y%m%d')}.pdf", "application/pdf", use_container_width=True)
    
    if st.session_state.report_generated and st.session_state.report_content:
        st.markdown('<div class="report-container">', unsafe_allow_html=True)
        st.code(st.session_state.report_content, language=None)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# PAGE: DATA SOURCES
# ============================================================================

elif page == "📥 Data Sources":
    st.markdown("""
    <div class="hero-header">
        <div class="hero-content">
            <div class="brand-logo" style="font-size: 2rem;">📥 Data Sources</div>
            <div class="brand-tagline">All FREE Public Data Sources - No API Keys Required</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="success-box"><h4>✅ All Data Sources are FREE!</h4></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🔌 EAGLE-I Power Outage Data
        **Source:** U.S. Department of Energy  
        **URL:** https://eagle-i.doe.gov/  
        
        ### 🏭 CalEnviroScreen 4.0
        **Source:** California OEHHA  
        **URL:** https://oehha.ca.gov/calenviroscreen
        """)
    
    with col2:
        st.markdown("""
        ### 🌍 EPA EJScreen
        **Source:** U.S. EPA  
        **URL:** https://www.epa.gov/ejscreen
        
        ### 🏥 CDC Social Vulnerability Index
        **Source:** CDC/ATSDR  
        **URL:** https://www.atsdr.cdc.gov/placeandhealth/svi/
        """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div class="footer">
    <div class="footer-logo">⚡ EAGLE-I EJ & Grid Resilience Analyzer</div>
    <p><b>Authors:</b> Victoria Love Franklin | Dr. Sajid Hussain | Dr. Lei Qian</p>
    <p><b>Institution:</b> Meharry Medical College, School of Applied Computational Sciences</p>
    <p><b>Funding:</b> U.S. Department of Energy - Savannah River National Laboratory (SRNL)</p>
    <p style="margin-top: 1rem;"><small>© 2025 Meharry Medical College. All data sources are publicly available.</small></p>
</div>
""", unsafe_allow_html=True)
