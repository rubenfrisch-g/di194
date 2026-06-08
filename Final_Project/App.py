import streamlit as st
import pandas as pd
from KNN_model import recommend, CONTINENT_COUNTRIES, ALL_LANGUAGES, get_student_level
from pdf_export import generate_pdf
from genai_explainer import generate_explanation
 
st.set_page_config(page_title="University Recommender", page_icon="🎓", layout="wide")
 
st.title("🎓 University Recommender")
st.caption("Find the universities that match your profile using Machine Learning")
st.divider()
 
COLORS = {
    "World Elite": "🔴",
    "Elite":       "🟠",
    "High Mid":    "🔵",
    "Mid":         "🟡",
    "Accessible":  "🟢",
    "Open":        "⚪",
}
 
with st.sidebar:
    st.header("👤 Your Profile")
 
    st.subheader("📊 Academic Results")
    scale = st.selectbox("Grading system", [20, 100, 4], index=0)
    grade = st.slider(f"Your grade (out of {scale})", 0.0, float(scale), float(scale) * 0.7, 0.5)
    level_student = get_student_level(grade, scale)
    st.caption(f"**{grade}/{scale}** ({grade/scale*100:.0f}%) → {COLORS[level_student]} **{level_student}**")
 
    st.divider()
 
    st.subheader("🎓 Desired Study Level")
    level = st.selectbox("Level", ["All levels", "Bachelor", "Master", "PhD"])
 
    st.divider()
 
    st.subheader("📚 Field of Study")
    subjects = [
        "All fields", "Engineering & Technology", "Computer Science",
        "Natural Sciences", "Life Sciences & Medicine", "Business & Management",
        "Social Sciences & Management", "Arts & Humanities", "Law",
    ]
    subject = st.selectbox("Desired field", subjects)
 
    st.divider()
 
    st.subheader("🗣️ Languages Spoken")
    languages = st.multiselect("Languages you speak", options=ALL_LANGUAGES, default=["English"])
 
    st.divider()
 
    st.subheader("🌍 Location")
    continent_options = ["All continents"] + list(CONTINENT_COUNTRIES.keys())
    continents = st.multiselect("Desired continents", options=continent_options, default=["All continents"])
    if not continents:
        continents = ["All continents"]
 
    st.divider()
 
    n_reco = st.slider("Number of recommendations", 1, 10, 5)
    run = st.button("🔍 Find my universities", type="primary", use_container_width=True)
 
 
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
 
    - **K-Means** groups universities into 6 levels based on your grade :
        - 🔴 **World Elite** → 93% and above (MIT, Harvard, Oxford...)
        - 🟠 **Elite** → 83% to 93% (ETH Zurich, Imperial, UCL...)
        - 🔵 **High Mid** → 76% to 83% (McGill, Edinburgh, Melbourne...)
        - 🟡 **Mid** → 63% to 76% (Sheffield, Adelaide, Utrecht...)
        - 🟢 **Accessible** → 50% to 63%
        - ⚪ **Open** → below 50%
 
    - **KNN (K-Nearest Neighbors)** finds the universities most suited to your profile within your level.
 
    Recommendations take into account :
    - Your academic results
    - Your field of study
    - Your languages
    - Your desired study level (Bachelor / Master / PhD)
    - Your desired continent(s)
    """)
 
else:
    with st.spinner("Analysing your profile..."):
        results = recommend(
            grade=grade,
            scale=scale,
            subject=subject,
            continents=continents,
            languages=languages if languages else None,
            level=level,
            n_recommendations=n_reco,
        )
 
    if "error" in results:
        st.error(f"❌ {results['error']}")
        st.info("Try broadening your search: fewer filters or more continents.")
    else:
        st.subheader("📋 Your Profile")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Grade", f"{grade}/{scale} ({grade/scale*100:.0f}%)")
        c2.metric("Level", f"{COLORS[level_student]} {level_student}")
        c3.metric("Field", subject.split("&")[0].strip())
        c4.metric("Languages", ", ".join(languages) if languages else "All")
 
        st.divider()
 
        unis = results["recommendations"]
        level_config = {
            "World Elite": {"emoji": "🔴", "desc": "World's most prestigious — extremely selective (top 1%)"},
            "Elite":       {"emoji": "🟠", "desc": "World-class universities — highly selective"},
            "High Mid":    {"emoji": "🔵", "desc": "Excellent universities — selective"},
            "Mid":         {"emoji": "🟡", "desc": "Very good universities — moderately selective"},
            "Accessible":  {"emoji": "🟢", "desc": "Good universities — accessible with solid grades"},
            "Open":        {"emoji": "⚪", "desc": "Universities with open or flexible admission"},
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
 
            st.divider()
            st.subheader("🤖 AI Counselor")
            with st.spinner("Generating personalized advice..."):
                try:
                    explanation = generate_explanation(
                        grade=grade, scale=scale, level=lvl, subject=subject,
                        languages=languages, continents=continents, recommendations=unis,
                    )
                    st.info(explanation)
                except Exception as e:
                    st.warning(f"AI explanation unavailable: {e}")
 
            st.divider()
            pdf_bytes = generate_pdf(
                grade=grade, scale=scale, level=lvl, subject=subject,
                languages=languages, continents=continents, recommendations=unis,
            )
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_bytes,
                file_name=f"university_recommendations_{lvl.lower().replace(' ', '_')}.pdf",
                mime="application/pdf",
                type="primary",
            )