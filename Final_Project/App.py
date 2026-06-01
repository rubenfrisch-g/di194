import streamlit as st
import pandas as pd
from Knn_model import recommend, CONTINENT_COUNTRIES, ALL_LANGUAGES, get_student_level
from pdf_export import generate_pdf
 
st.set_page_config(page_title="University Recommender", page_icon="🎓", layout="wide")
 
st.title("🎓 University Recommender")
st.caption("Find the universities that match your profile using Machine Learning")
st.divider()
 
with st.sidebar:
    st.header("👤 Your Profile")
 
    # Grade
    st.subheader("📊 Academic Results")
    scale = st.selectbox("Grading system", [20, 100, 4], index=0)
    grade = st.slider(f"Your grade (out of {scale})", 0.0, float(scale), float(scale) * 0.7, 0.5)
    level_student = get_student_level(grade, scale)
    colors = {"Elite": "🔴", "Mid": "🔵", "Accessible": "🟢"}
    st.caption(f"**{grade}/{scale}** ({grade/scale*100:.0f}%) → {colors[level_student]} **{level_student}**")
 
    st.divider()
 
    # Study level
    st.subheader("🎓 Desired Study Level")
    level = st.selectbox("Level", ["All levels", "Bachelor", "Master", "PhD"])
 
    st.divider()
 
    # Subject
    st.subheader("📚 Field of Study")
    subjects = [
        "All fields", "Engineering & Technology", "Computer Science",
        "Natural Sciences", "Life Sciences & Medicine", "Business & Management",
        "Social Sciences & Management", "Arts & Humanities", "Law",
    ]
    subject = st.selectbox("Desired field", subjects)
 
    st.divider()
 
    # Languages
    st.subheader("🗣️ Languages Spoken")
    languages = st.multiselect(
        "Languages you speak",
        options=ALL_LANGUAGES,
        default=["English"],
        help="We will filter universities that teach in these languages"
    )
 
    st.divider()
 
    # Location
    st.subheader("🌍 Location")
    continent_options = ["All continents"] + list(CONTINENT_COUNTRIES.keys())
    continents = st.multiselect(
        "Desired continents",
        options=continent_options,
        default=["All continents"],
    )
    if not continents:
        continents = ["All continents"]
 
    st.divider()
 
    n_reco = st.slider("Number of recommendations", 1, 10, 5)
    run = st.button("🔍 Find my universities", type="primary", use_container_width=True)
 
 
# Home page
if not run:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Step 1**\n\nEnter your grade, study level and languages")
    with col2:
        st.info("**Step 2**\n\nChoose your field of study")
    with col3:
        st.info("**Step 3**\n\nSelect one or more continents")
 
    st.markdown("""
    ### How does it work?
    This system uses two Machine Learning algorithms :
 
    - **K-Means** groups universities into 3 levels based on your grade :
        - 🔴 **Elite** → 80% and above
        - 🔵 **Mid** → between 65% and 80%
        - 🟢 **Accessible** → below 65%
 
    - **KNN (K-Nearest Neighbors)** finds the universities most suited to your profile within your level.
 
    Recommendations take into account :
    - Your academic results
    - Your field of study
    - Your languages
    - Your desired study level (Bachelor / Master / PhD)
    - Your desired continent(s)
    """)
 
# Results
else:
    # Map "All levels" and "All continents" back for the model
    level_param = None if level == "All levels" else level
    continents_param = ["Tous les continents"] if "All continents" in continents else continents
 
    with st.spinner("Analysing your profile..."):
        results = recommend(
            grade=grade,
            scale=scale,
            subject=subject if subject != "All fields" else "Tous les domaines",
            continents=continents_param,
            languages=languages if languages else None,
            level=level_param,
            n_recommendations=n_reco,
        )
 
    if "error" in results:
        st.error(f"❌ {results['error']}")
        st.info("Try broadening your search: fewer filters or more continents.")
    else:
        # Profile summary
        st.subheader("📋 Your Profile")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Grade", f"{grade}/{scale} ({grade/scale*100:.0f}%)")
        c2.metric("Level", f"{colors[level_student]} {level_student}")
        c3.metric("Field", subject.split("&")[0].strip())
        c4.metric("Languages", ", ".join(languages) if languages else "All")
 
        st.divider()
 
        unis = results["recommendations"]
        level_config = {
            "Elite":      {"emoji": "🔴", "desc": "World's best universities — highly selective"},
            "Mid":        {"emoji": "🔵", "desc": "Very good universities — selective"},
            "Accessible": {"emoji": "🟢", "desc": "Accessible universities — good quality/accessibility ratio"},
        }
        lvl = results["level"]
        config = level_config[lvl]
 
        st.subheader(f"{config['emoji']} Recommended Universities — {lvl} Level")
        st.caption(config["desc"])
 
        if not unis:
            st.warning("No universities found. Try broadening your search.")
        else:
            df_result = pd.DataFrame(unis)
            rename = {
                "Institution Name": "University",
                "Location":         "Country",
                "score_numeric":    "QS Score",
                "rank_numeric":     "QS Ranking",
                "Subject":          "Field",
                "Languages":        "Languages",
                "Level":            "Available Levels",
                "Website":          "Website",
            }
            df_result = df_result.rename(columns=rename)
 
            if "QS Score" in df_result.columns:
                df_result["QS Score"] = df_result["QS Score"].round(1)
            if "QS Ranking" in df_result.columns:
                df_result["QS Ranking"] = df_result["QS Ranking"].astype(int)
            if "Website" in df_result.columns:
                df_result["Website"] = df_result["Website"].apply(
                    lambda x: f'<a href="{x}" target="_blank">🔗 Visit</a>' if pd.notna(x) else "—"
                )
 
            display_cols = [c for c in [
                "University", "Country", "QS Score", "QS Ranking",
                "Field", "Languages", "Available Levels", "Website"
            ] if c in df_result.columns]
 
            df_result = df_result[display_cols].reset_index(drop=True)
            df_result.index += 1
 
            st.write(df_result.to_html(escape=False, index=True), unsafe_allow_html=True)
            st.success(f"✅ {len(unis)} universities recommended for your profile!")
 
            # PDF Export
            st.divider()
            pdf_bytes = generate_pdf(
                grade=grade,
                scale=scale,
                level=lvl,
                subject=subject,
                languages=languages,
                continents=continents,
                recommendations=unis,
            )
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_bytes,
                file_name=f"university_recommendations_{lvl.lower()}.pdf",
                mime="application/pdf",
                type="primary",
            )
 