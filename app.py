import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="YouTube Channel Analytics Dashboard", layout="wide")

st.title("📊 YouTube Channel Analytics Dashboard")

# Upload CSV
uploaded_file = st.file_uploader("Upload your YouTube data CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Convert date column
    if "published_date" in df.columns:
        df["published_date"] = pd.to_datetime(df["published_date"])

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # Sidebar Filters
    st.sidebar.header("Filter Options")

    if "published_date" in df.columns:
        min_date = df["published_date"].min()
        max_date = df["published_date"].max()

        start_date, end_date = st.sidebar.date_input(
            "Select Date Range",
            [min_date, max_date]
        )

        filtered_data = df[
            (df["published_date"] >= pd.to_datetime(start_date)) &
            (df["published_date"] <= pd.to_datetime(end_date))
        ]
    else:
        filtered_data = df

    # Metrics
    st.subheader("📌 Key Metrics")

    col1, col2, col3 = st.columns(3)

    if "view_count" in filtered_data.columns:
        total_views = filtered_data["view_count"].sum()
    else:
        total_views = 0

    if "like_count" in filtered_data.columns:
        total_likes = filtered_data["like_count"].sum()
    else:
        total_likes = 0

    if "comment_count" in filtered_data.columns:
        total_comments = filtered_data["comment_count"].sum()
    else:
        total_comments = 0

    col1.metric("Total Views", f"{total_views:,}")
    col2.metric("Total Likes", f"{total_likes:,}")
    col3.metric("Total Comments", f"{total_comments:,}")

    # Views Over Time
    if "published_date" in filtered_data.columns and "view_count" in filtered_data.columns:
        st.subheader("📈 Views Over Time")

        fig = px.line(
            filtered_data,
            x="published_date",
            y="view_count",
            markers=True,
            title="Views Growth Over Time"
        )

        st.plotly_chart(fig, use_container_width=True)

    # Top 10 Videos
    if "video_title" in filtered_data.columns and "view_count" in filtered_data.columns:
        st.subheader("🔥 Top 10 Videos by Views")

        top_videos = filtered_data.sort_values(
            by="view_count",
            ascending=False
        ).head(10)

        fig2 = px.bar(
            top_videos,
            x="view_count",
            y="video_title",
            orientation="h",
            title="Top 10 Most Viewed Videos"
        )

        st.plotly_chart(fig2, use_container_width=True)

else:
    st.info("Please upload a CSV file to view analytics.")
