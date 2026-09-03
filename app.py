import streamlit as st
import pandas as pd
import pydeck as pdk
import os
import numpy as np

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
            margin-top: -40px;
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

# 2. Performance Optimized Data Layer with Classroom Fallback
@st.cache_data
def fetch_engineered_dataset():
    data_path = "data/clean_bank_data.csv"
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    else:
        st.sidebar.warning("⚠️ Local dataset not found. Running on sandbox data.")
        np.random.seed(42)
        provinces = ['ON', 'QC', 'BC', 'AB', 'MB', 'NS']
        risk_tiers = ['Low', 'Medium', 'High']
        intents = ['Mortgage', 'Personal', 'Debt Consolidation', 'Business']
        
        mock_data = pd.DataFrame({
            'Province': np.random.choice(provinces, 200),
            'Risk_Segment': np.random.choice(risk_tiers, 200),
            'loan_amnt': np.random.randint(5000, 50000, 200),
            'Credit_Score': np.random.randint(580, 850, 200),
            'DTI_Ratio': np.random.uniform(0.1, 0.5, 200),
            'loan_intent': np.random.choice(intents, 200),
            'Latitude': np.random.uniform(43.0, 55.0, 200),
            'Longitude': np.random.uniform(-120.0, -70.0, 200)
        })
        return mock_data

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

# 4. Premium Web App Header
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
        gross_exposure = f"${filtered_df['loan_amnt'].sum():,}"
        weighted_credit = f"{int(filtered_df['Credit_Score'].mean())}"
        avg_dti = f"{filtered_df['DTI_Ratio'].mean():.1%}"

        # Inject metrics inside modern HTML styled container elements
        m1.markdown(f"<div class='premium-card'><div class='card-label'>Active Pipelines</div><div class='card-value'>{total_apps}</div></div>", unsafe_allow_html=True)
        m2.markdown(f"<div class='premium-card' style='border-top-color: #EF4444;'><div class='card-label' style='color:#EF4444;'>Gross Capital Outlay</div><div class='card-value' style='color:#EF4444;'>{gross_exposure}</div></div>", unsafe_allow_html=True)
        m3.markdown(f"<div class='premium-card' style='border-top-color: #10B981;'><div class='card-label'>Weighted Credit Mean</div><div class='card-value'>{weighted_credit}</div></div>", unsafe_allow_html=True)
        m4.markdown(f"<div class='premium-card'><div class='card-label'>Debt-To-Income (DTI)</div><div class='card-value'>{avg_dti}</div></div>", unsafe_allow_html=True)

        with col_left:
            st.markdown("### 🗺️ Geographic Asset Exposure Concentrations")
            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/dark-v10',
                initial_view_state=pdk.ViewState(latitude=53.5, longitude=-97.0, zoom=3.4, pitch=38),
                layers=[
                    pdk.Layer(
                        'ScreenGridLayer',
                        data=filtered_df,
                        get_position='[Longitude, Latitude]',
                        cell_size_pixels=22,
                        pickable=True,
                    ),
                ],
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
        m4.markdown("<div class='premium-card'><div class='card-label'>Debt-To-Income (DTI)</div><div class='card-value'>0.0%</div></div>", unsafe_allow_html=True)
        
        with col_left:
            st.warning("⚠️ Active geographic parameters empty. Please select a Province to populate data layers.")
        with col_right:
            st.warning("⚠️ Portfolio stream paused. Restore parameters in control deck to analyze graphs.")

with tab_market:
    st.markdown("### 🏢 Executive Workspace & Market Context")
    st.markdown("Macroeconomic overview matching underwriting parameters.")
    
    img_col1, img_col2 = st.columns(2)
    
    with img_col1:
        st.markdown("""
            <div class='image-caption-box'>
                <div style='background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); height: 120px; border-radius: 8px; margin-bottom: 15px; display: flex; align-items: center; justify-content: center; color: white; font-size: 24px;'>📊 Asset Control</div>
                <h4 style='margin: 0 0 5px 0; color:#1E3A8A; font-size: 18px;'>Asset Refinement Protocols</h4>
                <p style='margin: 0; color: #4B5563; font-size: 14px; line-height: 1.5;'>Commercial portfolio adjustments running in connection with current Bank of Canada credit lending standards.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with img_col2:
        st.markdown("""
            <div class='image-caption-box' style='border-left-color: #EF4444;'>
                <div style='background: linear-gradient(135deg, #7F1D1D 0%, #EF4444 100%); height: 120px; border-radius: 8px; margin-bottom: 15px; display: flex; align-items: center; justify-content: center; color: white; font-size: 24px;'>🛡️ Risk Mitigate</div>
                <h4 style='margin: 0 0 5px 0; color:#EF4444; font-size: 18px;'>Volatility Stress Indexing</h4>
                <p style='margin: 0; color: #4B5563; font-size: 14px; line-height: 1.5;'>Hedges subprime concentration vectors dynamically to insulate capital books from macroeconomic trends.</p>
            </div>
        """, unsafe_allow_html=True)

with tab_export:
