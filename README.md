# IMDB-2024-Project-01-
IMDb 2024 Movie Analysis – Streamlit App

This project is a data analysis and visualization web application built using Streamlit, which analyzes IMDb movie data for the year 2024. It connects to a MySQL database, retrieves movie data (including titles, genres, ratings, votes, and durations), and offers interactive visualizations and dynamic filters for deep insights into the movie landscape.

Features:

1. Visualizations Page:
   
Top 10 movies by rating and votes
Genre distribution bar chart
Average duration by genre (horizontal bar)
Average votes per genre
Ratings distribution histogram with KDE
Top-rated movie per genre (table)
Most popular genres by total votes (pie chart)
Shortest and longest movies (table)
Ratings heatmap by genre
Scatter plot showing correlation between votes and ratings

2. Interactive Filter Page

Filter movies by:
Genre(s)
Minimum rating (slider)
Minimum votes (input)
Duration range (<2 hrs, 2-3 hrs, >3 hrs)
Filtered movie cards with title, genre, rating, votes, and duration

Tech Stack:
Frontend: Streamlit
Backend: MySQL with SQLAlchemy
Visualization Libraries: Plotly, Seaborn, Matplotlib, Pandas
