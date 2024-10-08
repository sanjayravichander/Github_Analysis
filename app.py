import streamlit as st
import pandas as pd
import plotly.express as px

# Load your dataset
df = pd.read_csv('github_repos.csv')  # Replace with your actual dataset path
df['Creation_Date'] = pd.to_datetime(df['Creation_Date'])  # Ensure creation date is datetime

# Set the title of the app
st.title("🔍 GitHub Repository Analysis")
st.markdown("This app provides Insights into various GitHub repositories based on programming languages, forks, stars, licenses, and more.")

# Sidebar for user input
st.sidebar.header("Filters")
selected_language = st.sidebar.multiselect(
    "Select Programming Languages:",
    options=df['Programming_Language'].unique(),
    default=df['Programming_Language'].unique()
)

# Filter the dataframe based on user input
df_filtered = df[df['Programming_Language'].isin(selected_language)]

# Top 10 most forked repositories
top_forked = df_filtered[['Repository_Name', 'Number_of_Forks']].sort_values(by='Number_of_Forks',ascending=False).head(10)
st.subheader("📈 Top 10 Most Forked Repositories")
fig_forked = px.bar(top_forked, x='Number_of_Forks', y='Repository_Name',
                     title='Top 10 Most Forked Repositories', color='Number_of_Forks',
                     color_continuous_scale=px.colors.sequential.Rainbow)
st.plotly_chart(fig_forked)

# Top 10 most Bookmarked repositories
top_star = df_filtered[['Repository_Name', 'Number_of_Stars']].sort_values(by='Number_of_Stars', ascending=False).head(10)
st.subheader("📈 Top 10 Most Bookmarked Repositories")
fig_star = px.bar(top_star, x='Number_of_Stars', y='Repository_Name',
                     title='Top 10 Most Bookmarked Repositories', color='Number_of_Stars',
                     color_continuous_scale=px.colors.sequential.Rainbow)
st.plotly_chart(fig_star)

# Distribution of forks across repositories
st.subheader("📊 Distribution of Forks Across Repositories")
fig_forks_dist = px.histogram(df_filtered, x='Number_of_Forks', nbins=20,
                               title='Distribution of Forks Across Repositories',
                               histnorm='probability density')
st.plotly_chart(fig_forks_dist)


# Top 10 most used license types
top_licenses = df_filtered['License_Type'].value_counts().head(10)
fig_licenses = px.bar(x=top_licenses.index, y=top_licenses.values,
                      title='Top 10 Most Used License Types',
                      labels={'x': 'License Type', 'y': 'Number of Repositories'},
                      color=top_licenses.values, color_continuous_scale=px.colors.sequential.Viridis)
st.plotly_chart(fig_licenses)

# Pie chart for programming language distribution
st.subheader("📋 Programming Language Distribution")
top_languages = df_filtered['Programming_Language'].value_counts().head(10)
fig_languages = px.pie(names=top_languages.index, values=top_languages.values,
                        title='Programming Language Distribution', 
                        color_discrete_sequence=px.colors.qualitative.Plotly)
st.plotly_chart(fig_languages)

# Distribution of stars across repositories
st.subheader("⭐ Distribution of Stars Across Repositories")
fig_stars_dist = px.histogram(df_filtered, x='Number_of_Stars', nbins=20,
                               title='Distribution of Stars Across Repositories',
                               histnorm='probability density')
st.plotly_chart(fig_stars_dist)

# Repositories creation over time
df_filtered['Creation_Year'] = df_filtered['Creation_Date'].dt.year
repos_by_year = df_filtered['Creation_Year'].value_counts().sort_index()
fig_creation_over_time = px.line(x=repos_by_year.index, y=repos_by_year.values,
                                  title='Number of Repositories Created Over Time',
                                  labels={'x': 'Year', 'y': 'Number of Repositories'}, markers=True)
st.plotly_chart(fig_creation_over_time)

# Stars vs Forks scatter plot
st.subheader("🌟 Stars vs Forks by Programming Language")
fig_scatter = px.scatter(df_filtered, x='Number_of_Stars', y='Number_of_Forks',
                          color='Programming_Language', title='Stars vs Forks by Programming Language')
st.plotly_chart(fig_scatter)

# Top 10 repositories with most open issues
top_issues = df_filtered[['Repository_Name', 'Number_of_Open_Issues']].sort_values(by='Number_of_Open_Issues',ascending=False).head(10)
st.subheader("📝 Top 10 Repositories with Most Open Issues")
fig_issues = px.bar(top_issues, x='Number_of_Open_Issues', y='Repository_Name',
                     title='Top 10 Repositories with Most Open Issues',
                     color='Number_of_Open_Issues', color_continuous_scale=px.colors.sequential.Plasma)
st.plotly_chart(fig_issues)

# Adjusting the layout
st.sidebar.header("About")
st.sidebar.info("This app visualizes GitHub repository data. Select programming languages from the sidebar to filter the results.")
