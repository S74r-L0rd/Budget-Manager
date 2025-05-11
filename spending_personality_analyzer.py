import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import json

# Plot bar chart for spending personality
def generate_bar_chart(categories, user_values, cluster_values):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=list(categories), y=list(user_values), name='Your Spending', marker_color='#344e41'))
    fig.add_trace(go.Bar(x=list(categories), y=list(cluster_values), name='Personality Group Avg', marker_color='#588157'))
    fig.update_layout(
        title='Your Spending vs Your Personality Group Average',
        xaxis_title='Category',
        yaxis_title='Amount',
        barmode='group'
    )
    return fig.to_dict()

#  Generate insights for your spending and personality group
def generate_insights(user_grouped, centroids_denormalized, user_cluster):
    insights = []
    for category in user_grouped.columns:
        user_spending = user_grouped[category].values[0]
        cluster_avg = centroids_denormalized.iloc[int(user_cluster)][category]

        difference = user_spending - cluster_avg
        percentage = int((abs(difference) / max(cluster_avg, 1)) * 100)

        if difference > 0:
            message = f"${difference:.2f} more spent on {category} compared to your group average"
            insights.append({"category": category, "message": message, "difference": difference, "percentage": percentage})
        elif difference < 0:
            message = f"${abs(difference):.2f} less spent on {category} compared to your group average"
            insights.append({"category": category, "message": message, "difference": difference, "percentage": percentage})
        else:
            message = f"Spending on {category} matches your group average"
            insights.append({"category": category, "message": message, "difference": 0, "percentage": 0})

    return insights

# Implement cluster for spending personality (Spender Type)
# Main Cluster code
def spending_personality(user_df, demographic_df, n_clusters=3):
    cluster_label = "Unknown"
    insights = []

    try:
        # Transform demographic data to long format for compatibility
        demographic_long = demographic_df.melt(id_vars=['SpenderType'], var_name='Category', value_name='Amount')

        # Group demographic data by spender type and category
        demographic_grouped = demographic_long.groupby(['SpenderType', 'Category']).agg({'Amount': 'mean'}).unstack().fillna(0)
        demographic_grouped.columns = demographic_grouped.columns.droplevel(0)

        # Group user data
        user_grouped = user_df.groupby(['Category']).agg({'Amount': 'sum'}).T

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

        # Define cluster names
        cluster_names = ["Low Spender", "Moderate Spender", "High Spender"]
        cluster_label = cluster_names[user_cluster] if user_cluster < len(cluster_names) else f"Cluster {user_cluster}"
        
        insights = generate_insights(user_grouped, centroids_denormalized, user_cluster)
        bar_chart = generate_bar_chart(user_grouped.columns, user_grouped.values[0], centroids_denormalized.iloc[int(user_cluster)].values)

        return cluster_label, insights, bar_chart

    except Exception as e:
        print(f"\n[Error] Clustering failed at step: {str(e)}")
        return "Error", ["Clustering failed."], {}, {}