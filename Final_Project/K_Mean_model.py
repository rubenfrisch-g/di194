
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
 
from Final_project import FEATURE_COLS, load_data, get_feature_matrix
 
 
def train_kmeans(X: np.ndarray, n_clusters: int = 6) -> KMeans:
    """
    Entraîne le modèle K-Means avec 6 groupes :
    World Elite / Elite / High Mid / Mid / Accessible / Open
    """
    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    model.fit(X)
    return model
 
 
def assign_cluster_labels(df: pd.DataFrame, labels: np.ndarray) -> pd.DataFrame:
    """
    Ajoute les clusters au DataFrame et les renomme selon le score moyen.
    """
    df = df.copy()
    df["cluster"] = labels
 
    cluster_scores = df.groupby("cluster")["score_numeric"].mean().sort_values(ascending=False)
 
    cluster_names = {}
    level_names = ["World Elite", "Elite", "High Mid", "Mid", "Accessible", "Open"]
    for i, idx in enumerate(cluster_scores.index):
        cluster_names[idx] = level_names[i]
 
    df["cluster_name"] = df["cluster"].map(cluster_names)
    return df
 
 
if __name__ == "__main__":
    df = load_data()
    X, scaler = get_feature_matrix(df)
 
    print("Entraînement K-Means (k=6)...")
    model = train_kmeans(X, n_clusters=6)
    df = assign_cluster_labels(df, model.labels_)
 
    print("\nRépartition des clusters :")
    print(df["cluster_name"].value_counts())
 
    print("\nExemples par cluster :")
    for name in ["World Elite", "Elite", "High Mid", "Mid", "Accessible", "Open"]:
        print(f"\n--- {name} ---")
        sample = df[df["cluster_name"] == name][["Institution Name", "Location", "score_numeric"]].head(3)
        print(sample.to_string(index=False))