import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import json
from datetime import datetime

def calculate_age(dob):
    today = datetime.today()
    birth_date = datetime.strptime(dob, '%Y-%m-%d')
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def get_age_group(age):
    if age < 18:
        return 'Under 18'
    elif age < 30:
        return '18-29'
    elif age < 50:
        return '30-49'
    elif age < 65:
        return '50-64'
    else:
        return '65+'


def generate_bar_chart(categories, user_values, cluster_values):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=list(categories), y=list(user_values), name='User Spending', marker_color='blue'))
    fig.add_trace(go.Bar(x=list(categories), y=list(cluster_values), name='Cluster Avg', marker_color='green'))
    fig.update_layout(
        title='User Spending vs Cluster Average',
        xaxis_title='Category',
        yaxis_title='Amount',
        barmode='group'
    )
    # return fig.to_dict()  # Return as dictionary
    return fig.to_dict()

def generate_geographical_map(clustered_df):
    try:
        # Create Plotly map with clustering results
        fig = px.scatter_geo(
            clustered_df,
            lat='Latitude',
            lon='Longitude',
            color='Cluster',
            hover_name='Address',
            title="Spending Personality Clusters by Location",
            projection="natural earth"
        )
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)()
    
    except Exception as e:
        print(f"Error generating geographical map: {str(e)}")
        return {}

def spending_personality(user_df, demographic_df, n_clusters=3):
    cluster_label = "Unknown"
    insights = []

    try:
        # Transform demographic data to long format for compatibility
        demographic_long = demographic_df.melt(id_vars=['SpenderType'], var_name='Category', value_name='Amount')
        print("\nDemographic Data (Long Format):")
        print(demographic_long.head())

        # Group demographic data by spender type and category
        demographic_grouped = demographic_long.groupby(['SpenderType', 'Category']).agg({'Amount': 'mean'}).unstack().fillna(0)
        demographic_grouped.columns = demographic_grouped.columns.droplevel(0)
        print("\nDemographic Grouped Data:")
        print(demographic_grouped)

        # Group user data similarly
        user_grouped = user_df.groupby(['Category']).agg({'Amount': 'sum'}).T
        print("\nUser Grouped Data:")
        print(user_grouped)

        # Align columns by merging and filling missing categories with 0
        all_categories = sorted(set(demographic_grouped.columns).union(set(user_grouped.columns)))
        demographic_grouped = demographic_grouped.reindex(columns=all_categories, fill_value=0)
        user_grouped = user_grouped.reindex(columns=all_categories, fill_value=0)

        # Normalize the base data
        scaler = StandardScaler()
        normalized_demo = scaler.fit_transform(demographic_grouped)

        # Clustering using K-Means
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(normalized_demo)
        demographic_grouped['Cluster'] = cluster_labels

        # Cluster centroids in normalized form
        centroids = pd.DataFrame(kmeans.cluster_centers_, columns=all_categories)

        normalized_user = scaler.transform(user_grouped)

        # Predict the closest cluster for user data based on centroids
        distances = np.linalg.norm(centroids.values - normalized_user, axis=1)
        user_cluster = np.argmin(distances)

        # Denormalize the centroids to get back to raw values
        centroids_denormalized = pd.DataFrame(scaler.inverse_transform(centroids), columns=all_categories)
        print("\nCentroids (Denormalized):")
        print(centroids_denormalized)

        # Define cluster names
        cluster_names = ["Low Spender", "Moderate Spender", "High Spender"]
        cluster_label = cluster_names[user_cluster] if user_cluster < len(cluster_names) else f"Cluster {user_cluster}"
        
        # Generate insights
        for category in user_grouped.columns:
            user_spending = user_grouped[category].values[0]
            cluster_avg = centroids_denormalized.iloc[int(user_cluster)][category]

            if user_spending > cluster_avg:
                difference = user_spending - cluster_avg
                insights.append(f"You spend {difference:.2f} more on {category} compared to your group average.")
            elif user_spending < cluster_avg:
                difference = cluster_avg - user_spending
                insights.append(f"You spend {difference:.2f} less on {category} compared to your group average.")
            else:
                insights.append(f"Your spending on {category} matches your group average.")

        # Plotly Charts
        bar_chart = generate_bar_chart(user_grouped.columns, user_grouped.values[0], centroids_denormalized.iloc[int(user_cluster)].values)

        return cluster_label, insights, bar_chart

    except Exception as e:
        print(f"\n[Error] Clustering failed at step: {str(e)}")
        return "Error", ["Clustering failed."], {}, {}