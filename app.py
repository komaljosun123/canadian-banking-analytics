import streamlit as st
import pandas as pd
import pydeck as pdk

# 1. Page Configuration & Aesthetic Theme Layout
st.set_page_config(layout="wide", page_title="Canadian Banking Analytics Portal", page_icon="🇨🇦")

# Custom CSS Injector for modern webpage layout and UI element masking
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

        /* 🔒 NATIVE INTERFACE STYLING OVERRIDES TO HIDE THE FORK & VIEW SOURCE BUTTONS 🔒 */
        header { 
            display: none !important;
            visibility: hidden !important; 
        }
        
        [data-testid="stStatusWidget"],
        #GithubIcon, 
        .styles_viewerBadge__1yB5_, 
        button[title="Fork this app"],
        a[href*="fork"] { 
            display: none !important; 
            visibility: hidden !important; 
        }
    </style>
""", unsafe_allow_html=True)

# 2. Performance Optimized Production Data Layer
@st.cache_data
def fetch_engineered_dataset():
    try:
        # Attempt to read direct production pathway data
        return pd.read_csv("data/clean_bank_data.csv")
    except FileNotFoundError:
        # Safe structural fallback when file doesn't exist yet
        # Ensures filter drop-downs explicitly support all target choices
        all_provinces = ['ON', 'QC', 'BC', 'AB', 'MB', 'SK', 'NS', 'NB', 'NL', 'PE', 'NT', 'YT', 'NU']
        four_risk_tiers = ['Tier 1', 'Tier 2', 'Tier 3', 'Tier 4']
        
        # Returns an empty dataframe structured with your required categorical defaults
        empty_df = pd.DataFrame(columns=[
            'Province', 'Risk_Segment', 'loan_amnt', 'Credit_Score', 
            'DTI_Ratio', 'Latitude', 'Longitude', 'loan_intent'
        ])
        
        # Inject structural tracking properties so unique selection lookups function cleanly
        empty_df['Province'] = all_provinces + [all_provinces[0]] * (len(four_risk_tiers) - len(all_provinces) if len(four_risk_tiers) > len(all_provinces) else 0)
        empty_df['Risk_Segment'] = four_risk_tiers + [four_risk_tiers[0]] * (len(all_provinces) - len(four_risk_tiers) if len(all_provinces) > len(four_risk_tiers) else 0)
        
        # Truncate mock data records to leave the starting active canvas completely blank
        return empty_df.dropna(subset=['Province', 'Risk_Segment']).iloc[0:0]

df = fetch_engineered_dataset()

# Fixed definitions ensuring proper fallback presentation listing
available_provinces = sorted(df['Province'].unique()) if len(df) > 0 else sorted(['ON', 'QC', 'BC', 'AB', 'MB', 'SK', 'NS', 'NB', 'NL', 'PE', 'NT', 'YT', 'NU'])
available_risks = sorted(df['Risk_Segment'].unique()) if len(df) > 0 else sorted(['Tier 1', 'Tier 2', 'Tier 3', 'Tier 4'])

# 3. Sidebar Parameter Control Center
st.sidebar.markdown("### 🕹️ Governance Control Center")
st.sidebar.info("Slice and dice the real-time loan book metrics below.")

target_provinces = st.sidebar.multiselect(
    "📍 Select Geographic Scope", 
    options=available_provinces, 
    default=available_provinces
)

target_risk = st.sidebar.multiselect(
    "⚡ Select Underwriting Risk Tiers", 
    options=available_risks, 
    default=available_risks
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
        # Calculate metric strings safely from live records
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
            label_anchors = filtered_df.groupby('Province')[['Longitude', 'Latitude']].mean().reset_index()
            label_anchors['Province_Label'] = label_anchors['Province'].astype(str).str.upper()

            st.pydeck_chart(pdk.Deck(
                map_style='dark',
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
        # Clean placeholder cards visible before real file upload occurs
        m1.markdown("<div class='premium-card'><div class='card-label'>Active Pipelines</div><div class='card-value'>0</div></div>", unsafe_allow_html=True)
        m2.markdown("<div class='premium-card' style='border-top-color: #EF4444;'><div class='card-label' style='color:#EF4444;'>Gross Capital Outlay</div><div class='card-value' style='color:#EF4444;'>$0</div></div>", unsafe_allow_html=True)
        m3.markdown("<div class='premium-card' style='border-top-color: #10B981;'><div class='card-label'>Weighted Credit Mean</div><div class='card-value'>N/A</div></div>", unsafe_allow_html=True)
        m4.markdown("<div class='premium-card'><div class='card-label'>Debt-To-Income (DTI)</div><div class='card-value'>0.0%</div></div>", unsafe_allow_html=True)
        
        with col_left:
            st.warning("⚠️ Active geographic parameters empty. Please upload the data matrix to populate layers.")
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
