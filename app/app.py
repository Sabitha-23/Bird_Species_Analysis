import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🦅 Bird Species Analysis",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
# GREEN NATURE THEME
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #f0f7f0; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #1b4332 !important;
    }
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    section[data-testid="stSidebar"] .stRadio label {
        color: white !important;
    }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background-color: #d8f3dc;
        border: 1px solid #74c69d;
        border-radius: 10px;
        padding: 15px;
    }
    div[data-testid="metric-container"] label {
        color: #1b4332 !important;
    }

    /* Headers */
    h1, h2, h3 { color: #1b4332 !important; }

    /* Divider */
    hr { border-color: #74c69d; }

    /* Dataframe */
    .stDataFrame { border: 1px solid #74c69d; border-radius: 8px; }

    /* Selectbox label */
    .stSelectbox > label { color: #1b4332 !important; font-weight: bold; }
    .stMultiSelect > label { color: #1b4332 !important; font-weight: bold; }
    .stSlider > label { color: #1b4332 !important; font-weight: bold; }

    /* Success/info boxes */
    .stAlert { border-radius: 8px; }

    /* Page title styling */
    .page-title {
        background: linear-gradient(135deg, #1b4332, #2d6a4f);
        color: white !important;
        padding: 20px 25px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────
COLORS = {
    "Forest"    : "#2d6a4f",
    "Grassland" : "#d4a017",
}
COLOR_SEQ  = ["#1b4332","#2d6a4f","#40916c","#52b788",
               "#74c69d","#95d5b2","#b7e4c7","#d8f3dc"]
MONTH_MAP  = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
               7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
LAYOUT_CFG = dict(
    plot_bgcolor="#f0f7f0",
    paper_bgcolor="#f0f7f0",
    title_font_color="#1b4332",
    title_font_size=15,
    legend_title_font_color="#1b4332",
    font_color="#2c2c2c",
    margin=dict(t=50, b=30, l=20, r=20)
)

def apply_layout(fig):
    fig.update_layout(**LAYOUT_CFG)
    return fig

# ─────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="🌿 Loading bird observation data...")
def load_data():
    url = (
        "https://raw.githubusercontent.com/"
        "Sabitha-23/Bird_Species_Analysis/main/output/cleaned_data.csv"
    )
    df = pd.read_csv(url)
    df["Date"]  = pd.to_datetime(df["Date"], errors="coerce")
    df["Month"] = df["Date"].dt.month
    df["Year"]  = df["Date"].dt.year
    return df

try:
    df = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"❌ Could not load data: {e}")
    st.stop()

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🦅 Bird Species Analysis")
    st.markdown("*US National Parks*")
    st.markdown("---")

    page = st.radio(
        "📌 Navigate to",
        [
            "🏠 Overview",
            "📅 Temporal Analysis",
            "🐦 Species Analysis",
            "🌤️ Environment Analysis",
            "🚨 Conservation",
        ]
    )

    st.markdown("---")
    st.markdown("### 🔍 Global Filters")

    habitats = ["All"] + sorted(df["Habitat"].dropna().unique().tolist())
    sel_habitat = st.selectbox("Habitat", habitats)

    parks = ["All"] + sorted(df["Admin_Unit_Code"].dropna().unique().tolist())
    sel_park = st.selectbox("National Park", parks)

    seasons = ["All"] + sorted(df["Season"].dropna().unique().tolist())
    sel_season = st.selectbox("Season", seasons)

    st.markdown("---")
    st.markdown(
        "<small>📊 Data: US National Parks Bird Monitoring<br>"
        "🔗 github.com/Sabitha-23/Bird_Species_Analysis</small>",
        unsafe_allow_html=True
    )

# ─────────────────────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────────────────────
filtered = df.copy()
if sel_habitat != "All":
    filtered = filtered[filtered["Habitat"] == sel_habitat]
if sel_park != "All":
    filtered = filtered[filtered["Admin_Unit_Code"] == sel_park]
if sel_season != "All":
    filtered = filtered[filtered["Season"] == sel_season]

if len(filtered) == 0:
    st.warning("⚠️ No data matches the selected filters. Please adjust your filters.")
    st.stop()

# ═════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ═════════════════════════════════════════════════════════════
if page == "🏠 Overview":

    st.markdown("""
    <div class="page-title">
        <h1 style="color:white!important;margin:0">🦅 Bird Species Observation Analysis</h1>
        <p style="color:#b7e4c7;margin:5px 0 0 0">
            US National Parks — Forest & Grassland Habitats
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Metrics ──────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("📋 Total Observations",  f"{len(filtered):,}")
    c2.metric("🐦 Unique Species",       f"{filtered['Scientific_Name'].nunique():,}")
    c3.metric("🏞️ National Parks",       f"{filtered['Admin_Unit_Code'].nunique()}")
    c4.metric("🌲 Forest Obs",           f"{len(filtered[filtered['Habitat']=='Forest']):,}")
    c5.metric("🌾 Grassland Obs",        f"{len(filtered[filtered['Habitat']=='Grassland']):,}")

    st.markdown("---")

    # ── Row 1 ─────────────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        park_counts = filtered.groupby(
            ["Admin_Unit_Code","Habitat"]).size().reset_index(name="Count")
        fig = px.bar(
            park_counts, x="Admin_Unit_Code", y="Count", color="Habitat",
            barmode="group",
            title="Observations by National Park",
            labels={"Admin_Unit_Code":"Park","Count":"Observations"},
            color_discrete_map=COLORS, template="plotly_white"
        )
        st.plotly_chart(apply_layout(fig), use_container_width=True)

    with col2:
        hab_counts = filtered.groupby("Habitat").size().reset_index(name="Count")
        fig2 = px.pie(
            hab_counts, names="Habitat", values="Count",
            title="Habitat Distribution",
            color_discrete_map=COLORS, template="plotly_white",
            hole=0.4
        )
        st.plotly_chart(apply_layout(fig2), use_container_width=True)

    # ── Row 2 ─────────────────────────────────────────────────
    col3, col4 = st.columns(2)

    with col3:
        if "Location_Type" in filtered.columns:
            loc = filtered.groupby(
                ["Location_Type","Habitat"]).size().reset_index(name="Count")
            fig3 = px.bar(
                loc, x="Location_Type", y="Count", color="Habitat",
                barmode="group", title="Observations by Location Type",
                color_discrete_map=COLORS, template="plotly_white"
            )
            st.plotly_chart(apply_layout(fig3), use_container_width=True)

    with col4:
        yearly = filtered.groupby(
            ["Year","Habitat"]).size().reset_index(name="Count")
        fig4 = px.line(
            yearly, x="Year", y="Count", color="Habitat", markers=True,
            title="Observations Over the Years",
            color_discrete_map=COLORS, template="plotly_white"
        )
        st.plotly_chart(apply_layout(fig4), use_container_width=True)

    # ── Raw data preview ──────────────────────────────────────
    with st.expander("📋 Preview Raw Data"):
        st.dataframe(filtered.head(50), use_container_width=True)
        st.caption(f"Showing 50 of {len(filtered):,} rows")

# ═════════════════════════════════════════════════════════════
# PAGE 2 — TEMPORAL ANALYSIS
# ═════════════════════════════════════════════════════════════
elif page == "📅 Temporal Analysis":

    st.markdown("""
    <div class="page-title">
        <h1 style="color:white!important;margin:0">📅 Temporal Analysis</h1>
        <p style="color:#b7e4c7;margin:5px 0 0 0">
            Monthly, Seasonal & Yearly Observation Trends
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Monthly
    monthly = filtered.groupby(
        ["Month","Habitat"]).size().reset_index(name="Count")
    fig = px.line(
        monthly, x="Month", y="Count", color="Habitat", markers=True,
        title="Monthly Observation Trends",
        color_discrete_map=COLORS, template="plotly_white"
    )
    fig.update_xaxes(
        tickvals=list(MONTH_MAP.keys()),
        ticktext=list(MONTH_MAP.values())
    )
    st.plotly_chart(apply_layout(fig), use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        seasonal = filtered.groupby(
            ["Season","Habitat"]).size().reset_index(name="Count")
        fig2 = px.bar(
            seasonal, x="Season", y="Count", color="Habitat",
            barmode="group", title="Seasonal Trends",
            color_discrete_map=COLORS, template="plotly_white",
            category_orders={"Season":["Spring","Summer","Fall","Winter"]}
        )
        st.plotly_chart(apply_layout(fig2), use_container_width=True)

    with col2:
        yearly = filtered.groupby(
            ["Year","Habitat"]).size().reset_index(name="Count")
        fig3 = px.bar(
            yearly, x="Year", y="Count", color="Habitat",
            barmode="group", title="Yearly Trends",
            color_discrete_map=COLORS, template="plotly_white"
        )
        st.plotly_chart(apply_layout(fig3), use_container_width=True)

    # Heatmap
    st.markdown("### 🗓️ Observation Heatmap — Park × Month")
    hm_data = filtered.groupby(
        ["Admin_Unit_Code","Month"]).size().reset_index(name="Count")
    hm_pivot = hm_data.pivot(
        index="Admin_Unit_Code", columns="Month", values="Count").fillna(0)
    hm_pivot.columns = [MONTH_MAP[c] for c in hm_pivot.columns]

    fig4 = px.imshow(
        hm_pivot, color_continuous_scale="Greens",
        title="Observation Heatmap (Park × Month)",
        template="plotly_white", text_auto=True
    )
    st.plotly_chart(apply_layout(fig4), use_container_width=True)

# ═════════════════════════════════════════════════════════════
# PAGE 3 — SPECIES ANALYSIS
# ═════════════════════════════════════════════════════════════
elif page == "🐦 Species Analysis":

    st.markdown("""
    <div class="page-title">
        <h1 style="color:white!important;margin:0">🐦 Species Analysis</h1>
        <p style="color:#b7e4c7;margin:5px 0 0 0">
            Species Diversity, Distribution & Identification
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        top_n = st.slider("Show Top N Species", 5, 30, 15)
        top_sp = filtered["Common_Name"].value_counts().head(top_n).reset_index()
        top_sp.columns = ["Species","Count"]
        fig = px.bar(
            top_sp, x="Count", y="Species", orientation="h",
            title=f"Top {top_n} Most Observed Species",
            color="Count", color_continuous_scale="Greens",
            template="plotly_white"
        )
        fig.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(apply_layout(fig), use_container_width=True)

    with col2:
        sp_hab = filtered.groupby(
            "Habitat")["Scientific_Name"].nunique().reset_index()
        sp_hab.columns = ["Habitat","Unique_Species"]
        fig2 = px.pie(
            sp_hab, names="Habitat", values="Unique_Species",
            title="Species Diversity by Habitat",
            color_discrete_map=COLORS, template="plotly_white", hole=0.4
        )
        st.plotly_chart(apply_layout(fig2), use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        sex = filtered.groupby(
            ["Sex","Habitat"]).size().reset_index(name="Count")
        fig3 = px.bar(
            sex, x="Sex", y="Count", color="Habitat", barmode="group",
            title="Sex Distribution of Observed Birds",
            color_discrete_map=COLORS, template="plotly_white"
        )
        st.plotly_chart(apply_layout(fig3), use_container_width=True)

    with col4:
        if "ID_Method" in filtered.columns:
            id_m = filtered.groupby(
                ["ID_Method","Habitat"]).size().reset_index(name="Count")
            fig4 = px.bar(
                id_m, x="ID_Method", y="Count", color="Habitat",
                barmode="group", title="Identification Methods",
                color_discrete_map=COLORS, template="plotly_white"
            )
            st.plotly_chart(apply_layout(fig4), use_container_width=True)

    # Species per park
    st.markdown("### 🏞️ Unique Species per National Park")
    sp_park = filtered.groupby(
        ["Admin_Unit_Code","Habitat"])["Scientific_Name"].nunique().reset_index()
    sp_park.columns = ["Park","Habitat","Unique_Species"]
    fig5 = px.bar(
        sp_park, x="Park", y="Unique_Species", color="Habitat",
        barmode="group", title="Unique Species per National Park",
        color_discrete_map=COLORS, template="plotly_white"
    )
    st.plotly_chart(apply_layout(fig5), use_container_width=True)

    # Flyover
    if "Flyover_Observed" in filtered.columns:
        col5, col6 = st.columns(2)
        with col5:
            fly = filtered["Flyover_Observed"].value_counts().reset_index()
            fly.columns = ["Flyover","Count"]
            fig6 = px.pie(
                fly, names="Flyover", values="Count",
                title="✈️ Flyover vs Stationary",
                color_discrete_sequence=["#2d6a4f","#d4a017"],
                template="plotly_white", hole=0.4
            )
            st.plotly_chart(apply_layout(fig6), use_container_width=True)

# ═════════════════════════════════════════════════════════════
# PAGE 4 — ENVIRONMENT ANALYSIS
# ═════════════════════════════════════════════════════════════
elif page == "🌤️ Environment Analysis":

    st.markdown("""
    <div class="page-title">
        <h1 style="color:white!important;margin:0">🌤️ Environment Analysis</h1>
        <p style="color:#b7e4c7;margin:5px 0 0 0">
            Temperature, Sky, Wind & Disturbance Conditions
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if "Temperature_F" in filtered.columns:
            fig = px.histogram(
                filtered, x="Temperature_F", color="Habitat", nbins=30,
                title="🌡️ Temperature Distribution (°F)",
                color_discrete_map=COLORS, template="plotly_white",
                barmode="overlay", opacity=0.7
            )
            st.plotly_chart(apply_layout(fig), use_container_width=True)

    with col2:
        sky = filtered.groupby(
            ["Sky","Habitat"]).size().reset_index(name="Count")
        fig2 = px.bar(
            sky, x="Sky", y="Count", color="Habitat", barmode="group",
            title="☁️ Sky Conditions",
            color_discrete_map=COLORS, template="plotly_white"
        )
        st.plotly_chart(apply_layout(fig2), use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        wind = filtered.groupby(
            ["Wind","Habitat"]).size().reset_index(name="Count")
        fig3 = px.bar(
            wind, x="Wind", y="Count", color="Habitat", barmode="group",
            title="💨 Wind Conditions",
            color_discrete_map=COLORS, template="plotly_white"
        )
        st.plotly_chart(apply_layout(fig3), use_container_width=True)

    with col4:
        if "Disturbance" in filtered.columns:
            dist = filtered.groupby(
                ["Disturbance","Habitat"]).size().reset_index(name="Count")
            fig4 = px.bar(
                dist, x="Disturbance", y="Count", color="Habitat",
                barmode="group", title="⚠️ Disturbance Levels",
                color_discrete_map=COLORS, template="plotly_white"
            )
            st.plotly_chart(apply_layout(fig4), use_container_width=True)

    # Temperature vs Season
    if "Temperature_F" in filtered.columns:
        st.markdown("### 🌡️ Temperature by Season & Habitat")
        fig5 = px.box(
            filtered, x="Season", y="Temperature_F", color="Habitat",
            title="Temperature Distribution by Season",
            color_discrete_map=COLORS, template="plotly_white",
            category_orders={"Season":["Spring","Summer","Fall","Winter"]}
        )
        st.plotly_chart(apply_layout(fig5), use_container_width=True)

# ═════════════════════════════════════════════════════════════
# PAGE 5 — CONSERVATION
# ═════════════════════════════════════════════════════════════
elif page == "🚨 Conservation":

    st.markdown("""
    <div class="page-title">
        <h1 style="color:white!important;margin:0">🚨 Conservation & Watchlist</h1>
        <p style="color:#b7e4c7;margin:5px 0 0 0">
            Partners in Flight (PIF) Watchlist Species Analysis
        </p>
    </div>
    """, unsafe_allow_html=True)

    if "PIF_Watchlist_Status" in filtered.columns:
        watchlist = filtered[filtered["PIF_Watchlist_Status"] == True]

        if len(watchlist) == 0:
            st.warning("⚠️ No watchlist species found with the current filters.")
        else:
            # KPIs
            c1, c2, c3 = st.columns(3)
            c1.metric("🚨 Watchlist Observations", f"{len(watchlist):,}")
            c2.metric("🐦 Watchlist Species",
                      f"{watchlist['Scientific_Name'].nunique()}")
            c3.metric("📊 % of Total Observations",
                      f"{len(watchlist)/len(filtered)*100:.1f}%")

            st.markdown("---")

            col1, col2 = st.columns(2)

            with col1:
                top_w = watchlist["Common_Name"].value_counts().head(10).reset_index()
                top_w.columns = ["Species","Count"]
                fig = px.bar(
                    top_w, x="Count", y="Species", orientation="h",
                    title="Top 10 Watchlist Species",
                    color="Count", color_continuous_scale="Reds",
                    template="plotly_white"
                )
                fig.update_layout(yaxis=dict(autorange="reversed"))
                st.plotly_chart(apply_layout(fig), use_container_width=True)

            with col2:
                w_hab = watchlist.groupby("Habitat").size().reset_index(name="Count")
                fig2 = px.pie(
                    w_hab, names="Habitat", values="Count",
                    title="Watchlist by Habitat",
                    color_discrete_map=COLORS, template="plotly_white", hole=0.4
                )
                st.plotly_chart(apply_layout(fig2), use_container_width=True)

            # Watchlist by park
            w_park = watchlist.groupby(
                "Admin_Unit_Code").size().reset_index(name="Count")
            fig3 = px.bar(
                w_park, x="Admin_Unit_Code", y="Count",
                title="🏞️ Watchlist Observations by National Park",
                color="Count", color_continuous_scale="Reds",
                template="plotly_white"
            )
            st.plotly_chart(apply_layout(fig3), use_container_width=True)

            col3, col4 = st.columns(2)

            with col3:
                w_season = watchlist.groupby(
                    ["Season","Habitat"]).size().reset_index(name="Count")
                fig4 = px.bar(
                    w_season, x="Season", y="Count", color="Habitat",
                    barmode="group", title="Watchlist by Season",
                    color_discrete_map=COLORS, template="plotly_white",
                    category_orders={"Season":["Spring","Summer","Fall","Winter"]}
                )
                st.plotly_chart(apply_layout(fig4), use_container_width=True)

            with col4:
                w_year = watchlist.groupby(
                    ["Year","Habitat"]).size().reset_index(name="Count")
                fig5 = px.line(
                    w_year, x="Year", y="Count", color="Habitat", markers=True,
                    title="Watchlist Trend Over Years",
                    color_discrete_map=COLORS, template="plotly_white"
                )
                st.plotly_chart(apply_layout(fig5), use_container_width=True)

            # Watchlist species table
            st.markdown("### 📋 Watchlist Species Detail")
            cols_show = ["Common_Name","Scientific_Name",
                         "Admin_Unit_Code","Habitat","Season","Date"]
            cols_show = [c for c in cols_show if c in watchlist.columns]
            st.dataframe(
                watchlist[cols_show].drop_duplicates()
                    .sort_values("Common_Name")
                    .reset_index(drop=True),
                use_container_width=True
            )
    else:
        st.warning("⚠️ PIF_Watchlist_Status column not found in dataset.")
