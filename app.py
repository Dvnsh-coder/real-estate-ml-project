from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Real Estate Buyer Intelligence",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. BUYER SEGMENT NAMES
# ============================================================

CLUSTER_NAMES = {
    0: "Agency Home Buyers",
    1: "Website-Financed Home Buyers",
    2: "Higher-Value Home Buyers",
    3: "Mixed-Purpose Client-Referred Buyers",
    4: "Agency Investment Buyers",
    5: "Website Investment Buyers",
    6: "Financed Investment Buyers",
    7: "Older Active Home Buyers",
    8: "Agency-Financed Home Buyers",
    9: "High-Activity Property Buyers",
}


# ============================================================
# 3. COUNTRY ISO CODES FOR MAP
# ============================================================

COUNTRY_ISO_CODES = {
    "USA": "USA",
    "Canada": "CAN",
    "UK": "GBR",
    "Australia": "AUS",
    "Germany": "DEU",
    "France": "FRA",
    "Belgium": "BEL",
    "Mexico": "MEX",
    "Russia": "RUS",
    "Denmark": "DNK",
}


# ============================================================
# 4. LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    data_path = (
        Path(__file__).resolve().parent
        / "data"
        / "dashboard_data.csv"
    )

    if not data_path.exists():
        return None

    df = pd.read_csv(data_path)

    df["segment_name"] = df["cluster"].map(
        CLUSTER_NAMES
    )

    # Avoid blank segment labels if an unexpected cluster appears
    df["segment_name"] = df["segment_name"].fillna(
        "Cluster " + df["cluster"].astype(str)
    )

    return df


dashboard_df = load_data()


if dashboard_df is None:

    st.error(
        "⚠️ Dataset not found at "
        "`data/dashboard_data.csv`. "
        "Please ensure the file path is correct."
    )

    st.stop()


# ============================================================
# 5. HELPER FUNCTIONS
# ============================================================

def format_currency(value):

    return f"${value:,.0f}"


def format_percentage(value):

    return f"{value:.1f}%"


def create_plotly_layout(fig, height=430):

    """
    Apply consistent chart spacing while allowing
    Streamlit to control Light/Dark Mode colors.
    """

    fig.update_layout(

        height=height,

        margin=dict(
            l=15,
            r=45,
            t=75,
            b=35,
        ),

        font=dict(
            family="Arial",
            size=13,
        ),

        hoverlabel=dict(
            font_size=13,
        ),
    )

    fig.update_xaxes(
        automargin=True,
        zeroline=False,
    )

    fig.update_yaxes(
        automargin=True,
        zeroline=False,
    )

    return fig


def show_chart(fig):

    """
    Render charts using Streamlit's active theme.
    """

    st.plotly_chart(
        fig,
        use_container_width=True,
        theme="streamlit",
    )


def horizontal_bar_chart(
    data,
    x,
    y,
    title,
    height=450,
    currency=False,
    decimals=0,
):

    """
    Create a horizontal chart with readable category labels.
    """

    chart_df = data.sort_values(
        x,
        ascending=True,
    )

    fig = px.bar(

        chart_df,

        x=x,

        y=y,

        orientation="h",

        text=x,

        title=title,
    )

    fig.update_traces(

        texttemplate=f"%{{x:,.{decimals}f}}",

        textposition="outside",

        cliponaxis=False,
    )

    fig.update_yaxes(

        title=None,

        categoryorder="array",

        categoryarray=chart_df[y].tolist(),
    )

    fig.update_xaxes(
        title=None,
    )

    if currency:

        fig.update_xaxes(
            tickprefix="$",
        )

        fig.update_traces(
            hovertemplate=(
                "%{y}<br>"
                "Value: $%{x:,.0f}"
                "<extra></extra>"
            )
        )

    fig = create_plotly_layout(
        fig,
        height=height,
    )

    show_chart(fig)


def categorical_bar_chart(
    data,
    x,
    y,
    title,
):

    fig = px.bar(

        data,

        x=x,

        y=y,

        text=y,

        title=title,
    )

    fig.update_traces(

        textposition="outside",

        cliponaxis=False,
    )

    fig.update_xaxes(
        title=None,
    )

    fig.update_yaxes(
        title="Clients",
    )

    fig = create_plotly_layout(
        fig,
        height=370,
    )

    show_chart(fig)


# ============================================================
# 6. CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 1.6rem;
        padding-bottom: 2rem;
    }

    h1 {
        letter-spacing: -0.035em;
    }

    h2,
    h3 {
        letter-spacing: -0.02em;
    }

    div[data-testid="stMetric"] {
        padding: 16px;
        border: 1px solid rgba(128, 128, 128, 0.22);
        border-radius: 12px;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 14px;
    }

    div[data-testid="stMetricValue"] {
        font-weight: 700;
    }

    div[data-testid="stTabs"] {
        margin-top: 12px;
    }

    div[data-testid="stPlotlyChart"] {
        border: 1px solid rgba(128, 128, 128, 0.15);
        border-radius: 12px;
        padding: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 7. HEADER
# ============================================================

st.title(
    "🏠 Real Estate Buyer Intelligence"
)

st.markdown(
    """
    **Machine Learning Based Buyer Segmentation & Investment Profiling**

    Explore buyer segments, investment behavior, financing patterns,
    property activity, and geographic characteristics.
    """
)


# ============================================================
# 8. SIDEBAR FILTERS
# ============================================================

st.sidebar.title(
    "🔎 Dashboard Filters"
)

st.sidebar.caption(
    "Explore specific buyer groups using the filters below."
)


# ============================================================
# RESET FILTERS
# ============================================================

if st.sidebar.button(
    "🔄 Reset All Filters",
    use_container_width=True,
):

    for key in [
        "country_filter",
        "region_filter",
        "purpose_filter",
        "client_type_filter",
    ]:

        if key in st.session_state:
            del st.session_state[key]

    st.rerun()


# ============================================================
# COUNTRY FILTER
# ============================================================

country_options = sorted(
    dashboard_df[
        "country"
    ]
    .dropna()
    .unique()
    .tolist()
)

country_filter = st.sidebar.multiselect(

    "🌎 Country",

    options=country_options,

    placeholder="All countries",

    key="country_filter",
)


# ============================================================
# DYNAMIC REGION OPTIONS
# ============================================================

if country_filter:

    region_source = dashboard_df[
        dashboard_df["country"].isin(
            country_filter
        )
    ]

else:

    region_source = dashboard_df


region_options = sorted(
    region_source[
        "region"
    ]
    .dropna()
    .unique()
    .tolist()
)


# ============================================================
# CLEAR INVALID REGION SELECTIONS
# ============================================================

if "region_filter" not in st.session_state:

    st.session_state[
        "region_filter"
    ] = []


st.session_state[
    "region_filter"
] = [

    region

    for region
    in st.session_state[
        "region_filter"
    ]

    if region in region_options
]


region_filter = st.sidebar.multiselect(

    "📍 Region",

    options=region_options,

    placeholder="All regions",

    key="region_filter",
)


# ============================================================
# ACQUISITION PURPOSE FILTER
# ============================================================

purpose_options = sorted(

    dashboard_df[
        "acquisition_purpose"
    ]
    .dropna()
    .unique()
    .tolist()
)


purpose_filter = st.sidebar.multiselect(

    "🎯 Acquisition Purpose",

    options=purpose_options,

    placeholder="All purposes",

    key="purpose_filter",
)


# ============================================================
# CLIENT TYPE FILTER
# ============================================================

client_type_options = sorted(

    dashboard_df[
        "client_type"
    ]
    .dropna()
    .unique()
    .tolist()
)


client_type_filter = st.sidebar.multiselect(

    "👤 Client Type",

    options=client_type_options,

    placeholder="All client types",

    key="client_type_filter",
)


# ============================================================
# 9. APPLY FILTERS
# ============================================================

filtered_df = dashboard_df.copy()


if country_filter:

    filtered_df = filtered_df[
        filtered_df[
            "country"
        ].isin(
            country_filter
        )
    ]


if region_filter:

    filtered_df = filtered_df[
        filtered_df[
            "region"
        ].isin(
            region_filter
        )
    ]


if purpose_filter:

    filtered_df = filtered_df[
        filtered_df[
            "acquisition_purpose"
        ].isin(
            purpose_filter
        )
    ]


if client_type_filter:

    filtered_df = filtered_df[
        filtered_df[
            "client_type"
        ].isin(
            client_type_filter
        )
    ]


# ============================================================
# 10. SIDEBAR STATUS & EXPORT
# ============================================================

st.sidebar.divider()


st.sidebar.metric(
    "Clients in View",
    f"{len(filtered_df):,}",
)


st.sidebar.caption(
    f"Out of {len(dashboard_df):,} total clients"
)


csv_export = (
    filtered_df
    .to_csv(index=False)
    .encode("utf-8")
)


st.sidebar.download_button(

    label="📥 Download Filtered Data",

    data=csv_export,

    file_name="real_estate_filtered_data.csv",

    mime="text/csv",

    use_container_width=True,
)


# ============================================================
# 11. EMPTY RESULTS
# ============================================================

if filtered_df.empty:

    st.warning(
        "No buyers match the selected filters. "
        "Please adjust your selection."
    )

    st.stop()


# ============================================================
# 12. EXECUTIVE OVERVIEW
# ============================================================

st.header(
    "Executive Overview"
)

st.caption(
    "High-level metrics for the selected buyer population."
)


total_clients = len(
    filtered_df
)


investment_clients = (

    filtered_df[
        "acquisition_purpose"
    ]
    .eq("Investment")
    .sum()
)


investment_percentage = (

    (
        investment_clients
        / total_clients
        * 100
    )

    if total_clients > 0

    else 0
)


average_total_value = (

    filtered_df[
        "total_property_value"
    ]
    .mean()
)


average_property_count = (

    filtered_df[
        "property_count"
    ]
    .mean()
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(

        "👥 Buyers Analyzed",

        f"{total_clients:,}",

        help=(
            "Number of clients matching "
            "the selected filters."
        ),
    )


with col2:

    st.metric(

        "📈 Investment Buyers",

        format_percentage(
            investment_percentage
        ),

        help=(
            "Percentage of clients whose "
            "acquisition purpose is Investment."
        ),
    )


with col3:

    st.metric(

        "💰 Avg Total Property Value",

        format_currency(
            average_total_value
        ),

        help=(
            "Average total property value "
            "associated with each client."
        ),
    )


with col4:

    st.metric(

        "🏘️ Avg Properties / Client",

        f"{average_property_count:.2f}",

        help=(
            "Average number of property "
            "records per client."
        ),
    )


st.divider()


# ============================================================
# 13. AUTOMATIC KEY INSIGHTS
# ============================================================

st.subheader(
    "🧠 Key Insights"
)


segment_counts = (

    filtered_df[
        "segment_name"
    ]
    .value_counts()
)


largest_segment = (
    segment_counts.idxmax()
)


largest_segment_count = (
    segment_counts.max()
)


activity_by_segment = (

    filtered_df
    .groupby(
        "segment_name"
    )[
        "property_count"
    ]
    .mean()
)


highest_activity_segment = (
    activity_by_segment.idxmax()
)


highest_activity_value = (
    activity_by_segment.max()
)


investment_by_segment = (

    filtered_df
    .groupby(
        "segment_name"
    )[
        "acquisition_purpose"
    ]
    .apply(
        lambda values:
        values.eq("Investment").mean()
        * 100
    )
)


highest_investment_share = (
    investment_by_segment.max()
)


investment_leaders = (

    investment_by_segment[
        investment_by_segment.eq(
            highest_investment_share
        )
    ]
    .index
    .tolist()
)


insight_col1, insight_col2, insight_col3 = (
    st.columns(3)
)


with insight_col1:

    with st.container(
        border=True
    ):

        st.markdown(
            "**Largest Buyer Segment**"
        )

        st.subheader(
            largest_segment
        )

        st.write(
            f"{largest_segment_count:,} clients "
            "in the selected population."
        )


with insight_col2:

    with st.container(
        border=True
    ):

        st.markdown(
            "**Highest Property Activity**"
        )

        st.subheader(
            highest_activity_segment
        )

        st.write(
            f"{highest_activity_value:.2f} "
            "properties per client on average."
        )


with insight_col3:

    with st.container(
        border=True
    ):

        st.markdown(
            "**Investment-Oriented Segments**"
        )

        st.subheader(
            f"{highest_investment_share:.1f}%"
        )

        st.write(
            "Investment-purpose share among: "
            + ", ".join(
                investment_leaders
            )
        )


st.divider()


# ============================================================
# 14. MAIN DASHBOARD TABS
# ============================================================

(
    overview_tab,
    behavior_tab,
    geography_tab,
    segments_tab,
    model_tab,
) = st.tabs(

    [
        "📊 Overview",
        "💰 Buyer Behavior",
        "🌎 Geography",
        "👥 Segment Explorer",
        "🧠 ML Methodology",
    ]
)


# ============================================================
# 15. OVERVIEW TAB
# ============================================================

with overview_tab:

    st.header(
        "Buyer Segmentation Overview"
    )

    st.caption(
        "Distribution and characteristics "
        "of the identified buyer segments."
    )


    segment_distribution = (

        filtered_df[
            "segment_name"
        ]

        .value_counts()

        .rename_axis(
            "Segment"
        )

        .reset_index(
            name="Clients"
        )
    )


    horizontal_bar_chart(

        data=segment_distribution,

        x="Clients",

        y="Segment",

        title="Buyer Segment Distribution",

        height=540,
    )


    st.subheader(
        "Buyer Segment Summary"
    )


    segment_summary = (

        filtered_df

        .groupby(
            "segment_name"
        )

        .agg(

            Clients=(
                "client_id",
                "count",
            ),

            Avg_Age=(
                "age",
                "mean",
            ),

            Avg_Properties=(
                "property_count",
                "mean",
            ),

            Avg_Total_Value=(
                "total_property_value",
                "mean",
            ),

            Investment_Share=(

                "acquisition_purpose",

                lambda values:
                values.eq("Investment")
                .mean()
                * 100,
            ),
        )

        .reset_index()

        .rename(

            columns={

                "segment_name":
                    "Buyer Segment",

                "Avg_Age":
                    "Avg Age",

                "Avg_Properties":
                    "Avg Properties",

                "Avg_Total_Value":
                    "Avg Total Property Value",

                "Investment_Share":
                    "Investment Share",
            }
        )

        .sort_values(
            "Clients",
            ascending=False,
        )
    )


    st.dataframe(

        segment_summary,

        use_container_width=True,

        hide_index=True,

        column_config={

            "Avg Age":
                st.column_config.NumberColumn(
                    format="%.1f"
                ),

            "Avg Properties":
                st.column_config.NumberColumn(
                    format="%.2f"
                ),

            "Avg Total Property Value":
                st.column_config.NumberColumn(
                    format="$%.0f"
                ),

            "Investment Share":
                st.column_config.NumberColumn(
                    format="%.1f%%"
                ),
        },
    )


    with st.expander(
        "📄 View Filtered Raw Dataset Rows"
    ):

        st.dataframe(
            filtered_df,
            use_container_width=True,
        )


# ============================================================
# 16. BUYER BEHAVIOR TAB
# ============================================================

with behavior_tab:

    st.header(
        "Buyer Behavior Analysis"
    )

    st.caption(
        "Explore acquisition purpose, financing, "
        "property activity, and property-value exposure."
    )


    col1, col2 = st.columns(2)


    with col1:

        purpose_counts = (

            filtered_df[
                "acquisition_purpose"
            ]

            .value_counts()

            .rename_axis(
                "Purpose"
            )

            .reset_index(
                name="Clients"
            )
        )


        categorical_bar_chart(

            data=purpose_counts,

            x="Purpose",

            y="Clients",

            title="Acquisition Purpose",
        )


    with col2:

        loan_counts = (

            filtered_df[
                "loan_applied"
            ]

            .value_counts()

            .rename_axis(
                "Loan Status"
            )

            .reset_index(
                name="Clients"
            )
        )


        categorical_bar_chart(

            data=loan_counts,

            x="Loan Status",

            y="Clients",

            title="Financing Behavior(Loan Applied)",
        )


    st.subheader(
        "Property Activity by Segment"
    )


    activity_df = (

        filtered_df

        .groupby(
            "segment_name"
        )[
            "property_count"
        ]

        .mean()

        .reset_index()

        .rename(

            columns={

                "segment_name":
                    "Segment",

                "property_count":
                    "Average Properties",
            }
        )
    )


    horizontal_bar_chart(

        data=activity_df,

        x="Average Properties",

        y="Segment",

        title="Average Properties per Client",

        height=540,

        decimals=2,
    )


    st.subheader(
        "Property Value by Segment"
    )


    value_df = (

        filtered_df

        .groupby(
            "segment_name"
        )[
            "total_property_value"
        ]

        .mean()

        .reset_index()

        .rename(

            columns={

                "segment_name":
                    "Segment",

                "total_property_value":
                    "Average Total Value",
            }
        )
    )


    horizontal_bar_chart(

        data=value_df,

        x="Average Total Value",

        y="Segment",

        title="Average Total Property Value per Client",

        height=540,

        currency=True,
    )


# ============================================================
# 17. GEOGRAPHIC BUYER ANALYSIS
# ============================================================

with geography_tab:

    st.header(
        "🌎 Geographic Buyer Analysis"
    )

    st.caption(
        "Explore the distribution of buyers "
        "across countries and regions."
    )


    # ========================================================
    # COUNTRY DISTRIBUTION
    # ========================================================

    country_counts = (

        filtered_df[
            "country"
        ]

        .value_counts()

        .rename_axis(
            "Country"
        )

        .reset_index(
            name="Clients"
        )
    )


    horizontal_bar_chart(

        data=country_counts,

        x="Clients",

        y="Country",

        title="Buyer Distribution by Country",

        height=440,
    )


    # ========================================================
    # INTERACTIVE GEOGRAPHIC MAP
    # ========================================================

    st.subheader(
        "🗺️ Geographic Buyer Map"
    )

    st.caption(
        "Buyer concentration by country. "
        "Hover over a country to view buyer count "
        "and investment share."
    )


    map_df = (

        filtered_df

        .groupby(
            "country"
        )

        .agg(

            Buyers=(
                "client_id",
                "count",
            ),

            Investment_Share=(

                "acquisition_purpose",

                lambda values:
                values.eq("Investment")
                .mean()
                * 100,
            ),
        )

        .reset_index()
    )


    map_df["iso_code"] = (

        map_df[
            "country"
        ]

        .map(
            COUNTRY_ISO_CODES
        )
    )


    # Keep only countries for which we have
    # a valid ISO-3 code.

    map_df = map_df[
        map_df[
            "iso_code"
        ].notna()
    ]


    if not map_df.empty:

        fig = px.choropleth(

            map_df,

            locations="iso_code",

            locationmode="ISO-3",

            color="Buyers",

            hover_name="country",

            hover_data={

                "Buyers":
                    ":,",

                "Investment_Share":
                    ":.1f",

                "iso_code":
                    False,
            },

            title="Buyer Distribution Across Countries",

            labels={

                "Buyers":
                    "Buyers",

                "Investment_Share":
                    "Investment Share (%)",
            },
        )


        fig.update_geos(

            showcoastlines=True,

            showcountries=True,

            showland=True,

            fitbounds="locations",
        )


        fig.update_layout(

            margin=dict(
                l=10,
                r=10,
                t=75,
                b=20,
            )
        )


        fig = create_plotly_layout(

            fig,

            height=540,
        )


        show_chart(fig)


    else:

        st.info(
            "No geographic records are available "
            "for the current filters."
        )


    # ========================================================
    # BUYER SEGMENTS BY COUNTRY
    # ========================================================

    st.subheader(
        "Buyer Segments by Country"
    )

    st.caption(
        "Compare the composition of buyer segments "
        "across countries."
    )


    country_segment = (

        filtered_df

        .groupby(
            [
                "country",
                "segment_name",
            ]
        )

        .size()

        .reset_index(
            name="Clients"
        )
    )


    fig = px.bar(

        country_segment,

        x="country",

        y="Clients",

        color="segment_name",

        barmode="stack",

        title="Segment Distribution Across Countries",

        labels={

            "country":
                "Country",

            "segment_name":
                "Buyer Segment",

            "Clients":
                "Clients",
        },
    )


    # ========================================================
    # IMPORTANT FIX:
    # Legend moved BELOW chart.
    # Extra bottom margin prevents overlap.
    # ========================================================

    fig.update_layout(

        legend=dict(

            orientation="h",

            yanchor="top",

            y=-0.22,

            xanchor="center",

            x=0.5,

            title_text="Buyer Segment",
        ),

        margin=dict(

            l=20,

            r=20,

            t=85,

            b=170,
        ),

        xaxis_title="Country",

        yaxis_title="Clients",
    )


    fig = create_plotly_layout(

        fig,

        height=680,
    )


    show_chart(fig)


    # ========================================================
    # TOP BUYER REGIONS
    # ========================================================

    st.subheader(
        "Top Buyer Regions"
    )


    region_counts = (

        filtered_df[
            "region"
        ]

        .value_counts()

        .head(10)

        .rename_axis(
            "Region"
        )

        .reset_index(
            name="Clients"
        )
    )


    horizontal_bar_chart(

        data=region_counts,

        x="Clients",

        y="Region",

        title="Top 10 Regions by Buyer Count",

        height=460,
    )


# ============================================================
# 18. SEGMENT EXPLORER TAB
# ============================================================

with segments_tab:

    st.header(
        "👥 Buyer Segment Explorer"
    )

    st.caption(
        "Explore the demographic, behavioral, "
        "and property characteristics of a segment."
    )


    available_segments = sorted(

        filtered_df[
            "segment_name"
        ]
        .unique()
        .tolist()
    )


    selected_segment = st.selectbox(

        "Select Buyer Segment",

        options=available_segments,
    )


    selected_segment_df = filtered_df[
        filtered_df[
            "segment_name"
        ].eq(
            selected_segment
        )
    ]


    st.subheader(
        selected_segment
    )


    segment_clients = len(
        selected_segment_df
    )


    segment_avg_age = (

        selected_segment_df[
            "age"
        ]
        .mean()
    )


    segment_avg_property_count = (

        selected_segment_df[
            "property_count"
        ]
        .mean()
    )


    segment_total_value = (

        selected_segment_df[
            "total_property_value"
        ]
        .mean()
    )


    segment_satisfaction = (

        selected_segment_df[
            "satisfaction_score"
        ]
        .mean()
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "👥 Clients",
            f"{segment_clients:,}",
        )


    with col2:

        st.metric(
            "🎂 Average Age",
            f"{segment_avg_age:.1f}",
        )


    with col3:

        st.metric(
            "🏘️ Avg Properties",
            f"{segment_avg_property_count:.2f}",
        )


    with col4:

        st.metric(
            "⭐ Satisfaction",
            f"{segment_satisfaction:.2f}/5",
        )


    st.divider()


    # ========================================================
    # ACQUISITION PURPOSE
    # ========================================================

    col1, col2 = st.columns(2)


    with col1:

        purpose_profile = (

            selected_segment_df[
                "acquisition_purpose"
            ]

            .value_counts()

            .rename_axis(
                "Purpose"
            )

            .reset_index(
                name="Clients"
            )
        )


        categorical_bar_chart(

            data=purpose_profile,

            x="Purpose",

            y="Clients",

            title="Acquisition Purpose",
        )


    with col2:

        loan_profile = (

            selected_segment_df[
                "loan_applied"
            ]

            .value_counts()

            .rename_axis(
                "Loan Status"
            )

            .reset_index(
                name="Clients"
            )
        )


        categorical_bar_chart(

            data=loan_profile,

            x="Loan Status",

            y="Clients",

            title="Loan Behavior",
        )


    # ========================================================
    # REFERRAL CHANNEL
    # ========================================================

    referral_profile = (

        selected_segment_df[
            "referral_channel"
        ]

        .value_counts()

        .rename_axis(
            "Referral Channel"
        )

        .reset_index(
            name="Clients"
        )
    )


    categorical_bar_chart(

        data=referral_profile,

        x="Referral Channel",

        y="Clients",

        title="Referral Channel",
    )


    # ========================================================
    # COUNTRY DISTRIBUTION
    # ========================================================

    country_profile = (

        selected_segment_df[
            "country"
        ]

        .value_counts()

        .rename_axis(
            "Country"
        )

        .reset_index(
            name="Clients"
        )
    )


    horizontal_bar_chart(

        data=country_profile,

        x="Clients",

        y="Country",

        title="Country Distribution",

        height=430,
    )


    # ========================================================
    # SEGMENT INTERPRETATION
    # ========================================================

    st.subheader(
        "🧠 Segment Interpretation"
    )


    dominant_purpose = (

        selected_segment_df[
            "acquisition_purpose"
        ]

        .mode()

        .iloc[0]
    )


    dominant_loan = (

        selected_segment_df[
            "loan_applied"
        ]

        .mode()

        .iloc[0]
    )


    dominant_referral = (

        selected_segment_df[
            "referral_channel"
        ]

        .mode()

        .iloc[0]
    )


    with st.container(
        border=True
    ):

        st.markdown(

            f"""
            **{selected_segment}**

            This segment contains **{segment_clients:,} clients**
            in the current filtered population.

            **Dominant acquisition purpose:** {dominant_purpose}

            **Most common loan status:** {dominant_loan}

            **Most common referral channel:** {dominant_referral}

            **Average age:** {segment_avg_age:.1f} years

            **Average properties per client:**
            {segment_avg_property_count:.2f}

            **Average total property value:**
            {format_currency(segment_total_value)}

            **Average satisfaction score:**
            {segment_satisfaction:.2f} / 5
            """
        )


# ============================================================
# 19. ML METHODOLOGY TAB
# ============================================================

with model_tab:

    st.header(
        "🧠 Machine Learning Methodology"
    )

    st.caption(
        "How the buyer segmentation model was developed."
    )


    st.subheader(
        "Project Workflow"
    )


    st.markdown(
        """
        **1. Data Collection** — Client and property datasets

        **2. Data Cleaning** — Validate records and data types

        **3. Feature Engineering** — Create client-level property metrics

        **4. Encoding and Scaling** — Prepare features for
        distance-based clustering

        **5. Model Comparison** — K-Means and Hierarchical Clustering

        **6. Cluster Evaluation** — Elbow Method and Silhouette Score

        **7. Sensitivity Analysis** — Examine the influence
        of geography and client type

        **8. Final Segmentation** — Interpret the identified
        buyer groups

        **9. Dashboard** — Explore segment characteristics
        and business insights
        """
    )


    st.divider()


    st.subheader(
        "Final Model Configuration"
    )


    model_col1, model_col2, model_col3 = (
        st.columns(3)
    )


    with model_col1:

        st.metric(
            "Algorithm",
            "Agglomerative",
        )


    with model_col2:

        st.metric(
            "Buyer Segments",
            "10",
        )


    with model_col3:

        st.metric(
            "Linkage",
            "Ward",
        )


    st.caption(

        "Final-model silhouette score: approximately 0.195. "
        "This indicates that cluster separation is limited; "
        "the segments should be interpreted as exploratory "
        "buyer profiles rather than sharply separated groups."
    )


    st.divider()


    st.subheader(
        "Features Used for Clustering"
    )


    feature_list = [

        "Age",

        "Gender",

        "Satisfaction Score",

        "Acquisition Purpose",

        "Loan Applied",

        "Referral Channel",

        "Property Count",

        "Total Property Value",

        "Average Property Value",

        "Average Floor Area",
    ]


    st.dataframe(

        pd.DataFrame(
            {
                "Feature":
                    feature_list
            }
        ),

        use_container_width=True,

        hide_index=True,
    )


# ============================================================
# 20. FOOTER
# ============================================================

st.divider()


st.caption(

    "Real Estate Buyer Intelligence | "
    "Machine Learning Based Buyer Segmentation "
    "& Investment Profiling"
)