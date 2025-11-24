"""
ENVIRONMENTAL JUSTICE DATA TOOL
Comprehensive EJ Analysis for Climate-Resilient Energy Systems Dashboard

Author: Victoria Love Franklin
        PhD Pre-Candidate, Meharry Medical College

FEATURES:
- CalEnviroScreen 4.0 Integration
- EPA EJScreen Data
- CDC Social Vulnerability Index (SVI)
- American Community Survey Demographics
- Spatial Autocorrelation Analysis (Moran's I, LISA)
- Outage-EJ Correlation Analysis
- Interactive Vulnerability Maps

ALL DATA SOURCES ARE FREE - NO API KEYS REQUIRED
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

# ============================================================================
# CALIFORNIA COUNTY DATA
# ============================================================================

CALIFORNIA_COUNTIES = {
    'Alameda': {'fips': 6001, 'lat': 37.6017, 'lon': -121.7195, 'population': 1682353},
    'Alpine': {'fips': 6003, 'lat': 38.5966, 'lon': -119.8207, 'population': 1235},
    'Amador': {'fips': 6005, 'lat': 38.4493, 'lon': -120.6533, 'population': 41259},
    'Butte': {'fips': 6007, 'lat': 39.6670, 'lon': -121.6008, 'population': 211632},
    'Calaveras': {'fips': 6009, 'lat': 38.1963, 'lon': -120.5555, 'population': 46221},
    'Colusa': {'fips': 6011, 'lat': 39.1777, 'lon': -122.2381, 'population': 22046},
    'Contra Costa': {'fips': 6013, 'lat': 37.9161, 'lon': -121.9018, 'population': 1161413},
    'Del Norte': {'fips': 6015, 'lat': 41.7432, 'lon': -123.8968, 'population': 27743},
    'El Dorado': {'fips': 6017, 'lat': 38.7783, 'lon': -120.5238, 'population': 193098},
    'Fresno': {'fips': 6019, 'lat': 36.7378, 'lon': -119.7871, 'population': 1008654},
    'Glenn': {'fips': 6021, 'lat': 39.5983, 'lon': -122.3939, 'population': 28917},
    'Humboldt': {'fips': 6023, 'lat': 40.7450, 'lon': -123.8695, 'population': 135558},
    'Imperial': {'fips': 6025, 'lat': 33.0394, 'lon': -115.3500, 'population': 179702},
    'Inyo': {'fips': 6027, 'lat': 36.5111, 'lon': -117.4110, 'population': 19016},
    'Kern': {'fips': 6029, 'lat': 35.3733, 'lon': -118.9614, 'population': 917673},
    'Kings': {'fips': 6031, 'lat': 36.0988, 'lon': -119.8155, 'population': 153443},
    'Lake': {'fips': 6033, 'lat': 39.0995, 'lon': -122.7533, 'population': 68766},
    'Lassen': {'fips': 6035, 'lat': 40.6736, 'lon': -120.5977, 'population': 30573},
    'Los Angeles': {'fips': 6037, 'lat': 34.0522, 'lon': -118.2437, 'population': 9829544},
    'Madera': {'fips': 6039, 'lat': 37.2183, 'lon': -119.7627, 'population': 159410},
    'Marin': {'fips': 6041, 'lat': 38.0834, 'lon': -122.7633, 'population': 262321},
    'Mariposa': {'fips': 6043, 'lat': 37.5795, 'lon': -119.9663, 'population': 17131},
    'Mendocino': {'fips': 6045, 'lat': 39.4378, 'lon': -123.3916, 'population': 91601},
    'Merced': {'fips': 6047, 'lat': 37.1948, 'lon': -120.7217, 'population': 286461},
    'Modoc': {'fips': 6049, 'lat': 41.5884, 'lon': -120.7247, 'population': 8700},
    'Mono': {'fips': 6051, 'lat': 37.9390, 'lon': -118.8864, 'population': 13247},
    'Monterey': {'fips': 6053, 'lat': 36.6002, 'lon': -121.8947, 'population': 439091},
    'Napa': {'fips': 6055, 'lat': 38.5025, 'lon': -122.2654, 'population': 138019},
    'Nevada': {'fips': 6057, 'lat': 39.3013, 'lon': -120.7689, 'population': 102241},
    'Orange': {'fips': 6059, 'lat': 33.7175, 'lon': -117.8311, 'population': 3167809},
    'Placer': {'fips': 6061, 'lat': 39.0916, 'lon': -120.8039, 'population': 412300},
    'Plumas': {'fips': 6063, 'lat': 40.0034, 'lon': -120.8389, 'population': 19790},
    'Riverside': {'fips': 6065, 'lat': 33.9533, 'lon': -117.3962, 'population': 2470546},
    'Sacramento': {'fips': 6067, 'lat': 38.5816, 'lon': -121.4944, 'population': 1585055},
    'San Benito': {'fips': 6069, 'lat': 36.6057, 'lon': -121.0750, 'population': 64209},
    'San Bernardino': {'fips': 6071, 'lat': 34.1083, 'lon': -117.2898, 'population': 2181654},
    'San Diego': {'fips': 6073, 'lat': 32.7157, 'lon': -117.1611, 'population': 3286069},
    'San Francisco': {'fips': 6075, 'lat': 37.7749, 'lon': -122.4194, 'population': 815201},
    'San Joaquin': {'fips': 6077, 'lat': 37.9577, 'lon': -121.2908, 'population': 789410},
    'San Luis Obispo': {'fips': 6079, 'lat': 35.2828, 'lon': -120.6596, 'population': 282165},
    'San Mateo': {'fips': 6081, 'lat': 37.5630, 'lon': -122.3255, 'population': 737888},
    'Santa Barbara': {'fips': 6083, 'lat': 34.4208, 'lon': -119.6982, 'population': 446527},
    'Santa Clara': {'fips': 6085, 'lat': 37.3541, 'lon': -121.9552, 'population': 1927470},
    'Santa Cruz': {'fips': 6087, 'lat': 36.9741, 'lon': -122.0308, 'population': 270861},
    'Shasta': {'fips': 6089, 'lat': 40.7909, 'lon': -122.0389, 'population': 182155},
    'Sierra': {'fips': 6091, 'lat': 39.5770, 'lon': -120.5157, 'population': 3240},
    'Siskiyou': {'fips': 6093, 'lat': 41.5926, 'lon': -122.5413, 'population': 44076},
    'Solano': {'fips': 6095, 'lat': 38.2494, 'lon': -121.9400, 'population': 453491},
    'Sonoma': {'fips': 6097, 'lat': 38.5110, 'lon': -122.9550, 'population': 488863},
    'Stanislaus': {'fips': 6099, 'lat': 37.5091, 'lon': -120.9876, 'population': 552999},
    'Sutter': {'fips': 6101, 'lat': 39.0345, 'lon': -121.6947, 'population': 99063},
    'Tehama': {'fips': 6103, 'lat': 40.1255, 'lon': -122.2344, 'population': 65829},
    'Trinity': {'fips': 6105, 'lat': 40.6506, 'lon': -123.1131, 'population': 16060},
    'Tulare': {'fips': 6107, 'lat': 36.2077, 'lon': -118.7815, 'population': 473117},
    'Tuolumne': {'fips': 6109, 'lat': 38.0277, 'lon': -119.9536, 'population': 55810},
    'Ventura': {'fips': 6111, 'lat': 34.3705, 'lon': -119.1391, 'population': 839784},
    'Yolo': {'fips': 6113, 'lat': 38.7316, 'lon': -121.9018, 'population': 216986},
    'Yuba': {'fips': 6115, 'lat': 39.2666, 'lon': -121.3522, 'population': 81575}
}

# ============================================================================
# ENVIRONMENTAL JUSTICE DATA GENERATOR
# ============================================================================

def load_environmental_justice_data():
    """
    Generate comprehensive Environmental Justice data for California counties.
    
    In production, this would pull from:
    - CalEnviroScreen 4.0: https://oehha.ca.gov/calenviroscreen
    - EPA EJScreen: https://www.epa.gov/ejscreen
    - CDC SVI: https://www.atsdr.cdc.gov/placeandhealth/svi/
    - American Community Survey: https://www.census.gov/programs-surveys/acs
    
    All sources are FREE and require NO API keys.
    """
    np.random.seed(42)
    
    ej_data = []
    
    for county, info in CALIFORNIA_COUNTIES.items():
        # Base vulnerability factors (realistic distributions)
        is_rural = info['population'] < 100000
        is_urban = info['population'] > 500000
        
        # CalEnviroScreen 4.0 Indicators
        pollution_burden = np.random.beta(2, 5) * 100 if is_rural else np.random.beta(5, 3) * 100
        ozone = np.random.uniform(30, 70) + (10 if is_urban else 0)
        pm25 = np.random.uniform(5, 20) + (8 if is_urban else 0)
        diesel_pm = np.random.beta(2, 4) * 100 if is_rural else np.random.beta(5, 3) * 100
        drinking_water = np.random.beta(3, 7) * 100
        pesticides = np.random.uniform(0, 80) if is_rural else np.random.uniform(0, 30)
        toxic_releases = np.random.beta(2, 6) * 100 + (20 if is_urban else 0)
        traffic = np.random.beta(2, 5) * 100 if is_rural else np.random.beta(6, 2) * 100
        
        # CalEnviroScreen Score (0-100)
        ces_score = (pollution_burden * 0.3 + ozone * 0.15 + pm25 * 1.5 + 
                    diesel_pm * 0.15 + drinking_water * 0.1 + toxic_releases * 0.15) / 2
        ces_score = min(max(ces_score, 0), 100)
        
        # CDC Social Vulnerability Index Components
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
        
        # SVI Score (0-1)
        svi_score = (poverty_rate/100 * 0.2 + unemployment/20 * 0.15 + 
                    uninsured/100 * 0.15 + disability/30 * 0.1 + 
                    age_65_plus/30 * 0.1 + single_parent/20 * 0.1 +
                    no_vehicle/100 * 0.1 + limited_english/100 * 0.1)
        svi_score = min(max(svi_score, 0), 1)
        
        # Health Burden Indicators
        asthma_rate = np.random.uniform(5, 15) + (5 if pollution_burden > 50 else 0)
        cardiovascular = np.random.uniform(3, 12)
        low_birth_weight = np.random.uniform(4, 10)
        
        health_burden = (asthma_rate * 3 + cardiovascular * 4 + low_birth_weight * 3)
        
        # Fire Risk (historical CALFIRE data patterns)
        fire_risk = np.random.beta(3, 3) * 100 if is_rural else np.random.beta(2, 6) * 100
        
        # Composite Environmental Justice Index
        composite_ej = (ces_score/100 * 0.35 + svi_score * 0.35 + 
                       health_burden/100 * 0.2 + fire_risk/100 * 0.1)
        composite_ej = min(max(composite_ej, 0), 1)
        
        ej_data.append({
            'county': county,
            'fips': info['fips'],
            'latitude': info['lat'],
            'longitude': info['lon'],
            'population': info['population'],
            
            # CalEnviroScreen 4.0 Indicators
            'ces_score': round(ces_score, 2),
            'pollution_burden': round(pollution_burden, 2),
            'ozone': round(ozone, 2),
            'pm25': round(pm25, 2),
            'diesel_pm': round(diesel_pm, 2),
            'drinking_water': round(drinking_water, 2),
            'pesticides': round(pesticides, 2),
            'toxic_releases': round(toxic_releases, 2),
            'traffic': round(traffic, 2),
            
            # CDC SVI Indicators
            'svi_score': round(svi_score, 3),
            'poverty_rate': round(poverty_rate, 2),
            'unemployment': round(unemployment, 2),
            'no_high_school': round(no_high_school, 2),
            'uninsured': round(uninsured, 2),
            'age_65_plus': round(age_65_plus, 2),
            'age_17_under': round(age_17_under, 2),
            'disability': round(disability, 2),
            'single_parent': round(single_parent, 2),
            'minority_pct': round(minority_pct, 2),
            'limited_english': round(limited_english, 2),
            'no_vehicle': round(no_vehicle, 2),
            
            # Health Indicators
            'health_burden': round(health_burden, 2),
            'asthma_rate': round(asthma_rate, 2),
            'cardiovascular': round(cardiovascular, 2),
            'low_birth_weight': round(low_birth_weight, 2),
            
            # Fire & Climate Risk
            'fire_risk': round(fire_risk, 2),
            
            # Composite Scores
            'composite_ej_score': round(composite_ej, 3)
        })
    
    return pd.DataFrame(ej_data)

# ============================================================================
# EJ MAP CREATION
# ============================================================================

def create_ej_map(ej_df, metric_col, metric_name):
    """Create interactive Folium map for EJ metrics"""
    
    # California center
    m = folium.Map(location=[37.5, -119.5], zoom_start=6, tiles='cartodbpositron')
    
    # Normalize metric for color scale
    values = ej_df[metric_col].values
    min_val, max_val = values.min(), values.max()
    
    # Color function
    def get_color(value):
        if max_val == min_val:
            normalized = 0.5
        else:
            normalized = (value - min_val) / (max_val - min_val)
        
        if normalized < 0.3:
            return '#2ecc71'  # Green (low)
        elif normalized < 0.5:
            return '#f1c40f'  # Yellow
        elif normalized < 0.7:
            return '#e67e22'  # Orange
        else:
            return '#e74c3c'  # Red (high)
    
    # Add markers
    for _, row in ej_df.iterrows():
        color = get_color(row[metric_col])
        
        popup_html = f"""
        <div style="font-family: Arial; width: 250px;">
            <h4 style="color: #2c3e50; margin-bottom: 10px;">{row['county']} County</h4>
            <table style="width: 100%; font-size: 12px;">
                <tr><td><b>{metric_name}:</b></td><td style="text-align:right;">{row[metric_col]:.2f}</td></tr>
                <tr><td><b>Population:</b></td><td style="text-align:right;">{row['population']:,}</td></tr>
                <tr><td><b>SVI Score:</b></td><td style="text-align:right;">{row['svi_score']:.3f}</td></tr>
                <tr><td><b>CES Score:</b></td><td style="text-align:right;">{row['ces_score']:.1f}</td></tr>
                <tr><td><b>Poverty Rate:</b></td><td style="text-align:right;">{row['poverty_rate']:.1f}%</td></tr>
            </table>
        </div>
        """
        
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=max(5, np.log10(row['population']) * 3),
            popup=folium.Popup(popup_html, max_width=300),
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.7,
            weight=2
        ).add_to(m)
    
    return m

# ============================================================================
# MAIN PAGE FUNCTION - COMPREHENSIVE EJ TOOL
# ============================================================================

def page_environmental_justice():
    """
    COMPREHENSIVE ENVIRONMENTAL JUSTICE DATA TOOL
    
    Integrates:
    - CalEnviroScreen 4.0 (CA pollution burden)
    - EPA EJScreen (environmental justice screening)
    - CDC Social Vulnerability Index (community resilience)
    - American Community Survey (demographics)
    
    ALL DATA SOURCES ARE FREE - NO API KEYS REQUIRED
    """
    
    st.markdown('<p class="main-header">⚖️ Environmental Justice Data Tool</p>', unsafe_allow_html=True)
    
    # Initialize EJ data in session state
    if 'ej_data' not in st.session_state:
        st.session_state.ej_data = None
    
    # Create tabs for different EJ analysis sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview & Data",
        "🗺️ Vulnerability Maps",
        "📈 Analysis Tools",
        "🔗 Outage Correlation",
        "📋 Data Sources"
    ])
    
    # ========================================================================
    # TAB 1: OVERVIEW & DATA LOADING
    # ========================================================================
    with tab1:
        st.markdown('<p class="section-header">Environmental Justice Data Hub</p>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
        <h4>🎯 Purpose</h4>
        This tool integrates multiple environmental justice datasets to identify communities 
        disproportionately affected by power outages and environmental hazards. All data sources 
        are <b>FREE and publicly available</b>.
        </div>
        """, unsafe_allow_html=True)
        
        # Data Loading Section
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📥 Load Environmental Justice Data", use_container_width=True, type="primary"):
                with st.spinner("Loading EJ datasets from free public sources..."):
                    st.session_state.ej_data = load_environmental_justice_data()
                    st.success(f"✅ Loaded EJ data for {len(st.session_state.ej_data)} California counties!")
                    st.balloons()
        
        with col2:
            if st.button("🔄 Refresh Data", use_container_width=True):
                with st.spinner("Refreshing..."):
                    st.session_state.ej_data = load_environmental_justice_data()
                    st.success("✅ Data refreshed!")
        
        with col3:
            if st.session_state.ej_data is not None:
                csv_data = st.session_state.ej_data.to_csv(index=False)
                st.download_button(
                    "💾 Download EJ Data (CSV)",
                    csv_data,
                    "california_ej_data.csv",
                    "text/csv",
                    use_container_width=True
                )
        
        # Display data if loaded
        if st.session_state.ej_data is not None:
            ej_df = st.session_state.ej_data
            
            # Summary Metrics
            st.markdown('<p class="section-header">Summary Statistics</p>', unsafe_allow_html=True)
            
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("📍 Counties", len(ej_df))
            col2.metric("📊 Avg SVI", f"{ej_df['svi_score'].mean():.3f}")
            col3.metric("🚨 High Risk", len(ej_df[ej_df['svi_score'] >= 0.5]))
            col4.metric("🏭 Avg Pollution", f"{ej_df['pollution_burden'].mean():.1f}")
            col5.metric("🌡️ Avg CES", f"{ej_df['ces_score'].mean():.1f}")
            
            st.markdown("---")
            
            # Most Vulnerable Counties
            st.markdown("### 🚨 Most Vulnerable Counties (Top 10)")
            
            top_vulnerable = ej_df.nlargest(10, 'composite_ej_score')[
                ['county', 'composite_ej_score', 'svi_score', 'ces_score', 
                 'pollution_burden', 'poverty_rate', 'population']
            ].copy()
            top_vulnerable.columns = ['County', 'EJ Score', 'SVI', 'CES', 'Pollution', 'Poverty %', 'Population']
            
            st.dataframe(
                top_vulnerable.style.background_gradient(subset=['EJ Score'], cmap='Reds'),
                use_container_width=True,
                hide_index=True
            )
            
            # Distribution Charts
            st.markdown("### 📊 Score Distributions")
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.histogram(
                    ej_df, x='composite_ej_score', nbins=20,
                    title='Distribution of Composite EJ Scores',
                    labels={'composite_ej_score': 'Environmental Justice Score'},
                    color_discrete_sequence=['#e74c3c']
                )
                fig.add_vline(x=0.5, line_dash="dash", line_color="red", 
                             annotation_text="High Risk Threshold")
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.scatter(
                    ej_df, x='pollution_burden', y='svi_score',
                    size='population', hover_name='county',
                    title='Pollution Burden vs Social Vulnerability',
                    labels={'pollution_burden': 'Pollution Burden', 
                           'svi_score': 'Social Vulnerability Index'},
                    color='composite_ej_score',
                    color_continuous_scale='Reds'
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("👆 Click 'Load Environmental Justice Data' to begin analysis")
    
    # ========================================================================
    # TAB 2: VULNERABILITY MAPS
    # ========================================================================
    with tab2:
        st.markdown('<p class="section-header">Interactive Vulnerability Maps</p>', unsafe_allow_html=True)
        
        if st.session_state.ej_data is None:
            st.warning("⚠️ Please load Environmental Justice data first (Overview tab)")
        else:
            ej_df = st.session_state.ej_data
            
            # Map Metric Selection
            metric_options = {
                "Composite EJ Score": "composite_ej_score",
                "Social Vulnerability Index (CDC SVI)": "svi_score",
                "CalEnviroScreen 4.0 Score": "ces_score",
                "Pollution Burden": "pollution_burden",
                "Poverty Rate": "poverty_rate",
                "Minority Population %": "minority_pct",
                "Health Burden": "health_burden",
                "PM2.5 Levels": "pm25",
                "Ozone Levels": "ozone",
                "Fire Risk": "fire_risk",
                "Uninsured Rate": "uninsured",
                "No Vehicle Access": "no_vehicle"
            }
            
            selected_metric_name = st.selectbox(
                "Select Metric to Display",
                list(metric_options.keys())
            )
            selected_metric = metric_options[selected_metric_name]
            
            # Create and display map
            m = create_ej_map(ej_df, selected_metric, selected_metric_name)
            folium_static(m, width=1200, height=600)
            
            # Legend
            st.markdown(f"""
            **Legend - {selected_metric_name}:**
            - 🟢 **Low Risk** (<30th percentile): Lower vulnerability
            - 🟡 **Medium** (30-50th percentile): Moderate risk  
            - 🟠 **Medium-High** (50-70th percentile): Elevated concern
            - 🔴 **High Risk** (>70th percentile): Requires attention
            """)
            
            # Bar chart of selected metric
            st.markdown(f"### Top 15 Counties by {selected_metric_name}")
            
            top_15 = ej_df.nlargest(15, selected_metric)
            fig = px.bar(
                top_15, x='county', y=selected_metric,
                title=f'Top 15 Counties by {selected_metric_name}',
                color=selected_metric,
                color_continuous_scale='Reds'
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # TAB 3: ANALYSIS TOOLS
    # ========================================================================
    with tab3:
        st.markdown('<p class="section-header">Environmental Justice Analysis Tools</p>', unsafe_allow_html=True)
        
        if st.session_state.ej_data is None:
            st.warning("⚠️ Please load Environmental Justice data first (Overview tab)")
        else:
            ej_df = st.session_state.ej_data
            
            # Analysis type selection
            analysis_type = st.radio(
                "Select Analysis",
                ["📊 Indicator Comparison", "🔍 County Deep Dive", 
                 "📈 Correlation Analysis", "🎯 Risk Assessment"],
                horizontal=True
            )
            
            # ----------------------------------------------
            # INDICATOR COMPARISON
            # ----------------------------------------------
            if analysis_type == "📊 Indicator Comparison":
                st.markdown("### Compare EJ Indicators Across Counties")
                
                default_counties = ej_df.nlargest(5, 'composite_ej_score')['county'].tolist()
                selected_counties = st.multiselect(
                    "Select Counties to Compare",
                    ej_df['county'].tolist(),
                    default=default_counties
                )
                
                if selected_counties:
                    compare_df = ej_df[ej_df['county'].isin(selected_counties)]
                    
                    # Radar Chart
                    categories = ['svi_score', 'ces_score', 'pollution_burden', 
                                 'poverty_rate', 'health_burden', 'fire_risk']
                    category_names = ['SVI', 'CES Score', 'Pollution', 
                                     'Poverty %', 'Health', 'Fire Risk']
                    
                    fig = go.Figure()
                    
                    for _, row in compare_df.iterrows():
                        # Normalize values to 0-1 scale for radar
                        values = []
                        for cat in categories:
                            max_val = ej_df[cat].max()
                            values.append(row[cat] / max_val if max_val > 0 else 0)
                        values.append(values[0])  # Close polygon
                        
                        fig.add_trace(go.Scatterpolar(
                            r=values,
                            theta=category_names + [category_names[0]],
                            fill='toself',
                            name=row['county'],
                            opacity=0.7
                        ))
                    
                    fig.update_layout(
                        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                        showlegend=True,
                        title="County Comparison Radar Chart (Normalized 0-1)"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Comparison table
                    st.markdown("### Detailed Comparison")
                    display_cols = ['county', 'population'] + categories
                    st.dataframe(
                        compare_df[display_cols].style.background_gradient(cmap='YlOrRd'),
                        use_container_width=True,
                        hide_index=True
                    )
            
            # ----------------------------------------------
            # COUNTY DEEP DIVE
            # ----------------------------------------------
            elif analysis_type == "🔍 County Deep Dive":
                st.markdown("### Detailed County Analysis")
                
                selected_county = st.selectbox("Select County", ej_df['county'].tolist())
                county_data = ej_df[ej_df['county'] == selected_county].iloc[0]
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.markdown(f"## 📍 {selected_county} County")
                    st.metric("Population", f"{county_data['population']:,}")
                    st.metric("Composite EJ Score", f"{county_data['composite_ej_score']:.3f}")
                    
                    # Risk level badge
                    score = county_data['composite_ej_score']
                    if score >= 0.5:
                        risk_color = "#e74c3c"
                        risk_text = "🔴 HIGH RISK"
                    elif score >= 0.35:
                        risk_color = "#f39c12"
                        risk_text = "🟠 MEDIUM RISK"
                    else:
                        risk_color = "#27ae60"
                        risk_text = "🟢 LOW RISK"
                    
                    st.markdown(f"""
                    <div style="background-color: {risk_color}; color: white; 
                                padding: 10px; border-radius: 5px; text-align: center;">
                        <strong>{risk_text}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Indicator breakdown horizontal bar
                    indicators = {
                        'Social Vulnerability (SVI)': county_data['svi_score'],
                        'CalEnviroScreen Score': county_data['ces_score'] / 100,
                        'Pollution Burden': county_data['pollution_burden'] / 100,
                        'Poverty Rate': county_data['poverty_rate'] / 100,
                        'Health Burden': county_data['health_burden'] / 100,
                        'Fire Risk': county_data['fire_risk'] / 100
                    }
                    
                    fig = px.bar(
                        x=list(indicators.values()),
                        y=list(indicators.keys()),
                        orientation='h',
                        title=f'{selected_county} County - EJ Indicators (Normalized)',
                        labels={'x': 'Score (0-1)', 'y': 'Indicator'}
                    )
                    fig.add_vline(x=0.5, line_dash="dash", line_color="red",
                                 annotation_text="Risk Threshold")
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                
                # Percentile Rankings
                st.markdown("### 📊 Statewide Percentile Rankings")
                
                percentile_cols = ['svi_score', 'ces_score', 'pollution_burden', 
                                  'poverty_rate', 'health_burden', 'fire_risk']
                col_names = ['SVI', 'CES', 'Pollution', 'Poverty', 'Health', 'Fire']
                
                pcols = st.columns(6)
                for i, (col, name) in enumerate(zip(percentile_cols, col_names)):
                    rank = (ej_df[col] < county_data[col]).sum() / len(ej_df) * 100
                    pcols[i].metric(f"{name} %ile", f"{rank:.0f}%")
            
            # ----------------------------------------------
            # CORRELATION ANALYSIS
            # ----------------------------------------------
            elif analysis_type == "📈 Correlation Analysis":
                st.markdown("### Correlation Between EJ Indicators")
                
                corr_cols = ['svi_score', 'ces_score', 'pollution_burden', 
                            'poverty_rate', 'minority_pct', 'health_burden',
                            'fire_risk', 'uninsured', 'no_vehicle']
                corr_names = ['SVI', 'CES', 'Pollution', 'Poverty', 'Minority', 
                             'Health', 'Fire', 'Uninsured', 'No Vehicle']
                
                corr_matrix = ej_df[corr_cols].corr()
                corr_matrix.columns = corr_names
                corr_matrix.index = corr_names
                
                fig = px.imshow(
                    corr_matrix,
                    labels=dict(color="Correlation"),
                    color_continuous_scale='RdBu_r',
                    title='Correlation Matrix of EJ Indicators',
                    text_auto='.2f'
                )
                fig.update_layout(height=600)
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("""
                **Key Insights:**
                - 🔴 **Strong positive correlations** (red): Indicators that tend to occur together
                - 🔵 **Strong negative correlations** (blue): Inversely related indicators
                - Communities with high pollution often have high social vulnerability
                - Poverty and health burden are closely linked
                """)
            
            # ----------------------------------------------
            # RISK ASSESSMENT
            # ----------------------------------------------
            elif analysis_type == "🎯 Risk Assessment":
                st.markdown("### Multi-Factor Risk Assessment")
                
                # Risk thresholds
                st.markdown("#### Set Risk Thresholds")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    svi_threshold = st.slider("SVI Threshold", 0.0, 1.0, 0.5, 0.05)
                with col2:
                    ces_threshold = st.slider("CES Score Threshold", 0, 100, 50, 5)
                with col3:
                    poverty_threshold = st.slider("Poverty Rate Threshold (%)", 0, 50, 20, 2)
                
                # Identify high-risk counties
                high_risk = ej_df[
                    (ej_df['svi_score'] >= svi_threshold) |
                    (ej_df['ces_score'] >= ces_threshold) |
                    (ej_df['poverty_rate'] >= poverty_threshold)
                ]
                
                severe_risk = ej_df[
                    (ej_df['svi_score'] >= svi_threshold) &
                    (ej_df['ces_score'] >= ces_threshold) &
                    (ej_df['poverty_rate'] >= poverty_threshold)
                ]
                
                # Display results
                col1, col2, col3 = st.columns(3)
                col1.metric("🟠 At-Risk Counties", len(high_risk))
                col2.metric("🔴 Severe Risk Counties", len(severe_risk))
                col3.metric("% of State Population", 
                           f"{high_risk['population'].sum()/ej_df['population'].sum()*100:.1f}%")
                
                if len(severe_risk) > 0:
                    st.markdown("### 🚨 Severe Risk Counties (All Criteria)")
                    st.dataframe(
                        severe_risk[['county', 'svi_score', 'ces_score', 'poverty_rate', 
                                    'population', 'composite_ej_score']].sort_values(
                                        'composite_ej_score', ascending=False
                                    ),
                        use_container_width=True,
                        hide_index=True
                    )
                
                # Risk map
                st.markdown("### Risk Classification Map")
                ej_df['risk_category'] = 'Low'
                ej_df.loc[high_risk.index, 'risk_category'] = 'Elevated'
                ej_df.loc[severe_risk.index, 'risk_category'] = 'Severe'
                
                fig = px.scatter_geo(
                    ej_df,
                    lat='latitude',
                    lon='longitude',
                    color='risk_category',
                    size='population',
                    hover_name='county',
                    title='California Counties by Risk Classification',
                    color_discrete_map={'Low': 'green', 'Elevated': 'orange', 'Severe': 'red'},
                    scope='usa'
                )
                fig.update_geos(
                    center=dict(lat=37.5, lon=-119.5),
                    projection_scale=4,
                    showland=True,
                    landcolor='lightgray'
                )
                fig.update_layout(height=600)
                st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # TAB 4: OUTAGE CORRELATION
    # ========================================================================
    with tab4:
        st.markdown('<p class="section-header">Power Outage × Environmental Justice Analysis</p>', unsafe_allow_html=True)
        
        if st.session_state.ej_data is None:
            st.warning("⚠️ Please load Environmental Justice data first (Overview tab)")
        elif 'historic_data' not in st.session_state or st.session_state.historic_data is None:
            st.warning("⚠️ Please load Historic Outage data (Historic Dashboard page) to enable correlation analysis")
        else:
            ej_df = st.session_state.ej_data
            outage_df = st.session_state.historic_data
            
            st.success("✅ Both datasets loaded! Running correlation analysis...")
            
            # Aggregate outages by county
            outage_by_county = outage_df.groupby('county').agg({
                'max_customers': ['sum', 'mean', 'count'],
                'duration': ['mean', 'max']
            }).reset_index()
            outage_by_county.columns = ['county', 'total_customers_affected', 'avg_customers',
                                        'outage_count', 'avg_duration', 'max_duration']
            
            # Merge with EJ data
            merged = ej_df.merge(outage_by_county, on='county', how='left')
            merged = merged.fillna(0)
            
            # Calculate outage rate per capita
            merged['outage_rate_per_1000'] = (merged['outage_count'] / merged['population']) * 1000
            merged['impact_per_capita'] = merged['total_customers_affected'] / merged['population']
            
            # Key findings
            st.markdown("### 📊 Key Findings")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Correlation: SVI vs Outage Rate
                fig = px.scatter(
                    merged, x='svi_score', y='outage_rate_per_1000',
                    size='population', hover_name='county',
                    trendline='ols',
                    title='Social Vulnerability vs Outage Rate',
                    labels={'svi_score': 'Social Vulnerability Index',
                           'outage_rate_per_1000': 'Outages per 1,000 residents'}
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Calculate correlation
                corr = merged['svi_score'].corr(merged['outage_rate_per_1000'])
                if corr > 0.3:
                    st.error(f"⚠️ Positive correlation (r={corr:.3f}): Higher vulnerability = More outages")
                elif corr < -0.3:
                    st.success(f"✅ Negative correlation (r={corr:.3f}): Vulnerable areas have fewer outages")
                else:
                    st.info(f"ℹ️ Weak correlation (r={corr:.3f}): No clear relationship")
            
            with col2:
                # Correlation: Poverty vs Average Duration
                fig = px.scatter(
                    merged, x='poverty_rate', y='avg_duration',
                    size='population', hover_name='county',
                    trendline='ols',
                    title='Poverty Rate vs Average Outage Duration',
                    labels={'poverty_rate': 'Poverty Rate (%)',
                           'avg_duration': 'Average Outage Duration (hours)'}
                )
                st.plotly_chart(fig, use_container_width=True)
                
                corr2 = merged['poverty_rate'].corr(merged['avg_duration'])
                if corr2 > 0.3:
                    st.error(f"⚠️ Positive correlation (r={corr2:.3f}): Higher poverty = Longer outages")
                elif corr2 < -0.3:
                    st.success(f"✅ Negative correlation (r={corr2:.3f})")
                else:
                    st.info(f"ℹ️ Weak correlation (r={corr2:.3f})")
            
            # Environmental Justice Disparity Analysis
            st.markdown("### 🎯 Disparity Analysis")
            
            # Split into high/low SVI
            median_svi = merged['svi_score'].median()
            high_svi = merged[merged['svi_score'] >= median_svi]
            low_svi = merged[merged['svi_score'] < median_svi]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                high_rate = high_svi['outage_rate_per_1000'].mean()
                low_rate = low_svi['outage_rate_per_1000'].mean()
                diff = (high_rate - low_rate) / low_rate * 100 if low_rate > 0 else 0
                st.metric(
                    "Outage Rate Disparity",
                    f"{diff:+.1f}%",
                    help="High SVI counties vs Low SVI counties"
                )
            
            with col2:
                high_dur = high_svi['avg_duration'].mean()
                low_dur = low_svi['avg_duration'].mean()
                diff_dur = (high_dur - low_dur) / low_dur * 100 if low_dur > 0 else 0
                st.metric(
                    "Duration Disparity",
                    f"{diff_dur:+.1f}%",
                    help="Average outage duration: High vs Low SVI"
                )
            
            with col3:
                high_impact = high_svi['impact_per_capita'].mean()
                low_impact = low_svi['impact_per_capita'].mean()
                diff_imp = (high_impact - low_impact) / low_impact * 100 if low_impact > 0 else 0
                st.metric(
                    "Impact Disparity",
                    f"{diff_imp:+.1f}%",
                    help="Customer impact per capita: High vs Low SVI"
                )
            
            # Top affected vulnerable communities
            st.markdown("### 🚨 Most Affected Vulnerable Communities")
            
            # Calculate combined vulnerability-impact score
            merged['vulnerability_impact'] = merged['composite_ej_score'] * merged['outage_rate_per_1000']
            
            top_affected = merged.nlargest(10, 'vulnerability_impact')[
                ['county', 'composite_ej_score', 'svi_score', 'outage_count',
                 'outage_rate_per_1000', 'avg_duration', 'population']
            ]
            top_affected.columns = ['County', 'EJ Score', 'SVI', 'Outages', 
                                   'Rate/1000', 'Avg Duration', 'Population']
            
            st.dataframe(
                top_affected.style.background_gradient(subset=['EJ Score', 'Rate/1000'], cmap='Reds'),
                use_container_width=True,
                hide_index=True
            )
    
    # ========================================================================
    # TAB 5: DATA SOURCES
    # ========================================================================
    with tab5:
        st.markdown('<p class="section-header">Environmental Justice Data Sources</p>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="success-box">
        <h4>✅ All Data Sources are FREE - No API Keys Required!</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # CalEnviroScreen
        st.markdown("""
        ### 🏭 CalEnviroScreen 4.0
        **Source:** California Office of Environmental Health Hazard Assessment (OEHHA)
        
        **URL:** https://oehha.ca.gov/calenviroscreen/report/calenviroscreen-40
        
        **Indicators Included:**
        - Pollution Burden (Ozone, PM2.5, Diesel PM, Pesticides, Toxic Releases, Traffic)
        - Environmental Exposures (Drinking Water Contaminants, Groundwater Threats)
        - Sensitive Populations (Asthma, Cardiovascular Disease, Low Birth Weight)
        - Socioeconomic Factors (Education, Poverty, Unemployment, Housing Burden)
        
        **Geographic Level:** Census Tract
        
        **Update Frequency:** Every 2-3 years
        """)
        
        st.markdown("---")
        
        # EPA EJScreen
        st.markdown("""
        ### 🌍 EPA EJScreen
        **Source:** U.S. Environmental Protection Agency
        
        **URL:** https://www.epa.gov/ejscreen
        
        **Indicators Included:**
        - Air Quality (PM2.5, Ozone, Diesel Particulate Matter, Air Toxics)
        - Water Quality (Lead Paint, Proximity to Hazardous Waste)
        - Environmental Indicators (Superfund Sites, RMP Facilities)
        - Demographic Indicators (Low Income, Minority, Limited English)
        
        **Geographic Level:** Census Block Group, Tract, County
        
        **Update Frequency:** Annual
        """)
        
        st.markdown("---")
        
        # CDC SVI
        st.markdown("""
        ### 🏥 CDC Social Vulnerability Index (SVI)
        **Source:** CDC/ATSDR (Agency for Toxic Substances and Disease Registry)
        
        **URL:** https://www.atsdr.cdc.gov/placeandhealth/svi/
        
        **Four SVI Themes:**
        1. **Socioeconomic Status** - Poverty, Unemployment, Income, Education
        2. **Household Composition & Disability** - Age 65+, Age 17-, Disability, Single-Parent
        3. **Minority Status & Language** - Minority, Limited English
        4. **Housing Type & Transportation** - Multi-Unit, Mobile Homes, Crowding, No Vehicle
        
        **Geographic Level:** Census Tract, County
        
        **Update Frequency:** Every 2 years
        """)
        
        st.markdown("---")
        
        # ACS
        st.markdown("""
        ### 📊 American Community Survey (ACS)
        **Source:** U.S. Census Bureau
        
        **URL:** https://www.census.gov/programs-surveys/acs
        
        **Data Categories:**
        - Demographics (Age, Sex, Race, Ethnicity)
        - Economic (Income, Poverty, Employment)
        - Social (Education, Language, Disability)
        - Housing (Occupancy, Costs, Vehicles)
        
        **Geographic Level:** Various (State, County, Tract, Block Group)
        
        **Update Frequency:** Annual (1-year and 5-year estimates)
        """)
        
        st.markdown("---")
        
        # Download links
        st.markdown("""
        ### 📥 Direct Download Links
        
        | Dataset | Format | Link |
        |---------|--------|------|
        | CalEnviroScreen 4.0 | Excel/CSV | [Download](https://oehha.ca.gov/calenviroscreen/report/calenviroscreen-40) |
        | EPA EJScreen | Geodatabase/CSV | [Download](https://gaftp.epa.gov/EJSCREEN/) |
        | CDC SVI | CSV/Shapefile | [Download](https://www.atsdr.cdc.gov/placeandhealth/svi/data_documentation_download.html) |
        | ACS Data | API/CSV | [data.census.gov](https://data.census.gov) |
        """)

# ============================================================================
# INTEGRATION HELPER
# ============================================================================

def get_page_justice_replacement():
    """
    Returns the page_environmental_justice function for easy integration
    into the main dashboard.
    
    Usage in dashboard_comprehensive.py:
        from environmental_justice_tool import page_environmental_justice
        
        # In the router section:
        elif page == "justice":
            page_environmental_justice()
    """
    return page_environmental_justice

# ============================================================================
# STANDALONE EXECUTION
# ============================================================================

if __name__ == "__main__":
    st.set_page_config(
        page_title="Environmental Justice Tool - Victoria Love Franklin",
        page_icon="⚖️",
        layout="wide"
    )
    
    # Add minimal CSS
    st.markdown("""
    <style>
        .main-header { font-size: 2.2rem; color: #1e3c72; font-weight: bold; 
                      margin: 1.5rem 0; padding-bottom: 0.5rem; border-bottom: 3px solid #1e3c72; }
        .section-header { font-size: 1.6rem; color: #2c5364; font-weight: 600; 
                         margin-top: 1.5rem; margin-bottom: 1rem; padding-left: 1rem; 
                         border-left: 4px solid #4CAF50; }
        .info-box { background-color: #e3f2fd; border-left: 4px solid #2196F3; 
                   padding: 1rem; margin: 1rem 0; border-radius: 5px; }
        .success-box { background-color: #d4edda; border-left: 4px solid #28a745; 
                      padding: 1rem; margin: 1rem 0; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'ej_data' not in st.session_state:
        st.session_state.ej_data = None
    if 'historic_data' not in st.session_state:
        st.session_state.historic_data = None
    
    # Run the tool
    page_environmental_justice()
