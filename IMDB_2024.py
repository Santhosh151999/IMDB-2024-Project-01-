import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from sqlalchemy import create_engine

# MySQL Connection
engine = create_engine("mysql+mysqlconnector://root:Dark2020%40@localhost/IMDB_2024")

# Load data from MySQL
query = "SELECT * FROM movies2024"
df = pd.read_sql(query, engine)

# Fill missing genres
df['Genre'] = df['Genre'].fillna('Unknown')

# Explode genres for individual analysis
def split_genres(df):
    rows = []
    for _, row in df.iterrows():
        for genre in row['Genre'].split(','):
            new_row = row.copy()
            new_row['Genre'] = genre.strip()
            rows.append(new_row)
    return pd.DataFrame(rows)

df_exploded = split_genres(df)

# Navigation
page = st.sidebar.radio("Choose View:", ["Visualizations", "Interactive Filter"])

if page == "Visualizations":
    st.title("IMDb 2024 Movie Analysis")
    st.header("Data Visualizations")

    top_movies = df[df['Votes'] > 1000].sort_values(by=['Ratings', 'Votes'], ascending=False).head(10)
    st.subheader("Top 10 Movies by Rating and Voting")
    st.dataframe(top_movies[['Title', 'Genre', 'Ratings', 'Votes']])

    genre_count = df_exploded['Genre'].value_counts().reset_index()
    genre_count.columns = ['Genre', 'Count']
    st.subheader("Genre Distribution")
    st.bar_chart(data=genre_count.set_index('Genre'))

    avg_duration = df_exploded.groupby('Genre')['Duration'].mean().sort_values()
    st.subheader("Average Duration by Genre")
    fig, ax = plt.subplots()
    avg_duration.plot(kind='barh', ax=ax)
    st.pyplot(fig)

    avg_votes = df_exploded.groupby('Genre')['Votes'].mean().sort_values(ascending=False)
    st.subheader("Average Voting Counts by Genre")
    st.bar_chart(avg_votes)

    st.subheader("Rating Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df['Ratings'].dropna(), bins=20, kde=True, ax=ax)
    st.pyplot(fig)

    top_per_genre = df_exploded.sort_values('Ratings', ascending=False).groupby('Genre').first().reset_index()
    st.subheader("Top-rated Movie per Genre")
    st.dataframe(top_per_genre[['Genre', 'Title', 'Ratings']])

    genre_votes = df_exploded.groupby('Genre')['Votes'].sum().reset_index().sort_values(by='Votes', ascending=False)
    st.subheader("Most Popular Genres by Total Votes")
    fig = px.pie(genre_votes, names='Genre', values='Votes')
    st.plotly_chart(fig)

    min_duration_row = df.loc[df['Duration'].idxmin()][['Title', 'Duration']]
    max_duration_row = df.loc[df['Duration'].idxmax()][['Title', 'Duration']]
    duration_extremes = pd.DataFrame({
        "Type": ["Shortest", "Longest"],
        "Title": [min_duration_row['Title'], max_duration_row['Title']],
        "Duration (Minutes)": [min_duration_row['Duration'], max_duration_row['Duration']]
    })
    st.subheader("Duration Extremes")
    st.dataframe(duration_extremes)

    avg_rating_genre = df_exploded.groupby('Genre')['Ratings'].mean().reset_index()
    st.subheader("Ratings by Genre Heatmap")
    heatmap_df = avg_rating_genre.pivot_table(index='Genre', values='Ratings')
    fig, ax = plt.subplots(figsize=(10, len(heatmap_df) * 0.4))
    sns.heatmap(heatmap_df, annot=True, cmap='YlGnBu', ax=ax)
    st.pyplot(fig)

    st.subheader("Ratings vs Votes Correlation")
    fig = px.scatter(df, x='Votes', y='Ratings', hover_data=['Title'])
    st.plotly_chart(fig)

elif page == "Interactive Filter":
    st.title("Interactive Movie Filter")

    st.sidebar.header("Filter Movies")

    genres = sorted(df_exploded['Genre'].unique().tolist())
    selected_genres = st.sidebar.multiselect("Select Genre(s):", genres)

    min_rating, max_rating = float(df_exploded['Ratings'].min()), float(df_exploded['Ratings'].max())
    rating_filter = st.sidebar.slider("Minimum Rating:", min_value=min_rating, max_value=max_rating, value=min_rating, step=0.1)

    vote_filter = st.sidebar.number_input("Minimum Voting Count:", min_value=0, value=10000, step=1000)

    duration_option = st.sidebar.selectbox("Select Duration Range:",["All", "< 2 hrs", "2-3 hrs", "> 3 hrs"])

    filtered_df = df_exploded.copy()

    if selected_genres:
        filtered_df = filtered_df[filtered_df['Genre'].isin(selected_genres)]

    filtered_df = filtered_df[filtered_df['Ratings'] >= rating_filter]
    filtered_df = filtered_df[filtered_df['Votes'] >= vote_filter]

    if duration_option == "< 2 hrs":
        filtered_df = filtered_df[filtered_df['Duration'] < 120]
    elif duration_option == "2-3 hrs":
        filtered_df = filtered_df[(filtered_df['Duration'] >= 120) & (filtered_df['Duration'] <= 180)]
    elif duration_option == "> 3 hrs":
        filtered_df = filtered_df[filtered_df['Duration'] > 180]

    st.subheader("Filtered Movie Results")
    st.write(f"Showing {len(filtered_df)} movie(s) after applying filters.")

    if filtered_df.empty:
        st.warning("No movies found matching your filter criteria. Try adjusting the filters.")

    for idx, row in filtered_df.iterrows():
        st.markdown(f"""
        <div style='border:1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 10px;'>
            <h4 style='margin: 0;'>{row['Title']}</h4>
            <p style='margin: 5px 0;'><strong>Genre:</strong> {row['Genre']} | <strong>Rating:</strong> {row['Ratings']} | <strong>Votes:</strong> {int(row['Votes'])} | <strong>Duration:</strong> {row['Duration']}</p>
        </div>
        """, unsafe_allow_html=True)
