
# ============================================================
# PHARMAOPT v1.0 — PHARMACEUTICAL SUPPLY CHAIN INTELLIGENCE
# Complete dashboard with navy + teal visual redesign
# ============================================================

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="PharmaOpt | Supply Chain Intelligence",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = Path(__file__).resolve().parent

DATA_FILE = (
    ROOT
    / "pharmaopt_2025_dashboard_corrected_v01.csv.gz"
)


# ============================================================
# PROFESSIONAL VISUAL DESIGN
# ============================================================

st.markdown(
    """
<style>
:root {
    --po-navy: #0B1728;
    --po-navy-light: #14283D;
    --po-teal: #087F78;
    --po-mint: #14B8A6;
    --po-text: #15263B;
    --po-muted: #64748B;
    --po-border: #DFE8EF;
    --po-surface: #FFFFFF;
    --po-background: #F4F7FB;
}

/* Main application */
[data-testid="stAppViewContainer"] {
    background: var(--po-background);
    color: var(--po-text);
}

.block-container {
    max-width: 1480px;
    padding-top: 2.3rem;
    padding-bottom: 4rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--po-navy);
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #EAF3F7 !important;
}

[data-testid="stSidebar"] input {
    color: #15263B !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #15263B;
}

/* Typography */
h1, h2, h3 {
    color: var(--po-text);
    letter-spacing: -0.025em;
}

h1 {
    font-size: 2.6rem !important;
    font-weight: 750 !important;
}

h2 {
    font-weight: 700 !important;
}

h3 {
    font-weight: 650 !important;
}

/* Hero panel */
.po-hero {
    background: linear-gradient(
        120deg,
        #0B1728 0%,
        #142F42 65%,
        #0B4F54 100%
    );
    border: 1px solid #24475A;
    border-radius: 20px;
    padding: 32px 36px;
    margin-bottom: 22px;
    box-shadow: 0 12px 30px rgba(11, 23, 40, 0.10);
}

.po-eyebrow {
    color: #72E4D2;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.13em;
    margin-bottom: 12px;
}

.po-hero-title {
    color: #F8FAFC !important;
    font-size: 2.25rem;
    font-weight: 760;
    letter-spacing: -0.035em;
    margin-bottom: 10px;
}

.po-hero-subtitle {
    color: #C3D3E1;
    font-size: 1.03rem;
    line-height: 1.7;
    max-width: 780px;
}

.po-status {
    display: inline-block;
    margin-top: 20px;
    padding: 7px 13px;
    background: rgba(20, 184, 166, 0.15);
    border: 1px solid rgba(114, 228, 210, 0.30);
    border-radius: 100px;
    color: #8EF3E0;
    font-size: 0.78rem;
    font-weight: 650;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: var(--po-surface);
    border: 1px solid var(--po-border);
    border-radius: 16px;
    padding: 22px 20px;
    box-shadow: 0 4px 18px rgba(15, 35, 55, 0.035);
    transition: transform 0.18s ease, box-shadow 0.18s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 9px 24px rgba(15, 35, 55, 0.07);
}

[data-testid="stMetricLabel"] {
    color: var(--po-muted);
    font-weight: 550;
}

[data-testid="stMetricValue"] {
    color: var(--po-navy);
    font-weight: 750;
    letter-spacing: -0.03em;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    border-bottom: 1px solid var(--po-border);
    margin-bottom: 1.5rem;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px 10px 0 0;
    padding: 12px 20px;
    color: var(--po-muted);
    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    color: var(--po-teal) !important;
    background: #E7F5F3 !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    background: var(--po-teal);
}

/* Buttons */
.stDownloadButton button,
.stButton button[kind="primary"] {
    background: var(--po-teal);
    color: white;
    border: 1px solid var(--po-teal);
    border-radius: 10px;
    font-weight: 650;
    padding: 0.6rem 1.2rem;
}

.stDownloadButton button:hover,
.stButton button[kind="primary"]:hover {
    background: #066B66;
    color: white;
    border-color: #066B66;
}

/* Dataframes */
[data-testid="stDataFrame"] {
    border: 1px solid var(--po-border);
    border-radius: 12px;
    overflow: hidden;
}

/* Inputs */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    border-radius: 10px;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Captions */
[data-testid="stCaptionContainer"] {
    color: var(--po-muted);
}

/* Section cards */
.po-step {
    background: white;
    border: 1px solid #DFE8EF;
    border-radius: 14px;
    padding: 22px;
    min-height: 145px;
    margin-bottom: 10px;
}

.po-step-number {
    color: #087F78;
    font-size: 0.8rem;
    font-weight: 750;
    margin-bottom: 10px;
}

.po-step-title {
    color: #15263B;
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 8px;
}

.po-step-text {
    color: #64748B;
    font-size: 0.9rem;
    line-height: 1.6;
}

/* Mobile */
@media (max-width: 768px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        padding-top: 1.5rem;
    }

    .po-hero {
        padding: 24px 20px;
    }

    .po-hero-title {
        font-size: 1.7rem;
    }

    h1 {
        font-size: 2rem !important;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        DATA_FILE,
        dtype={"package_ndc": "string"},
        low_memory=False,
    )

    required = [
        "package_ndc",
        "prediction_year",
        "risk_score_v04",
        "risk_score_v05",
        "generic_name",
        "brand_name",
        "labeler_name",
        "dosage_form",
        "fda_event_any",
        "non_discontinuation_event_candidate",
        "discontinuation_notice_candidate",
    ]

    missing = sorted(set(required) - set(df.columns))

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    if len(df) != 221667:
        raise ValueError(
            f"Unexpected row count: {len(df):,}"
        )

    if df["package_ndc"].isna().any():
        raise ValueError("Missing package identifiers")

    if df["package_ndc"].duplicated().any():
        raise ValueError("Duplicate package identifiers")

    if not df["prediction_year"].eq(2025).all():
        raise ValueError("Expected 2025 data only")

    for column in ["risk_score_v04", "risk_score_v05"]:

        df[column] = pd.to_numeric(
            df[column],
            errors="raise",
        )

        if not np.isfinite(df[column]).all():
            raise ValueError(
                f"Invalid scores in {column}"
            )

    target_columns = [
        "fda_event_any",
        "non_discontinuation_event_candidate",
        "discontinuation_notice_candidate",
    ]

    for column in target_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="raise",
        )

        if not df[column].isin([0, 1]).all():
            raise ValueError(
                f"Invalid outcome labels in {column}"
            )

    for column in [
        "generic_name",
        "brand_name",
        "labeler_name",
        "dosage_form",
    ]:

        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
            .fillna("Not available")
        )

        df.loc[
            df[column].eq(""),
            column,
        ] = "Not available"

    return df


try:
    data = load_data()

except (FileNotFoundError, ValueError) as error:

    st.error(
        f"Unable to load PharmaOpt data: {error}"
    )

    st.info(
        "The dashboard needs the compressed data file "
        "pharmaopt_2025_dashboard_corrected_v01.csv.gz "
        "in the same folder as this Python script."
    )

    st.stop()


# ============================================================
# RANKING FUNCTION
# ============================================================

@st.cache_data
def rank_packages(df, score_column):

    ranked = df.sort_values(
        [score_column, "package_ndc"],
        ascending=[False, True],
    ).reset_index(drop=True)

    ranked["risk_rank"] = np.arange(
        1,
        len(ranked) + 1,
    )

    return ranked


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("## 💊 PharmaOpt")

st.sidebar.caption(
    "SUPPLY CHAIN INTELLIGENCE"
)

st.sidebar.divider()

st.sidebar.subheader("Choose a ranking model")
st.sidebar.caption("v0.4 is the recommended comparison model; v0.5 is an experimental alternative.")

model = st.sidebar.selectbox(
    "Model used to rank packages",
    ["v0.4", "v0.5"],
)

score_col = {
    "v0.4": "risk_score_v04",
    "v0.5": "risk_score_v05",
}[model]

st.sidebar.divider()

st.sidebar.subheader("Plan a sample review")
st.sidebar.caption(
    "Imagine a team deciding which products to examine first. "
    "Change the budget, cost per review, or team capacity to "
    "see how many packages could be selected."
)
budget = st.sidebar.slider(
    "Available review budget ($) — example only",
    min_value=10000,
    max_value=2000000,
    value=500000,
    step=10000,
)

review_cost = st.sidebar.number_input(
    "Estimated cost to review one package ($)",
    min_value=1,
    value=1000,
    step=100,
)

max_capacity = st.sidebar.slider(
    "Team capacity (number of packages)",
    min_value=100,
    max_value=5000,
    value=500,
    step=100,
)

capacity = min(
    int(budget // review_cost),
    max_capacity,
    len(data),
)
st.sidebar.info(
    f"This example selects **{capacity:,} packages** for review. "
    f"At ${review_cost:,.0f} each, the assumed total cost is "
    f"**${capacity * review_cost:,.0f}**. "
    "No real spending or purchases occur."
)
ranked = rank_packages(
    data,
    score_col,
)

selected = ranked.head(
    capacity
).copy()

selected["review_status"] = "Not reviewed"

selected["assumed_review_cost"] = review_cost

selected["priority_tier"] = pd.cut(
    selected["risk_rank"],
    bins=[0, 100, 250, np.inf],
    labels=["Tier 1", "Tier 2", "Tier 3"],
)

st.sidebar.divider()

st.sidebar.caption(
    "Research prototype · 2025 retrospective data"
)

st.sidebar.caption(
    "Not validated for live clinical or "
    "purchasing decisions."
)


# ============================================================
# HERO HEADER
# ============================================================

st.markdown(
    """
<div class="po-hero">
    <div class="po-eyebrow">
        PHARMAOPT / RESEARCH INTELLIGENCE
    </div>
    <div class="po-hero-title">
        Pharmaceutical Supply Chain Intelligence
    </div>
    <div class="po-hero-subtitle">
        When a team cannot investigate every drug product, where should it start?
        Explore a research-based ranking and see how limited review capacity
        changes which packages are selected.
    </div>
    <div class="po-status">
        ● RESEARCH PROTOTYPE · VERSION 1.0
    </div>
</div>
""",
    unsafe_allow_html=True,
)

st.caption(
    "2025 historical study  •  FDA and Medicare (CMS) records  •  Demonstration, not a live monitoring service"
)

st.markdown("### Start here")
st.write(
    "PharmaOpt explores a practical question: if a team can review only a "
    "small number of pharmaceutical packages, which ones might deserve "
    "a closer look first? It combines historical public data and two "
    "experimental ranking models to organize that review."
)
st.write(
    "**Try it:** Use the budget controls on the left, browse the selected "
    "products in **Drug Explorer**, and compare the two models in "
    "**Model Evaluation**. Nothing on this page places an order or spends money."
)
st.info(
    "**Important:** A high model score means higher position on an "
    "experimental review list—not a confirmed shortage or a percentage "
    "chance of shortage. Historical FDA-linked events are not the same "
    "as verified active drug shortages."
)

# ============================================================
# NAVIGATION
# ============================================================

tab_overview, tab_drugs, tab_models, tab_method = st.tabs(
    [
        "📊 Overview",
        "💊 Drug Explorer",
        "📈 Model Evaluation",
        "📖 Methodology",
    ]
)


# ============================================================
# TAB 1 — OVERVIEW
# ============================================================

with tab_overview:

    st.subheader("Your review plan at a glance")

    st.write(
        "These numbers show the size of the historical dataset and what "
        "your example budget would cover. All costs are assumptions, not actual spending."
    )

    a, b, c, d = st.columns(4)

    a.metric(
        "Packages in the 2025 study",
        f"{len(data):,}",
    )

    b.metric(
        "Packages selected for review",
        f"{len(selected):,}",
    )

    c.metric(
        "Example review cost",
        f"${len(selected) * review_cost:,.0f}",
    )

    d.metric(
        "Budget remaining",
        f"${budget - len(selected) * review_cost:,.0f}",
    )

    st.caption(
        f"Active model: {model} | "
        f"Reviewing {len(selected) / len(data) * 100:.3f}% "
        "of available packages"
    )

    st.divider()

    st.subheader("How PharmaOpt works in three steps")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
<div class="po-step">
    <div class="po-step-number">STEP 01</div>
    <div class="po-step-title">Analyze</div>
    <div class="po-step-text">
        Integrate pharmaceutical product information
        with historical FDA and CMS records.
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
<div class="po-step">
    <div class="po-step-number">STEP 02</div>
    <div class="po-step-title">Prioritize</div>
    <div class="po-step-text">
        Apply experimental machine-learning rankings
        to identify packages for further review.
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            """
<div class="po-step">
    <div class="po-step-number">STEP 03</div>
    <div class="po-step-title">Allocate</div>
    <div class="po-step-text">
        Simulate the allocation of limited review
        capacity under hypothetical cost constraints.
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

    st.divider()

    st.subheader("Which packages would be reviewed first?")
    st.caption(
        "This table shows the 20 highest-ranked packages in your selection. "
        "Position 1 means first to review, not most likely to be in shortage. "
        "A model score is a ranking indicator, not a probability."
    )

    overview_columns = [
        "package_ndc",
        "generic_name",
        "brand_name",
        "labeler_name",
        "risk_rank",
        score_col,
    ]

    st.dataframe(
        selected[overview_columns].head(20).rename(
            columns={
                "package_ndc": "Package NDC",
                "generic_name": "Generic Name",
                "brand_name": "Brand Name",
                "labeler_name": "FDA Labeler",
                "risk_rank": "Priority Rank",
                score_col: "Model Score",
            }
        ),
        hide_index=True,
        use_container_width=True,
    )

    st.divider()

    st.subheader("How the selected packages are grouped")
    st.caption(
        "Tier 1 = ranks 1–100; Tier 2 = ranks 101–250; "
        "Tier 3 = remaining selected packages. These are organizing buckets, "
        "not clinically validated risk categories."
    )

    tier_summary = (
        selected["priority_tier"]
        .value_counts()
        .reindex(
            ["Tier 1", "Tier 2", "Tier 3"],
            fill_value=0,
        )
        .reset_index()
    )

    tier_summary.columns = [
        "Priority Tier",
        "Packages",
    ]

    fig_tiers = px.bar(
        tier_summary,
        x="Priority Tier",
        y="Packages",
        text="Packages",
        title="Selected Packages by Priority Tier",
        color="Priority Tier",
        color_discrete_map={
            "Tier 1": "#087F78",
            "Tier 2": "#16A6A0",
            "Tier 3": "#78CFC4",
        },
    )

    fig_tiers.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#15263B"),
        margin=dict(l=20, r=20, t=60, b=20),
    )

    st.plotly_chart(
        fig_tiers,
        use_container_width=True,
    )


# ============================================================
# TAB 2 — DRUG EXPLORER
# ============================================================

with tab_drugs:

    st.subheader("Explore the products selected for review")
    st.write(
        "Search within the packages your current budget and model selected. "
        "You can look up a drug name, brand, company labeler, or NDC "
        "(the FDA identifier for a drug package)."
    )
    st.caption(
        "Can't find a product? The search covers only selected packages. "
        "Increase your review capacity to include more products."
    )

    search = st.text_input(
        "Find a selected package",
        placeholder="Search by drug, brand, labeler, or NDC",
    )

    explorer = selected.copy()

    if search:

        search_fields = [
            "package_ndc",
            "generic_name",
            "brand_name",
            "labeler_name",
        ]

        matches = pd.Series(
            False,
            index=explorer.index,
        )

        for field in search_fields:

            matches |= (
                explorer[field]
                .astype("string")
                .str.contains(
                    search,
                    case=False,
                    regex=False,
                    na=False,
                )
            )

        explorer = explorer.loc[matches]

    display_columns = [
        "package_ndc",
        "generic_name",
        "brand_name",
        "labeler_name",
        "dosage_form",
        "risk_rank",
        score_col,
        "priority_tier",
    ]

    st.caption(
        f"Showing {len(explorer):,} "
        f"of {len(selected):,} selected packages"
    )

    st.dataframe(
        explorer[display_columns].rename(
            columns={
                "package_ndc": "Package NDC",
                "generic_name": "Generic Name",
                "brand_name": "Brand Name",
                "labeler_name": "FDA Labeler",
                "dosage_form": "Dosage Form",
                "risk_rank": "Priority Rank",
                score_col: "Model Score",
                "priority_tier": "Priority Tier",
            }
        ),
        use_container_width=True,
        hide_index=True,
        height=430,
    )

    st.download_button(
        "Download Selected Package Rankings",
        data=selected[
            display_columns
            + [
                "review_status",
                "assumed_review_cost",
            ]
        ].to_csv(index=False).encode("utf-8"),
        file_name=f"pharmaopt_{model}_allocation.csv",
        mime="text/csv",
    )

    st.divider()

    st.subheader("Which drug groups appear most often?")

    st.caption(
        "Groups are based on generic names and dosage "
        "forms. They do not establish clinical equivalence."
    )

    explorer_groups = selected.copy()

    known_name = (
        explorer_groups["generic_name"]
        .str.casefold()
        .ne("not available")
    )

    explorer_groups["drug_group"] = (
        explorer_groups["generic_name"]
        + " — "
        + explorer_groups["dosage_form"]
    )

    explorer_groups.loc[
        ~known_name,
        "drug_group",
    ] = (
        "Unidentified package "
        + explorer_groups.loc[
            ~known_name,
            "package_ndc",
        ]
    )

    drug_summary = (
        explorer_groups.groupby(
            "drug_group",
            as_index=False,
        )
        .agg(
            packages=("package_ndc", "nunique"),
            best_rank=("risk_rank", "min"),
            highest_score=(score_col, "max"),
        )
    )

    st.metric(
        "Distinct drug-form groups",
        f"{len(drug_summary):,}",
    )

    most_represented = (
        drug_summary.sort_values(
            "packages",
            ascending=False,
        ).head(12)
    )

    if not most_represented.empty:

        fig_drugs = px.bar(
            most_represented.sort_values("packages"),
            x="packages",
            y="drug_group",
            orientation="h",
            title="Most Represented Drug Groups",
            labels={
                "packages": "Selected Packages",
                "drug_group": "Drug / Dosage Form",
            },
            color_discrete_sequence=["#087F78"],
        )

        fig_drugs.update_layout(
            height=500,
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="#15263B"),
        )

        st.plotly_chart(
            fig_drugs,
            use_container_width=True,
        )

    st.divider()

    st.subheader("Which FDA-listed companies appear most often?")
    st.caption(
        "This chart counts selected packages by their FDA labeler. "
        "A labeler is not necessarily the company that physically made the drug."
    )

    known_labelers = selected.loc[
        selected["labeler_name"]
        .str.casefold()
        .ne("not available")
    ]

    labeler_summary = (
        known_labelers.groupby(
            "labeler_name",
            as_index=False,
        )
        .agg(
            packages=("package_ndc", "nunique"),
        )
        .sort_values(
            "packages",
            ascending=False,
        )
        .head(12)
    )

    if not labeler_summary.empty:

        fig_labelers = px.bar(
            labeler_summary.sort_values("packages"),
            x="packages",
            y="labeler_name",
            orientation="h",
            title="Most Represented FDA Labelers",
            labels={
                "packages": "Selected Packages",
                "labeler_name": "FDA Labeler",
            },
            color_discrete_sequence=["#16A6A0"],
        )

        fig_labelers.update_layout(
            height=500,
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="#15263B"),
        )

        st.plotly_chart(
            fig_labelers,
            use_container_width=True,
        )

    st.caption(
        "FDA labelers are not necessarily "
        "the physical manufacturers."
    )


# ============================================================
# TAB 3 — MODEL EVALUATION
# ============================================================

with tab_models:

    st.subheader("Which ranking model performed better?")
    st.write(
        "A ranking model orders packages for closer review. We compare two "
        "versions by looking backward at recorded FDA-linked events in 2025. "
        "The question is: how many of those event-linked packages appear near "
        "the top of each model's list?"
    )
    st.write(
        "**v0.4 — simpler model:** Uses the earlier feature set and performs "
        "better on the main historical comparison. "
        "**v0.5 — expanded model:** Also uses more recall-text information; "
        "the tested version did not outperform v0.4 on the main outcome."
    )
    st.caption(
        "These models also used different training solvers in the corrected "
        "comparison, so the result cannot be attributed solely to the added text features."
    )

    target_options = {
        "All FDA-linked events (main comparison)": "fda_event_any",
        "Non-discontinuation event candidates (smaller group)":
            "non_discontinuation_event_candidate",
        "Discontinuation notices": "discontinuation_notice_candidate",
    }
    target_name = st.selectbox(
        "Which type of historical FDA record should we compare?",
        list(target_options),
        help=(
            "The main comparison includes all FDA-linked event flags. "
            "The smaller non-discontinuation group has just 12 candidates in 2025. "
            "Neither means a verified active shortage."
        ),
    )
    target = target_options[target_name]
    positives = int(data[target].sum())

    evaluation = []
    for version, column in [
        ("v0.4", "risk_score_v04"),
        ("v0.5", "risk_score_v05"),
    ]:
        ordered = rank_packages(data, column)
        cumulative = ordered[target].cumsum()
        for n in [100, 250, 500, 1000, 2500, 5000]:
            captured = int(cumulative.iloc[n - 1])
            evaluation.append({
                "Model": version,
                "Review Capacity": n,
                "Events Captured": captured,
                "Recall": captured / positives if positives else 0,
            })

    evaluation_df = pd.DataFrame(evaluation)
    top500 = evaluation_df.loc[evaluation_df["Review Capacity"].eq(500)]
    cap04 = int(top500.loc[top500["Model"].eq("v0.4"), "Events Captured"].iloc[0])
    cap05 = int(top500.loc[top500["Model"].eq("v0.5"), "Events Captured"].iloc[0])

    m1, m2, m3 = st.columns(3)
    m1.metric("Packages with this recorded outcome", f"{positives:,}")
    m2.metric("v0.4: found in first 500", f"{cap04} of {positives}")
    m3.metric("v0.5: found in first 500", f"{cap05} of {positives}")

    st.write(
        "**Example:** If a team could examine only 500 packages, the numbers "
        "above show how many packages with the selected historical record "
        "each model would have included. This does **not** measure prevented shortages."
    )

    fig_eval = px.line(
        evaluation_df,
        x="Review Capacity",
        y="Events Captured",
        color="Model",
        markers=True,
        title=f"Historical event records found at different review limits — {target_name}",
        color_discrete_map={"v0.4": "#087F78", "v0.5": "#2D5B9A"},
    )
    fig_eval.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#15263B"),
        margin=dict(l=20, r=20, t=60, b=20),
    )
    st.plotly_chart(fig_eval, use_container_width=True)
    st.caption(
        "How to read the chart: the horizontal axis is the number of packages "
        "a team could review. The vertical axis is how many packages with "
        "the selected historical FDA record appear in those top-ranked packages. "
        "At the same review limit, a higher line means more historical events found."
    )

    with st.expander("Show the detailed comparison table"):
        detail = evaluation_df.rename(columns={
            "Review Capacity": "Packages reviewed",
            "Events Captured": "Historical events found",
            "Recall": "Share of recorded events found",
        })
        st.dataframe(detail, use_container_width=True, hide_index=True)
        st.caption(
            "'Share of recorded events found' means the fraction of flagged "
            "2025 packages included in the selected top-N list—not a model probability."
        )

    st.warning(
        "**Research limitations:** Only 12 non-discontinuation event candidates "
        "appear in the 2025 data. FDA-linked event flags do not establish "
        "active shortages. The 2025 data was examined repeatedly during "
        "development, so this is not an independent or prospective test."
    )


# ============================================================
# TAB 4 — METHODOLOGY
# ============================================================

with tab_method:

    st.subheader("How this research was built")
    st.write(
        "**In one sentence:** PharmaOpt combines historical public drug data "
        "with experimental scoring methods to help explore which packages "
        "might be reviewed first under limited resources."
    )

    st.write(
        "PharmaOpt is a research and decision-support "
        "prototype exploring how pharmaceutical data "
        "and analytical methods can simplify supply-chain "
        "monitoring and review prioritization."
    )

    st.divider()

    st.markdown("#### Where the information comes from")
    st.caption("FDA = U.S. Food and Drug Administration. CMS = Centers for Medicare & Medicaid Services.")

    st.write(
        "**FDA National Drug Code Directory:** "
        "Product identifiers, drug names, FDA labelers, "
        "dosage forms, and package information."
    )

    st.write(
        "**FDA Drug Shortage Data:** "
        "Historical event records used to construct "
        "experimental outcome indicators."
    )

    st.write(
        "**FDA Recall Data:** "
        "Historical recall-related information "
        "used in the modeling pipeline."
    )

    st.write(
        "**CMS Data:** "
        "Historical prescription utilization and "
        "expenditure information where matching "
        "records were available."
    )

    st.divider()

    st.markdown("#### How the rankings were evaluated")

    st.write(
        "The models were trained on historical "
        "package-year records from 2022–2024 "
        "and evaluated retrospectively on 2025 records."
    )

    st.write(
        "The application ranks packages using existing "
        "v0.4 and v0.5 scores. These are ranking "
        "indicators, not calibrated shortage probabilities."
    )

    st.divider()

    st.markdown("#### How the sample budget works")

    st.write(
        "The allocation simulation assumes an equal "
        "cost for every package review. The highest-ranked "
        "packages are selected until the hypothetical "
        "budget or review capacity is reached."
    )

    st.divider()

    st.markdown("#### What this study cannot tell us")

    st.markdown(
        """
- FDA event status is not a validated historical
  active-shortage label.
- Historical FDA event coverage may be incomplete.
- Some product and package matches may be ambiguous.
- Model evaluation is limited by sparse outcomes.
- Prediction-time feature availability requires
  additional validation.
- Review costs are hypothetical.
- No clinical benefit, shortage prevention, or
  financial savings have been demonstrated.
"""
    )

    st.divider()

    st.markdown("#### What PharmaOpt is intended for")

    st.write(
        "Educational research, pharmaceutical data "
        "exploration, retrospective analysis, and "
        "hypothetical resource-allocation simulations."
    )

    with st.expander("Plain-English glossary"):
        st.markdown(
            "**Package:** A specific FDA-listed drug package, identified by an NDC.\n\n"
            "**Ranking model:** A method that puts packages in an order for review.\n\n"
            "**Model score:** A number used to sort packages, not a shortage probability.\n\n"
            "**FDA-linked event:** A record associated with an FDA event; "
            "it does not prove the package was in an active shortage.\n\n"
            "**Retrospective:** Looking back at past records, rather than "
            "monitoring events as they happen.\n\n"
            "**Review capacity:** The maximum number of packages a team can examine."
        )

    st.error(
        "Not validated for clinical decisions, "
        "live shortage prediction, procurement automation, "
        "or real-world inventory allocation."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "PharmaOpt v1.0 | Pharmaceutical Supply Chain "
    "Intelligence | Research Prototype"
)
