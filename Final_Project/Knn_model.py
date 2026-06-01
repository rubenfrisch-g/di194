import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

from Final_project import load_data, get_feature_matrix, FEATURE_COLS
from K_Mean_model import train_kmeans, assign_cluster_labels

CONTINENT_COUNTRIES = {
    "Europe": ["UK", "DE", "FR", "IT", "ES", "NL", "BE", "CH", "SE", "DK", "NO", "FI", "AT", "PL", "CZ", "PT", "IE", "GR", "HU", "RO"],
    "North America": ["US", "CA", "MX"],
    "Asia": ["CN", "JP", "KR", "SG", "HK", "IN", "TW", "MY", "TH", "ID"],
    "Oceania": ["AU", "NZ"],
    "Middle East": ["IL", "AE", "SA", "QA", "TR"],
    "South America": ["BR", "CL", "AR", "CO"],
    "Africa": ["ZA", "EG", "MA"],
}

BUDGET_RANGES = {
    'Low (< $5k/year)':        (0, 5000),
    'Medium ($5k-$20k/year)':  (5000, 20000),
    'High ($20k-$40k/year)':   (20000, 40000),
    'Very High (> $40k/year)': (40000, 999999),
}

ALL_LANGUAGES = [
    'English', 'French', 'German', 'Spanish', 'Italian',
    'Dutch', 'Swedish', 'Norwegian', 'Danish', 'Finnish',
    'Japanese', 'Korean', 'Chinese', 'Arabic', 'Portuguese',
]


def get_student_level(grade: float, scale: int) -> str:
    ratio = grade / scale * 100
    if ratio >= 80:
        return "Elite"
    elif ratio >= 65:
        return "Mid"
    else:
        return "Accessible"


def grade_to_profile(grade: float, scale: int = 20) -> dict:
    ratio = grade / scale
    return {
        "Academic Reputation":    ratio * 100,
        "Employer Reputation":    ratio * 100,
        "Faculty Student":        ratio * 80,
        "Citations per Faculty":  ratio * 70,
        "International Faculty":  50,
        "International Students": 50,
        "Employment Outcomes":    ratio * 90,
    }


def load_merged_data(
    path_main: str = "qs-world-rankings-2025.csv",
    path_subjects: str = "qs_subjects.csv",
    path_costs: str = "university_costs_complete.csv",
    path_websites: str = "university_websites.csv",
) -> pd.DataFrame:
    df_main = load_data(path_main)
    df_subjects = pd.read_csv(path_subjects)
    df_costs = pd.read_csv(path_costs)
    df_websites = pd.read_csv(path_websites)

    # Merge avec les sujets
    df = df_main.merge(df_subjects, on="Institution Name", how="left")
    if "Location_x" in df.columns:
        df = df.rename(columns={"Location_x": "Location"})
        df = df.drop(columns=["Location_y"], errors="ignore")

    # Merge avec les couts
    df = df.merge(
        df_costs[["Institution Name", "Tuition_USD", "Total_Annual_USD",
                  "Rent_USD", "Languages", "Level", "Budget_Category"]],
        on="Institution Name",
        how="left"
    )

    # Merge avec les sites web
    df = df.merge(df_websites[["Institution Name", "Website"]], on="Institution Name", how="left")

    return df


def filter_universities(
    df: pd.DataFrame,
    subject: str = None,
    continents: list = None,
    languages: list = None,
    level: str = None,
    budget: str = None,
) -> pd.DataFrame:
    filtered = df.copy()

    if subject and subject != "Tous les domaines":
        filtered = filtered[filtered["Subject"] == subject]

    if continents and "Tous les continents" not in continents:
        all_countries = []
        for continent in continents:
            all_countries += CONTINENT_COUNTRIES.get(continent, [])
        filtered = filtered[filtered["Location"].isin(all_countries)]

    if languages:
        def has_language(lang_str):
            if pd.isna(lang_str):
                return True
            for lang in languages:
                if lang.lower() in lang_str.lower():
                    return True
            return False
        filtered = filtered[filtered["Languages"].apply(has_language)]

    if level and level != "Tous les niveaux":
        def has_level(level_str):
            if pd.isna(level_str):
                return True
            return level.lower() in level_str.lower()
        filtered = filtered[filtered["Level"].apply(has_level)]

    if budget and budget != "Tous les budgets":
        min_b, max_b = BUDGET_RANGES.get(budget, (0, 999999))
        budget_filtered = filtered[
            filtered["Tuition_USD"].isna() |
            ((filtered["Tuition_USD"] >= min_b) & (filtered["Tuition_USD"] <= max_b))
        ]
        if len(budget_filtered) > 0:
            filtered = budget_filtered

    return filtered.drop_duplicates(subset=["Institution Name"]).reset_index(drop=True)


def recommend(
    grade: float,
    scale: int,
    subject: str,
    continents: list,
    languages: list = None,
    level: str = None,
    budget: str = None,
    n_recommendations: int = 5,
    path_main: str = "qs-world-rankings-2025.csv",
    path_subjects: str = "qs_subjects.csv",
    path_costs: str = "university_costs_complete.csv",
) -> dict:
    student_level = get_student_level(grade, scale)

    df = load_merged_data(path_main, path_subjects, path_costs)

    X_all, scaler = get_feature_matrix(df.drop_duplicates(subset=["Institution Name"]))
    df_unique = df.drop_duplicates(subset=["Institution Name"]).reset_index(drop=True)
    kmeans = train_kmeans(X_all, n_clusters=3)
    df_unique = assign_cluster_labels(df_unique, kmeans.labels_)

    cluster_map = df_unique.set_index("Institution Name")["cluster_name"].to_dict()
    df["cluster_name"] = df["Institution Name"].map(cluster_map)

    df_filtered = filter_universities(df, subject, continents, languages, level, budget)

    if len(df_filtered) == 0:
        return {"level": student_level, "recommendations": [], "error": "Aucune universite trouvee avec ces criteres."}

    df_cluster = df_filtered[df_filtered["cluster_name"] == student_level].copy()

    if len(df_cluster) == 0:
        return {"level": student_level, "recommendations": [], "error": f"Aucune universite niveau {student_level} trouvee."}

    profile = grade_to_profile(grade, scale)
    profile_df = pd.DataFrame([profile])[FEATURE_COLS]
    profile_scaled = scaler.transform(profile_df)

    X_cluster = scaler.transform(df_cluster[FEATURE_COLS].values)
    k = min(n_recommendations, len(df_cluster))
    knn = NearestNeighbors(n_neighbors=k, metric="cosine")
    knn.fit(X_cluster)
    distances, indices = knn.kneighbors(profile_scaled)

    cols = ["Institution Name", "Location", "score_numeric", "rank_numeric",
            "cluster_name", "Subject", "Languages", "Level", "Website"]
    existing_cols = [c for c in cols if c in df_cluster.columns]
    recommended = df_cluster.iloc[indices[0]][existing_cols].copy()
    recommended["distance"] = distances[0]
    recommended = recommended.sort_values("distance")

    return {"level": student_level, "recommendations": recommended.to_dict(orient="records")}


if __name__ == "__main__":
    print("Test — 16/20, Computer Science, Europe, English, Master...")
    results = recommend(
        grade=16, scale=20, subject="Computer Science",
        continents=["Europe"], languages=["English"],
        level="Master", budget="Medium ($5k-$20k/year)",
        n_recommendations=5,
    )
    print(f"Niveau: {results['level']}")
    if "error" in results:
        print("Erreur:", results["error"])
    else:
        for u in results["recommendations"]:
            print(f"  {u['Institution Name']} ({u['Location']}) | Score: {u['score_numeric']:.1f} | ${u.get('Tuition_USD', 'N/A'):,.0f}/an | {u.get('Languages', 'N/A')}")