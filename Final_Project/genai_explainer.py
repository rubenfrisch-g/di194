import os
from groq import Groq
 
 
def generate_explanation(
    grade: float,
    scale: int,
    level: str,
    subject: str,
    languages: list,
    continents: list,
    recommendations: list,
) -> str:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
 
    uni_list = ""
    for i, uni in enumerate(recommendations[:5], start=1):
        name  = uni.get('Institution Name', '')
        loc   = uni.get('Location', '')
        score = uni.get('score_numeric', 0)
        rank  = int(uni.get('rank_numeric', 0))
        uni_list += f"{i}. {name} ({loc}) - QS Score: {score:.1f}, Rank: #{rank}\n"
 
    teaching_languages = set()
    for uni in recommendations[:5]:
        lang = uni.get("Languages", "")
        lang = str(lang) if lang and str(lang) != "nan" else ""
        for l in lang.split(","):
            l = l.strip().lower()
            if l:
                teaching_languages.add(l)
 
    cert_lines = []
    if "english" in teaching_languages:
        cert_lines.append("TOEFL (90+) or IELTS (6.5+) for English programs")
    if "german" in teaching_languages:
        cert_lines.append("TestDaF or DSH for German programs")
    if "french" in teaching_languages:
        cert_lines.append("DELF/DALF B2+ for French programs")
    if "dutch" in teaching_languages:
        cert_lines.append("NT2 for Dutch programs")
    if "spanish" in teaching_languages:
        cert_lines.append("DELE B2+ for Spanish programs")
    if "korean" in teaching_languages:
        cert_lines.append("TOPIK Level 3+ for Korean programs")
    if "japanese" in teaching_languages:
        cert_lines.append("JLPT N2+ for Japanese programs")
    if "chinese" in teaching_languages:
        cert_lines.append("HSK Level 4+ for Chinese programs")
 
    cert_advice    = ", ".join(cert_lines) if cert_lines else "No specific certifications needed"
    langs_str      = ", ".join(languages) if languages else "English"
    continents_str = ", ".join(continents) if "All continents" not in continents else "Worldwide"
 
    prompt = (
        "You are a university admissions counselor.\n\n"
        f"Student: Grade {grade}/{scale} ({grade/scale*100:.0f}%), "
        f"Level: {level}, Field: {subject}, "
        f"Languages: {langs_str}, Region: {continents_str}\n\n"
        f"Universities:\n{uni_list}\n"
        f"Certifications needed: {cert_advice}\n\n"
        "Write 3 sentences: why these universities fit, "
        "which certifications are needed, and one encouraging tip."
    )
 
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful university admissions counselor."},
            {"role": "user",   "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7,
    )
 
    return response.choices[0].message.content