import pandas as pd
from sklearn.neighbors import NearestNeighbors

# Sample data
data = [
    {"destination": "Bali", "category": "beach", "popularity": 9},
    {"destination": "Paris", "category": "city", "popularity": 10},
    {"destination": "Tokyo", "category": "city", "popularity": 8},
    {"destination": "Alps", "category": "mountain", "popularity": 7},
]

df = pd.DataFrame(data)

def recommend(destination, category=None):
    # Filter by category if provided
    if category:
        df_filtered = df[df["category"] == category]
    else:
        df_filtered = df

    # Model setup
    model = NearestNeighbors(n_neighbors=2, metric="cosine")
    features = pd.get_dummies(df_filtered[["category", "popularity"]])
    model.fit(features)

    # Find recommendations
    query = df_filtered[df_filtered["destination"] == destination]
    distances, indices = model.kneighbors(pd.get_dummies(query[["category", "popularity"]]))
    recommendations = df_filtered.iloc[indices[0]].to_dict("records")
    return recommendations
