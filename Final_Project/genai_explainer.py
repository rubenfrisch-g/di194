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
 
    # Build university list
    uni_list = ""
    for i, uni in enumerate(recommendations[:5], start=1):
        uni_list += f"{i}. {uni.get('Institution Name', '')} ({uni.get('Location', '')}) — QS Score: {uni.get('score_numeric', 0):.1f}, Rank: #{int(uni.get('rank_numeric', 0))}\n"
 
    # Detect teaching languages safely
    teaching_languages = set()
    for uni in recommendations[:5]:
        lang = uni.get("Languages", "")
        lang = str(lang) if lang and str(lang) != "nan" else ""
        for l in lang.split(","):
            l = l.strip().lower()
            if l:
                teaching_languages.add(l)
 
    # Build certification advice
    cert_lines = []
    if "english" in teaching_languages:
        cert_lines.append("TOEFL (90+) or IELTS (6.5+) for English-taught programs")
    if "german" in teaching_languages:
        cert_lines.append("TestDaF or DSH for German-taught programs")
    if "french" in teaching_languages:
        cert_lines.append("DELF/DALF (B2+) for French-taught programs")
    if "dutch" in teaching_languages:
        cert_lines.append("NT2 exam for Dutch-taught programs")
    if "spanish" in teaching_languages:
        cert_lines.append("DELE (B2+) for Spanish-taught programs")
    if "korean" in teaching_languages:
        cert_lines.append("TOPIK (Level 3+) for Korean-taught programs")
    if "japanese" in teaching_languages:
        cert_lines.append("JLPT (N2+) for Japanese-taught programs")
    if "chinese" in teaching_languages:
        cert_lines.append("HSK (Level 4+) for Chinese-taught programs")
 
    cert_advice = "\n".join(f"- {c}" for c in cert_lines) if cert_lines else "No specific certifications identified."
 
    prompt = f"""You are a university admissions counselor helping a student find the right university.
 
Student Profile:
- Grade: {grade}/{scale} ({grade/scale*100:.0f}%)
- Academic Level: {level}
- Field of Study: {subject}
- Languages spoken: {', '.join(languages) if languages else 'English'}
- Preferred continents: {', '.join(continents) if 'All continents' not in continents else 'Worldwide'}
 
Recommended Universities:
{uni_list}
 
Language certifications that may be required:
{cert_advice}
 
Write a very short, friendly and personalized paragraph (3-4 sentences maximum) that:
1. Explains why these universities match the student's profile
2. Highlights what makes them a good fit for their field of study
3. Mentions which language certifications they should prepare (TOEFL, IELTS, TestDaF, etc.)
4. Ends with one encouraging piece of advice for the application process
 
Keep it concise, positive and motivating. Address the student directly."""
 
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful university admissions counselor."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7,
    )
 
    return response.choices[0].message.content