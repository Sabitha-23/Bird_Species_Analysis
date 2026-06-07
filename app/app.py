import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
# THEME — Dark green backgrounds, white text everywhere
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── App background ── */
    .stApp { background-color: #1b4332; }

    /* ── Main content area ── */
    .main .block-container {
        background-color: #1b4332;
        padding-top: 20px;
    }

    /* ── ALL text white ── */
    html, body, [class*="css"], p, span, div, label,
    .stMarkdown, .stText {
        color: #ffffff !important;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background-color: #0d2b1f !important;
        border-right: 2px solid #52b788;
    }
    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] .stRadio > label {
        color: #b7e4c7 !important;
        font-weight: bold;
        font-size: 14px;
    }
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        color: #ffffff !important;
        font-size: 15px;
        padding: 4px 0;
    }
    section[data-testid="stSidebar"] .stSelectbox label {
        color: #b7e4c7 !important;
        font-weight: bold;
    }

    /* ── Dropdown box (closed state) ── */
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
        background-color: #ffffff !important;
        border: 2px solid #52b788 !important;
        border-radius: 6px;
    }

    /* ── Selected value text in the box ── */
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div[class*="ValueContainer"] *,
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div[class*="singleValue"],
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] input {
        color: #000000 !important;
        background-color: #ffffff !important;
    }

    /* ── Dropdown arrow icon ── */
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] svg {
        fill: #1b4332 !important;
    }

    /* ── Dropdown open list/menu ── */
    div[data-baseweb="popover"] ul,
    div[data-baseweb="popover"] [role="listbox"],
    div[data-baseweb="menu"] {
        background-color: #ffffff !important;
        border: 2px solid #52b788 !important;
        border-radius: 8px !important;
    }

    /* ── Dropdown option text ── */
    div[data-baseweb="popover"] li,
    div[data-baseweb="popover"] [role="option"],
    div[data-baseweb="menu"] li {
        color: #000000 !important;
        background-color: #ffffff !important;
        font-size: 14px !important;
    }

    /* ── Hovered option ── */
    div[data-baseweb="popover"] li:hover,
    div[data-baseweb="popover"] [role="option"]:hover,
    div[data-baseweb="menu"] li:hover {
        background-color: #d8f3dc !important;
        color: #1b4332 !important;
    }

    /* ── Selected option in list ── */
    div[data-baseweb="popover"] [aria-selected="true"],
    div[data-baseweb="menu"] [aria-selected="true"] {
        background-color: #52b788 !important;
        color: #ffffff !important;
    }

    /* ── Typing/search input inside dropdown ── */
    div[data-baseweb="popover"] input,
    div[data-baseweb="select"] input {
        color: #000000 !important;
        background-color: #ffffff !important;
        caret-color: #1b4332 !important;
    }

    /* ── Metric cards ── */
    div[data-testid="metric-container"] {
        background-color: #2d6a4f !important;
        border: 2px solid #52b788 !important;
        border-radius: 12px !important;
        padding: 18px !important;
    }
    div[data-testid="metric-container"] label {
        color: #b7e4c7 !important;
        font-size: 13px !important;
        font-weight: bold !important;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 28px !important;
        font-weight: bold !important;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricDelta"] {
        color: #95d5b2 !important;
    }

    /* ── Headers ── */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: bold !important;
    }

    /* ── Page title banner ── */
    .page-title {
        background: linear-gradient(135deg, #0d2b1f, #2d6a4f);
        border: 2px solid #52b788;
        border-radius: 12px;
        padding: 22px 28px;
        margin-bottom: 25px;
    }
    .page-title h1 {
        color: #ffffff !important;
        margin: 0 !important;
        font-size: 28px !important;
    }
    .page-title p {
        color: #95d5b2 !important;
        margin: 6px 0 0 0 !important;
        font-size: 15px !important;
    }

    /* ── Section headers ── */
    .section-header {
        background-color: #2d6a4f;
        border-left: 5px solid #95d5b2;
        border-radius: 6px;
        padding: 10px 16px;
        margin: 20px 0 12px 0;
        color: #ffffff !important;
        font-weight: bold;
        font-size: 17px;
    }

    /* ── Divider ── */
    hr { border-color: #52b788 !important; }

    /* ── Slider ── */
    .stSlider label { color: #b7e4c7 !important; font-weight: bold !important; }
    .stSlider .st-emotion-cache-1xw8zd0 { color: #ffffff !important; }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background-color: #2d6a4f !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    .streamlit-expanderContent {
        background-color: #1b4332 !important;
        border: 1px solid #52b788 !important;
    }

    /* ── Dataframe ── */
    .stDataFrame {
        border: 2px solid #52b788 !important;
        border-radius: 8px !important;
    }
    .stDataFrame th {
        background-color: #2d6a4f !important;
        color: #ffffff !important;
    }
    .stDataFrame td {
        color: #ffffff !important;
        background-color: #1b4332 !important;
    }

    /* ── Warning / info alerts ── */
    .stAlert {
        border-radius: 8px !important;
        background-color: #2d6a4f !important;
        color: #ffffff !important;
    }

    /* ── Tabs (if used) ── */
    .stTabs [data-baseweb="tab"] {
        color: #b7e4c7 !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #ffffff !important;
        border-bottom: 3px solid #52b788 !important;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────
COLORS    = {"Forest": "#52b788", "Grassland": "#f4a261"}
COLOR_SEQ = ["#52b788","#40916c","#2d6a4f","#74c69d",
             "#f4a261","#e76f51","#95d5b2","#b7e4c7"]
MONTH_MAP = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
             7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}

LAYOUT_CFG = dict(
    plot_bgcolor="#2d6a4f",
    paper_bgcolor="#1b4332",
    font_color="#ffffff",
    title_font_color="#ffffff",
    title_font_size=16,
    legend_bgcolor="#2d6a4f",
    legend_bordercolor="#52b788",
    legend_borderwidth=1,
    legend_font_color="#ffffff",
    coloraxis_colorbar_tickfont_color="#ffffff",
    coloraxis_colorbar_title_font_color="#ffffff",
    margin=dict(t=55, b=35, l=20, r=20),
    xaxis=dict(
        gridcolor="#40916c",
        linecolor="#52b788",
        tickfont_color="#ffffff",
        title_font_color="#ffffff",
        zerolinecolor="#40916c"
    ),
    yaxis=dict(
        gridcolor="#40916c",
        linecolor="#52b788",
        tickfont_color="#ffffff",
        title_font_color="#ffffff",
        zerolinecolor="#40916c"
    )
)

def show(fig):
    """Apply dark theme layout and render chart."""
    fig.update_layout(**LAYOUT_CFG)
    # Fix colorbar text for continuous color scales
    fig.update_coloraxes(
        colorbar_tickfont_color="#ffffff",
        colorbar_title_font_color="#ffffff"
    )
    st.plotly_chart(fig, use_container_width=True)

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
except Exception as e:
    st.error(f"❌ Could not load data: {e}")
    st.stop()

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🦅 Bird Species Analysis")
    st.markdown("**US National Parks**")
    st.markdown("*Forest & Grassland Habitats*")
    st.markdown("---")

    page = st.radio(
        "📌 Navigate",
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
        "📊 **Data:** US National Parks  \n"
        "🔗 [GitHub Repo](https://github.com/Sabitha-23/Bird_Species_Analysis)"
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
    st.warning("⚠️ No data matches the selected filters. Please adjust.")
    st.stop()

# ═════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ═════════════════════════════════════════════════════════════
if page == "🏠 Overview":

    st.markdown("""
    <div class="page-title">
        <h1>🦅 Bird Species Observation Analysis</h1>
        <p>US National Parks — Forest & Grassland Habitats</p>
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("📋 Total Observations",  f"{len(filtered):,}")
    c2.metric("🐦 Unique Species",       f"{filtered['Scientific_Name'].nunique():,}")
    c3.metric("🏞️ National Parks",       f"{filtered['Admin_Unit_Code'].nunique()}")
    c4.metric("🌲 Forest Obs",           f"{len(filtered[filtered['Habitat']=='Forest']):,}")
    c5.metric("🌾 Grassland Obs",        f"{len(filtered[filtered['Habitat']=='Grassland']):,}")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        park_counts = filtered.groupby(
            ["Admin_Unit_Code","Habitat"]).size().reset_index(name="Count")
        fig = px.bar(
            park_counts, x="Admin_Unit_Code", y="Count", color="Habitat",
            barmode="group",
            title="Observations by National Park",
            labels={"Admin_Unit_Code":"Park","Count":"Observations"},
            color_discrete_map=COLORS, template="plotly_dark"
        )
        show(fig)

    with col2:
        hab_counts = filtered.groupby("Habitat").size().reset_index(name="Count")
        fig2 = px.pie(
            hab_counts, names="Habitat", values="Count",
            title="Habitat Distribution",
            color_discrete_map=COLORS, template="plotly_dark", hole=0.45
        )
        show(fig2)

    col3, col4 = st.columns(2)
    with col3:
        if "Location_Type" in filtered.columns:
            loc = filtered.groupby(
                ["Location_Type","Habitat"]).size().reset_index(name="Count")
            fig3 = px.bar(
                loc, x="Location_Type", y="Count", color="Habitat",
                barmode="group", title="Observations by Location Type",
                color_discrete_map=COLORS, template="plotly_dark"
            )
            show(fig3)

    with col4:
        yearly = filtered.groupby(
            ["Year","Habitat"]).size().reset_index(name="Count")
        fig4 = px.line(
            yearly, x="Year", y="Count", color="Habitat", markers=True,
            title="Observations Over the Years",
            color_discrete_map=COLORS, template="plotly_dark"
        )
        show(fig4)

    with st.expander("📋 Preview Raw Data"):
        st.dataframe(filtered.head(50), use_container_width=True)
        st.caption(f"Showing 50 of {len(filtered):,} rows")

# ═════════════════════════════════════════════════════════════
# PAGE 2 — TEMPORAL ANALYSIS
# ═════════════════════════════════════════════════════════════
elif page == "📅 Temporal Analysis":

    st.markdown("""
    <div class="page-title">
        <h1>📅 Temporal Analysis</h1>
        <p>Monthly, Seasonal & Yearly Observation Trends</p>
    </div>
    """, unsafe_allow_html=True)

    monthly = filtered.groupby(
        ["Month","Habitat"]).size().reset_index(name="Count")
    fig = px.line(
        monthly, x="Month", y="Count", color="Habitat", markers=True,
        title="Monthly Observation Trends",
        color_discrete_map=COLORS, template="plotly_dark"
    )
    fig.update_xaxes(
        tickvals=list(MONTH_MAP.keys()),
        ticktext=list(MONTH_MAP.values())
    )
    show(fig)

    col1, col2 = st.columns(2)
    with col1:
        seasonal = filtered.groupby(
            ["Season","Habitat"]).size().reset_index(name="Count")
        fig2 = px.bar(
            seasonal, x="Season", y="Count", color="Habitat",
            barmode="group", title="Seasonal Trends",
            color_discrete_map=COLORS, template="plotly_dark",
            category_orders={"Season":["Spring","Summer","Fall","Winter"]}
        )
        show(fig2)

    with col2:
        yearly = filtered.groupby(
            ["Year","Habitat"]).size().reset_index(name="Count")
        fig3 = px.bar(
            yearly, x="Year", y="Count", color="Habitat",
            barmode="group", title="Yearly Trends",
            color_discrete_map=COLORS, template="plotly_dark"
        )
        show(fig3)

    st.markdown('<div class="section-header">🗓️ Observation Heatmap — Park × Month</div>',
                unsafe_allow_html=True)
    hm_data = filtered.groupby(
        ["Admin_Unit_Code","Month"]).size().reset_index(name="Count")
    hm_pivot = hm_data.pivot(
        index="Admin_Unit_Code", columns="Month", values="Count").fillna(0)
    hm_pivot.columns = [MONTH_MAP[c] for c in hm_pivot.columns]

    fig4 = px.imshow(
        hm_pivot, color_continuous_scale="Greens",
        title="Observation Heatmap (Park × Month)",
        template="plotly_dark", text_auto=True
    )
    fig4.update_traces(textfont_color="#ffffff")
    show(fig4)

# ═════════════════════════════════════════════════════════════
# PAGE 3 — SPECIES ANALYSIS
# ═════════════════════════════════════════════════════════════
elif page == "🐦 Species Analysis":

    st.markdown("""
    <div class="page-title">
        <h1>🐦 Species Analysis</h1>
        <p>Species Diversity, Distribution & Identification</p>
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
            template="plotly_dark"
        )
        fig.update_layout(yaxis=dict(autorange="reversed"))
        show(fig)

    with col2:
        sp_hab = filtered.groupby(
            "Habitat")["Scientific_Name"].nunique().reset_index()
        sp_hab.columns = ["Habitat","Unique_Species"]
        fig2 = px.pie(
            sp_hab, names="Habitat", values="Unique_Species",
            title="Species Diversity by Habitat",
            color_discrete_map=COLORS, template="plotly_dark", hole=0.45
        )
        show(fig2)

    col3, col4 = st.columns(2)
    with col3:
        sex = filtered.groupby(
            ["Sex","Habitat"]).size().reset_index(name="Count")
        fig3 = px.bar(
            sex, x="Sex", y="Count", color="Habitat", barmode="group",
            title="Sex Distribution of Observed Birds",
            color_discrete_map=COLORS, template="plotly_dark"
        )
        show(fig3)

    with col4:
        if "ID_Method" in filtered.columns:
            id_m = filtered.groupby(
                ["ID_Method","Habitat"]).size().reset_index(name="Count")
            fig4 = px.bar(
                id_m, x="ID_Method", y="Count", color="Habitat",
                barmode="group", title="Identification Methods",
                color_discrete_map=COLORS, template="plotly_dark"
            )
            show(fig4)

    st.markdown('<div class="section-header">🏞️ Unique Species per National Park</div>',
                unsafe_allow_html=True)
    sp_park = filtered.groupby(
        ["Admin_Unit_Code","Habitat"])["Scientific_Name"].nunique().reset_index()
    sp_park.columns = ["Park","Habitat","Unique_Species"]
    fig5 = px.bar(
        sp_park, x="Park", y="Unique_Species", color="Habitat",
        barmode="group", title="Unique Species per National Park",
        color_discrete_map=COLORS, template="plotly_dark"
    )
    show(fig5)

    if "Flyover_Observed" in filtered.columns:
        col5, col6 = st.columns(2)
        with col5:
            fly = filtered["Flyover_Observed"].value_counts().reset_index()
            fly.columns = ["Flyover","Count"]
            fig6 = px.pie(
                fly, names="Flyover", values="Count",
                title="✈️ Flyover vs Stationary",
                color_discrete_sequence=["#52b788","#f4a261"],
                template="plotly_dark", hole=0.45
            )
            show(fig6)

# ═════════════════════════════════════════════════════════════
# PAGE 4 — ENVIRONMENT ANALYSIS
# ═════════════════════════════════════════════════════════════
elif page == "🌤️ Environment Analysis":

    st.markdown("""
    <div class="page-title">
        <h1>🌤️ Environment Analysis</h1>
        <p>Temperature, Sky, Wind & Disturbance Conditions</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if "Temperature_F" in filtered.columns:
            fig = px.histogram(
                filtered, x="Temperature_F", color="Habitat", nbins=30,
                title="🌡️ Temperature Distribution (°F)",
                color_discrete_map=COLORS, template="plotly_dark",
                barmode="overlay", opacity=0.75
            )
            show(fig)

    with col2:
        sky = filtered.groupby(
            ["Sky","Habitat"]).size().reset_index(name="Count")
        fig2 = px.bar(
            sky, x="Sky", y="Count", color="Habitat", barmode="group",
            title="☁️ Sky Conditions",
            color_discrete_map=COLORS, template="plotly_dark"
        )
        show(fig2)

    col3, col4 = st.columns(2)
    with col3:
        wind = filtered.groupby(
            ["Wind","Habitat"]).size().reset_index(name="Count")
        fig3 = px.bar(
            wind, x="Wind", y="Count", color="Habitat", barmode="group",
            title="💨 Wind Conditions",
            color_discrete_map=COLORS, template="plotly_dark"
        )
        show(fig3)

    with col4:
        if "Disturbance" in filtered.columns:
            dist = filtered.groupby(
                ["Disturbance","Habitat"]).size().reset_index(name="Count")
            fig4 = px.bar(
                dist, x="Disturbance", y="Count", color="Habitat",
                barmode="group", title="⚠️ Disturbance Levels",
                color_discrete_map=COLORS, template="plotly_dark"
            )
            show(fig4)

    if "Temperature_F" in filtered.columns:
        st.markdown('<div class="section-header">🌡️ Temperature by Season & Habitat</div>',
                    unsafe_allow_html=True)
        fig5 = px.box(
            filtered, x="Season", y="Temperature_F", color="Habitat",
            title="Temperature Distribution by Season",
            color_discrete_map=COLORS, template="plotly_dark",
            category_orders={"Season":["Spring","Summer","Fall","Winter"]}
        )
        show(fig5)

# ═════════════════════════════════════════════════════════════
# PAGE 5 — CONSERVATION
# ═════════════════════════════════════════════════════════════
elif page == "🚨 Conservation":

    st.markdown("""
    <div class="page-title">
        <h1>🚨 Conservation & Watchlist</h1>
        <p>Partners in Flight (PIF) Watchlist Species Analysis</p>
    </div>
    """, unsafe_allow_html=True)

    if "PIF_Watchlist_Status" in filtered.columns:
        watchlist = filtered[filtered["PIF_Watchlist_Status"] == True]

        if len(watchlist) == 0:
            st.warning("⚠️ No watchlist species found with current filters.")
        else:
            c1, c2, c3 = st.columns(3)
            c1.metric("🚨 Watchlist Observations", f"{len(watchlist):,}")
            c2.metric("🐦 Watchlist Species",
                      f"{watchlist['Scientific_Name'].nunique()}")
            c3.metric("📊 % of Total",
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
                    template="plotly_dark"
                )
                fig.update_layout(yaxis=dict(autorange="reversed"))
                show(fig)

            with col2:
                w_hab = watchlist.groupby(
                    "Habitat").size().reset_index(name="Count")
                fig2 = px.pie(
                    w_hab, names="Habitat", values="Count",
                    title="Watchlist by Habitat",
                    color_discrete_map=COLORS,
                    template="plotly_dark", hole=0.45
                )
                show(fig2)

            w_park = watchlist.groupby(
                "Admin_Unit_Code").size().reset_index(name="Count")
            fig3 = px.bar(
                w_park, x="Admin_Unit_Code", y="Count",
                title="🏞️ Watchlist Observations by National Park",
                color="Count", color_continuous_scale="Reds",
                template="plotly_dark"
            )
            show(fig3)

            col3, col4 = st.columns(2)
            with col3:
                w_season = watchlist.groupby(
                    ["Season","Habitat"]).size().reset_index(name="Count")
                fig4 = px.bar(
                    w_season, x="Season", y="Count", color="Habitat",
                    barmode="group", title="Watchlist by Season",
                    color_discrete_map=COLORS, template="plotly_dark",
                    category_orders={"Season":["Spring","Summer","Fall","Winter"]}
                )
                show(fig4)

            with col4:
                w_year = watchlist.groupby(
                    ["Year","Habitat"]).size().reset_index(name="Count")
                fig5 = px.line(
                    w_year, x="Year", y="Count", color="Habitat",
                    markers=True, title="Watchlist Trend Over Years",
                    color_discrete_map=COLORS, template="plotly_dark"
                )
                show(fig5)

            st.markdown('<div class="section-header">📋 Watchlist Species Detail</div>',
                        unsafe_allow_html=True)
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
