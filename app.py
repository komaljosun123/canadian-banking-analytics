import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
import os

# 1. Page Configuration & Aesthetic Theme Layout
st.set_page_config(layout="wide", page_title="Canadian Banking Analytics Portal", page_icon="🇨🇦")

# Custom CSS Injector for modern webpage layout
st.markdown("""
    <style>
        /* Main Webpage Font Smoothness & Clean Background */
        .main {
            background-color: #FAFAFB;
        }
        /* Gradient Hero Banner */
        .hero-banner {
            background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
            border-radius: 16px;
            color: white;
            margin-top: -40px; /* Pulls the banner flush to the top */
            margin-bottom: 30px;
            box-shadow: 0 10px 25px rgba(30, 58, 138, 0.15);
        }
        /* Luxury Styled Metric Cards */
        .premium-card {
            background-color: #FFFFFF;
            border-top: 4px solid #3B82F6;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
            transition: transform 0.2s ease-in-out;
        }
        .premium-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        }
        .card-label {
            font-size: 13px;
            color: #6B7280;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }
        .card-value {
            font-size: 32px;
            font-weight: 700;
            color: #1F2937;
            margin-top: 8px;
        }
        /* Image Card Container */
        .image-caption-box {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
            border-left: 4px solid #1E3A8A;
        }
    </style>
""", unsafe_allow_html=True)

# 2. Performance Optimized Data Layer with Server-Safe Dynamic Engine
@st.cache_data
def fetch_engineered_dataset():
    target_path = "data/clean_bank_data.csv"
    if os.path.exists(target_path):
        return pd.read_csv(target_path)
    else:
        # Fallback Data Generator Engine if file is missing in Repository
        np.random.seed(42)
        df = pd.DataFrame({
            'person_age': np.random.randint(20, 65, 1000),
            'person_income': np.random.randint(35000, 140000, 1000),
            'loan_amnt': np.random.randint(5000, 42000, 1000),
            'Credit_Score': np.random.randint(500, 850, size=1000),
            'loan_intent': np.random.choice(['PERSONAL', 'EDUCATION', 'MEDICAL', 'VENTURE'], 1000)
        })
        provinces = ['Ontario', 'Quebec', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan']
        weights = [0.40, 0.23, 0.14, 0.11, 0.06, 0.06]
        df['Province'] = np.random.choice(provinces, size=len(df), p=weights)
        
        geo_coords = {
            'Ontario': (43.6532, -79.3832), 'Quebec': (45.5017, -73.5673),
            'British Columbia': (49.2827, -123.1207), 'Alberta': (53.5461, -113.4938),
            'Manitoba': (49.8951, -97.1384), 'Saskatchewan': (52.1332, -106.6700)
        }
        
        df['Latitude'] = df['Province'].map(lambda x: geo_coords[x][0] + np.random.uniform(-0.6, 0.6))
        df['Longitude'] = df['Province'].map(lambda x: geo_coords[x][1] + np.random.uniform(-0.6, 0.6))
        
        def calc_tier(score):
            if score >= 760: return 'Tier 1 - Super Prime'
            elif score >= 680: return 'Tier 2 - Prime'
            elif score >= 600: return 'Tier 3 - Near Prime'
            return 'Tier 4 - Subprime'
        df['Risk_Segment'] = df['Credit_Score'].apply(calc_tier)
        df['DTI_Ratio'] = (df['loan_amnt'] / df['person_income']).round(3)
        return df

df = fetch_engineered_dataset()

# 3. Sidebar Parameter Control Center
st.sidebar.markdown("### 🕹️ Governance Control Center")
st.sidebar.info("Slice and dice the real-time loan book metrics below.")

target_provinces = st.sidebar.multiselect(
    "📍 Select Geographic Scope", 
    options=sorted(df['Province'].unique()), 
    default=df['Province'].unique()
)

target_risk = st.sidebar.multiselect(
    "⚡ Select Underwriting Risk Tiers", 
    options=sorted(df['Risk_Segment'].unique()), 
    default=df['Risk_Segment'].unique()
)

# Compute runtime filtered dataset scoping matrix
filtered_df = df[(df['Province'].isin(target_provinces)) & (df['Risk_Segment'].isin(target_risk))]

# 4. Premium Web App Header with Structural Depth Protection
st.markdown("""
    <div class='hero-banner' style='padding: 40px 30px; min-height: 160px; overflow: hidden; display: block;'>
        <div style='display: inline-block; background-color: rgba(255,255,255,0.18); padding: 6px 14px; border-radius: 20px; font-size: 11px; font-weight: bold; letter-spacing: 1.2px; text-transform: uppercase; margin-bottom: 12px;'>
            Financial Risk Division
        </div>
        <h1 style='color: white; margin: 5px 0; font-size: 34px; font-weight: 800; line-height: 1.2;'>
            Canadian Credit Risk Portfolio Portal
        </h1>
        <p style='color: #E2E8F0; margin: 4px 0 0 0; font-size: 15px; font-weight: 400; opacity: 0.95;'>
            Institutional Asset Underwriting, Exposure Stratification, and Geospatial Mapping Architecture
        </p>
    </div>
""", unsafe_allow_html=True)

# 5. Interactive Tab Navigation System
tab_analytics, tab_market, tab_export = st.tabs(["📊 Executive Dashboard", "🏢 Institutional Context", "📥 Portfolio Export"])

with tab_analytics:
    # 6. Grid Layout for Dynamic KPI Metric Cards
    m1, m2, m3, m4 = st.columns(4)

    st.markdown("<br>", unsafe_allow_html=True)

    # Split-Screen Core Visualizations Layout
    col_left, col_right = st.columns([1.1, 0.9])

    if len(filtered_df) > 0:
        # Calculate metric strings safely
        total_apps = f"{len(filtered_df):,}"
        gross_exposure = f"${int(filtered_df['loan_amnt'].sum()):,}"
        weighted_credit = f"{int(filtered_df['Credit_Score'].mean())}"
        avg_dti = f"{filtered_df['DTI_Ratio'].mean():.1%}"

        # Inject metrics inside modern HTML styled container elements
        m1.markdown(f"<div class='premium-card'><div class='card-label'>Active Pipelines</div><div class='card-value'>{total_apps}</div></div>", unsafe_allow_html=True)
        m2.markdown(f"<div class='premium-card' style='border-top-color: #EF4444;'><div class='card-label' style='color:#EF4444;'>Gross Capital Outlay</div><div class='card-value' style='color:#EF4444;'>{gross_exposure}</div></div>", unsafe_allow_html=True)
        m3.markdown(f"<div class='premium-card' style='border-top-color: #10B981;'><div class='card-label'>Weighted Credit Mean</div><div class='card-value'>{weighted_credit}</div></div>", unsafe_allow_html=True)
        m4.markdown(f"<div class='premium-card'><div class='card-label'>Debt-To-Income (DTI)</div><div class='card-value'>{avg_dti}</div></div>", unsafe_allow_html=True)

        with col_left:
            st.markdown("### 🗺️ Geographic Asset Exposure Concentrations")
            
            # Map values to their two-letter postal code abbreviations
            prov_abbrev = {
                'Ontario': 'ON', 'Quebec': 'QC', 'British Columbia': 'BC',
                'Alberta': 'AB', 'Manitoba': 'MB', 'Saskatchewan': 'SK'
            }
            
            # Generate static centered midpoints and append the new abbrev column
            label_df = filtered_df.groupby('Province')[['Longitude', 'Latitude']].mean().reset_index()
            label_df['Abbrev'] = label_df['Province'].map(prov_abbrev)
            
            grid_layer = pdk.Layer(
                'ScreenGridLayer', 
                data=filtered_df, 
                get_position='[Longitude, Latitude]', 
                cell_size_pixels=22, 
                pickable=True
            )
            
            text_layer = pdk.Layer(
                'TextLayer',
                data=label_df,
                get_position='[Longitude, Latitude]',
                get_text='Abbrev',  # Target the abbreviation string column
                get_color=[30, 58, 138, 255],
                get_size=14,
                get_alignment_baseline='"center"',
                get_text_anchor='"middle"',
                background_color=[255, 255, 255, 220],
                get_border_color=[180, 180, 180, 255],
                get_border_width=1,
                padding=[6, 10, 6, 10],
                billboard=True
            )
            
            st.pydeck_chart(pdk.Deck(
                map_style='road',
                initial_view_state=pdk.ViewState(latitude=53.5, longitude=-97.0, zoom=3.4, pitch=0),
                layers=[grid_layer, text_layer],
            ))

        with col_right:
            st.markdown("### 📈 Exposure Outlay by Capital Allocation Intent")
            intent_alloc = filtered_df.groupby('loan_intent')['loan_amnt'].sum().reset_index()
            st.bar_chart(data=intent_alloc, x='loan_intent', y='loan_amnt', use_container_width=True)
            
            st.markdown("### 📋 Real-Time Risk Register Registry")
            st.dataframe(filtered_df[['Province', 'Risk_Segment', 'Credit_Score', 'loan_amnt', 'DTI_Ratio']].head(6), use_container_width=True)

    else:
        m1.markdown("<div class='premium-card'><div class='card-label'>Active Pipelines</div><div class='card-value'>0</div></div>", unsafe_allow_html=True)
        m2.markdown("<div class='premium-card'><div class='card-label'>Gross Capital Outlay</div><div class='card-value'>$0</div></div>", unsafe_allow_html=True)
        m3.markdown("<div class='premium-card'><div class='card-label'>Weighted Credit Mean</div><div class='card-value'>N/A</div></div>", unsafe_allow_html=True)
