import pandas as pd
import numpy as np

FEATURE_COLS = [
    "Academic Reputation",
    "Employer Reputation",
    "Faculty Student",
    "Citations per Faculty",
    "International Faculty",
    "International Students",
    "Employment Outcomes",
]

def load_data(path: str = "qs-world-rankings-2025.csv") -> pd.DataFrame:
    """
    Charge et nettoie le dataset QS World Rankings 2025.
    Retourne un DataFrame prêt pour les modèles ML.
    """
    df = pd.read_csv(
        path,
        encoding="utf-8-sig",
        na_values=["-", "", " "]
    )

    # ── Nettoyage du rank ─────────────────────────────────────────
    def parse_rank(val):
        val = str(val).strip()
        if "-" in val:
            return int(val.split("-")[0])
        try:
            return int(val)
        except ValueError:
            return np.nan

    df["rank_numeric"] = df["2025 Rank"].apply(parse_rank)

    # ── Nettoyage du score global ─────────────────────────────────
    def parse_score(val):
        val = str(val).strip()
        if "-" in val:
            parts = val.split("-")
            try:
                return (float(parts[0]) + float(parts[1])) / 2
            except ValueError:
                return np.nan
        try:
            return float(val)
        except ValueError:
            return np.nan

    df["score_numeric"] = df["QS Overall Score"].apply(parse_score)

    # ── Remplir les valeurs manquantes par la médiane ─────────────
    for col in FEATURE_COLS:
        median = df[col].median()
        df[col] = df[col].fillna(median)

    # ── Garder uniquement les colonnes utiles ─────────────────────
    keep_cols = [
        "Institution Name",
        "Location",
        "Location Full",
        "Size",
        "rank_numeric",
        "score_numeric",
    ] + FEATURE_COLS

    df = df[keep_cols].copy()

    print("Avant suppression :", len(df))
    df = df.dropna(subset=["rank_numeric", "score_numeric"])
    print("Après suppression :", len(df))

    df = df.reset_index(drop=True)
    return df


def get_feature_matrix(df: pd.DataFrame):
    """Retourne la matrice de features normalisée pour KNN et K-Means."""
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    X = scaler.fit_transform(df[FEATURE_COLS])
    return X, scaler


if __name__ == "__main__":
    df = load_data()
    print(f"\nDataset chargé : {df.shape[0]} universités, {df.shape[1]} colonnes")
    print(f"Valeurs manquantes : {df.isnull().sum().sum()}")
    print(f"\nAperçu :\n{df.head(3).to_string()}")