import streamlit as st
import pandas as pd
import pydeck as pdk

# 1. Page Configuration & Aesthetic Theme Layout
st.set_page_config(layout="wide", page_title="Canadian Banking Analytics Portal", page_icon="🇨🇦")

# Custom CSS Injector for modern webpage layout
st.markdown("""
    <style>
        .main { background-color: #FAFAFB; }
        .premium-card {
            background-color: #FFFFFF;
            border-top: 4px solid #3B82F6;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
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
    </style>
""", unsafe_allow_html=True)

# 2. Performance Optimized Data Layer
@st.cache_data
def fetch_engineered_dataset():
    # Fallback to dummy data generation if the file isn't found locally
    try:
        return pd.read_csv("data/clean_bank_data.csv")
    except FileNotFoundError:
        import numpy as np
        return pd.DataFrame({
            'Province': np.random.choice(['ON', 'BC', 'AB', 'QC'], 100),
            'Risk_Segment': np.random.choice(['Low', 'Medium', 'High'], 100),
            'loan_amnt': np.random.randint(10000, 50000, 100),
            'Credit_Score': np.random.randint(600, 850, 100),
            'DTI_Ratio': np.random.uniform(0.1, 0.5, 100),
            'Latitude': np.random.uniform(49.0, 55.0, 100),
            'Longitude': np.random.uniform(-125.0, -70.0, 100),
            'loan_intent': np.random.choice(['PERSONAL', 'EDUCATION', 'MEDICAL', 'VENTURE'], 100)
        })

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

# 4. Premium Web App Header using native elements to completely avoid syntax crashes
st.title("🇨🇦 Canadian Credit Risk Portfolio Portal")
st.caption("Financial Risk Division — Institutional Asset Underwriting, Exposure Stratification, and Geospatial Mapping Architecture")
st.divider()

# 5. Interactive Tab Navigation System
tab_analytics, tab_market, tab_export = st.tabs(["📊 Executive Dashboard", "🏢 Institutional Context", "📥 Portfolio Export"])

with tab_analytics:
    # Grid Layout for Dynamic KPI Metric Cards
    m1, m2, m3, m4 = st.columns(4)

    # Split-Screen Core Visualizations Layout
    col_left, col_right = st.columns([1.1, 0.9])

    if len(filtered_df) > 0:
        # Calculate metric strings safely
        total_apps = f"{len(filtered_df):,}"
        gross_exposure = f"${filtered_df['loan_amnt'].sum():,}"
        weighted_credit = f"{int(filtered_df['Credit_Score'].mean())}"
        avg_dti = f"{filtered_df['DTI_Ratio'].mean():.1%}"

        # Inject metrics using safe custom layout styles
        m1.markdown(f"<div class='premium-card'><div class='card-label'>Active Pipelines</div><div class='card-value'>{total_apps}</div></div>", unsafe_allow_html=True)
        m2.markdown(f"<div class='premium-card' style='border-top-color: #EF4444;'><div class='card-label' style='color:#EF4444;'>Gross Capital Outlay</div><div class='card-value' style='color:#EF4444;'>{gross_exposure}</div></div>", unsafe_allow_html=True)
        m3.markdown(f"<div class='premium-card' style='border-top-color: #10B981;'><div class='card-label'>Weighted Credit Mean</div><div class='card-value'>{weighted_credit}</div></div>", unsafe_allow_html=True)
        m4.markdown(f"<div class='premium-card'><div class='card-label'>Debt-To-Income (DTI)</div><div class='card-value'>{avg_dti}</div></div>", unsafe_allow_html=True)

        with col_left:
            st.markdown("### 🗺️ Geographic Asset Exposure Concentrations")
            
            # Generate aggregate coordinates for map labels
            label_anchors = filtered_df.groupby('Province')[['Longitude', 'Latitude']].mean().reset_index()
            label_anchors['Province_Label'] = label_anchors['Province'].astype(str).str.upper()

            # Clean Pydeck Map rendering with explicit data text-layers
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
                    pdk.Layer(
                        'TextLayer',
                        data=label_anchors,
                        get_position='[Longitude, Latitude]',
                        get_text='Province_Label',
                        get_size=18,
                        get_color=[255, 255, 255, 230],
                        get_alignment_baseline='"center"',
                        get_text_anchor='"middle"',
                        billboard=True
                    )
                ],
            ))

        with col_right:
            st.markdown("### 📈 Exposure Outlay by Capital Allocation Intent")
            intent_alloc = filtered_df.groupby('loan_intent')['loan_amnt'].sum().reset_index()
            st.bar_chart(data=intent_alloc, x='loan_intent', y='loan_amnt', use_container_width=True)
            
            st.markdown("### 📋 Real-Time Risk Register Registry")
            st.dataframe(filtered_df[['Province', 'Risk_Segment', 'Credit_Score', 'loan_amnt', 'DTI_Ratio']].head(6), use_container_width=True)

    else:
        m1.metric("Active Pipelines", "0")
        m2.metric("Gross Capital Outlay", "$0")
        m3.metric("Weighted Credit Mean", "N/A")
        m4.metric("Debt-To-Income (DTI)", "0.0%")
        
        with col_left:
            st.warning("⚠️ Active geographic parameters empty. Please select a Province to populate data layers.")
        with col_right:
            st.warning("⚠️ Portfolio stream paused. Restore parameters in control deck to analyze graphs.")

with tab_market:
    st.markdown("### 🏢 Executive Workspace & Market Context")
    st.markdown("Macroeconomic overview matching underwriting parameters.")
    
    img_col1, img_col2 = st.columns(2)
    
    with img_col1:
        st.info("### 📊 Asset Control\n\n**Asset Refinement Protocols**\n\nCommercial portfolio adjustments running in connection with current Bank of Canada credit lending standards.")
        
    with img_col2:
        st.error("### 🛡️ Risk Mitigate\n\n**Volatility Stress Indexing**\n\nHedges subprime concentration vectors dynamically to insulate capital books from macroeconomic trends.")

with tab_export:
    st.markdown("### 📥 Archive & Export Portal")
    st.markdown("Extract current filtered states as structured compliance audit assets.")
    
    csv_buffer = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Structured Risk Portfolio State (CSV)",
        data=csv_buffer,
        file_name="filtered_canadian_banking_manifest.csv",
        mime="text/csv"
    )
