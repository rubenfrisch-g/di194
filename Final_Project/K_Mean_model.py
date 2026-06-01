
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
 
from Final_project import FEATURE_COLS, load_data, get_feature_matrix
 
 
def train_kmeans(X: np.ndarray, n_clusters: int = 3) -> KMeans:
    """
    Entraîne le modèle K-Means avec n_clusters groupes.
    3 groupes : Elite / Mid / Accessible
    """
    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    model.fit(X)
    return model
 
 
def assign_cluster_labels(df: pd.DataFrame, labels: np.ndarray) -> pd.DataFrame:
    """
    Ajoute les clusters au DataFrame et les renomme
    en Elite / Mid / Accessible selon le score moyen.
    """
    df = df.copy()
    df["cluster"] = labels
 
    # Calculer le score moyen par cluster
    cluster_scores = df.groupby("cluster")["score_numeric"].mean().sort_values(ascending=False)
 
    # Renommer selon le niveau : meilleur score = Elite
    cluster_names = {
        cluster_scores.index[0]: "Elite",
        cluster_scores.index[1]: "Mid",
        cluster_scores.index[2]: "Accessible",
    }
 
    df["cluster_name"] = df["cluster"].map(cluster_names)
    return df
 
 
if __name__ == "__main__":
    # 1. Charger les données
    df = load_data()
    X, scaler = get_feature_matrix(df)
 
    # 2. Entraîner K-Means
    print("Entraînement K-Means (k=3)...")
    model = train_kmeans(X, n_clusters=3)
 
    # 3. Assigner les labels
    df = assign_cluster_labels(df, model.labels_)
 
    # 4. Résultats
    print("\nRépartition des clusters :")
    print(df["cluster_name"].value_counts())
 
    print("\nExemples par cluster :")
    for name in ["Elite", "Mid", "Accessible"]:
        print(f"\n--- {name} ---")
        sample = df[df["cluster_name"] == name][["Institution Name", "Location", "score_numeric"]].head(5)
        print(sample.to_string(index=False))