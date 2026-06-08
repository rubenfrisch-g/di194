import warnings
warnings.filterwarnings("ignore")
 
import os
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
 
from Final_project import load_data, get_feature_matrix, FEATURE_COLS
from K_Mean_model import train_kmeans, assign_cluster_labels
 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
 
CONTINENT_COUNTRIES = {
    "Europe": ["UK", "DE", "FR", "IT", "ES", "NL", "BE", "CH", "SE", "DK", "NO", "FI", "AT", "PL", "CZ", "PT", "IE", "GR", "HU", "RO"],
    "North America": ["US", "CA", "MX"],
    "Asia": ["CN", "JP", "KR", "SG", "HK", "IN", "TW", "MY", "TH", "ID"],
    "Oceania": ["AU", "NZ"],
    "Middle East": ["IL", "AE", "SA", "QA", "TR"],
    "South America": ["BR", "CL", "AR", "CO"],
    "Africa": ["ZA", "EG", "MA"],
}
 
ALL_LANGUAGES = [
    'English', 'French', 'German', 'Spanish', 'Italian',
    'Dutch', 'Swedish', 'Norwegian', 'Danish', 'Finnish',
    'Japanese', 'Korean', 'Chinese', 'Arabic', 'Portuguese',
]
 
 
def get_student_level(grade: float, scale: int) -> str:
    ratio = grade / scale * 100
    if ratio >= 93:
        return "World Elite"
    elif ratio >= 83:
        return "Elite"
    elif ratio >= 76:
        return "High Mid"
    elif ratio >= 63:
        return "Mid"
    elif ratio >= 50:
        return "Accessible"
    else:
        return "Open"
 
 
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
    path_main: str = None,
    path_subjects: str = None,
    path_costs: str = None,
    path_websites: str = None,
) -> pd.DataFrame:
    if path_main is None:
        path_main = os.path.join(BASE_DIR, "qs-world-rankings-2025.csv")
    if path_subjects is None:
        path_subjects = os.path.join(BASE_DIR, "qs_subjects.csv")
    if path_costs is None:
        path_costs = os.path.join(BASE_DIR, "university_costs_complete.csv")
    if path_websites is None:
        path_websites = os.path.join(BASE_DIR, "university_websites.csv")
 
    df_main     = load_data(path_main)
    df_subjects = pd.read_csv(path_subjects)
    df_costs    = pd.read_csv(path_costs)
    df_websites = pd.read_csv(path_websites)
 
    df = df_main.merge(df_subjects, on="Institution Name", how="left")
    if "Location_x" in df.columns:
        df = df.rename(columns={"Location_x": "Location"})
        df = df.drop(columns=["Location_y"], errors="ignore")
 
    df = df.merge(
        df_costs[["Institution Name", "Tuition_USD", "Total_Annual_USD",
                  "Rent_USD", "Languages", "Level", "Budget_Category"]],
        on="Institution Name", how="left"
    )
    df = df.merge(df_websites[["Institution Name", "Website"]], on="Institution Name", how="left")
 
    return df
 
 
def filter_universities(
    df: pd.DataFrame,
    subject: str = None,
    continents: list = None,
    languages: list = None,
    level: str = None,
) -> pd.DataFrame:
    filtered = df.copy()
 
    if subject and subject != "Tous les domaines" and subject != "All fields":
        filtered = filtered[filtered["Subject"] == subject]
 
    if continents and "Tous les continents" not in continents and "All continents" not in continents:
        all_countries = []
        for continent in continents:
            all_countries += CONTINENT_COUNTRIES.get(continent, [])
        filtered = filtered[filtered["Location"].isin(all_countries)]
 
    if languages:
        def has_language(lang_str):
            if pd.isna(lang_str) or str(lang_str) == "nan":
                return True
            for lang in languages:
                if lang.lower() in str(lang_str).lower():
                    return True
            return False
        filtered = filtered[filtered["Languages"].apply(has_language)]
 
    if level and level != "Tous les niveaux" and level != "All levels":
        def has_level(level_str):
            if pd.isna(level_str) or str(level_str) == "nan":
                return True
            return level.lower() in str(level_str).lower()
        filtered = filtered[filtered["Level"].apply(has_level)]
 
    return filtered.drop_duplicates(subset=["Institution Name"]).reset_index(drop=True)
 
 
def recommend(
    grade: float,
    scale: int,
    subject: str,
    continents: list,
    languages: list = None,
    level: str = None,
    n_recommendations: int = 5,
    path_main: str = None,
    path_subjects: str = None,
    path_costs: str = None,
    path_websites: str = None,
) -> dict:
    student_level = get_student_level(grade, scale)
 
    df = load_merged_data(path_main, path_subjects, path_costs, path_websites)
 
    X_all, scaler = get_feature_matrix(df.drop_duplicates(subset=["Institution Name"]))
    df_unique = df.drop_duplicates(subset=["Institution Name"]).reset_index(drop=True)
    kmeans = train_kmeans(X_all, n_clusters=6)
    df_unique = assign_cluster_labels(df_unique, kmeans.labels_)
 
    cluster_map = df_unique.set_index("Institution Name")["cluster_name"].to_dict()
    df["cluster_name"] = df["Institution Name"].map(cluster_map)
 
    df_filtered = filter_universities(df, subject, continents, languages, level)
 
    if len(df_filtered) == 0:
        return {"level": student_level, "recommendations": [], "error": "No university found with these criteria."}
 
    df_cluster = df_filtered[df_filtered["cluster_name"] == student_level].copy()
 
    if len(df_cluster) == 0:
        return {"level": student_level, "recommendations": [], "error": f"No {student_level} university found. Try broadening your search."}
 
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
 