import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("African Climate Trends Dashboard")

# Load datasets
ethiopia = pd.read_csv("data/ethiopia_clean.csv")
kenya = pd.read_csv("data/kenya_clean.csv")
sudan = pd.read_csv("data/sudan_clean.csv")
tanzania = pd.read_csv("data/tanzania_clean.csv")
nigeria = pd.read_csv("data/nigeria_clean.csv")

# Add country column
ethiopia["Country"] = "Ethiopia"
kenya["Country"] = "Kenya"
sudan["Country"] = "Sudan"
tanzania["Country"] = "Tanzania"
nigeria["Country"] = "Nigeria"

# Combine datasets
df = pd.concat([ethiopia, kenya, sudan, tanzania, nigeria])

df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].dt.year

# Sidebar controls
st.sidebar.header("Filters")

countries = st.sidebar.multiselect(
    "Select Countries",
    df["Country"].unique(),
    default=df["Country"].unique()
)

year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (2015, 2026)
)

variable = st.sidebar.selectbox(
    "Select Variable",
    ["T2M", "PRECTOTCORR", "RH2M"]
)

# Filter data
filtered = df[
    (df["Country"].isin(countries)) &
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]

# Temperature trend chart
st.subheader("Temperature Trend")

monthly = filtered.groupby(["Country","Date"])[variable].mean().reset_index()

fig, ax = plt.subplots()

for country in monthly["Country"].unique():
    data = monthly[monthly["Country"] == country]
    ax.plot(data["Date"], data[variable], label=country)

ax.set_xlabel("Date")
ax.set_ylabel(variable)
ax.legend()

st.pyplot(fig)

# Precipitation distribution
st.subheader("Precipitation Distribution")

fig2, ax2 = plt.subplots()

sns.boxplot(x="Country", y="PRECTOTCORR", data=filtered, ax=ax2)

st.pyplot(fig2)