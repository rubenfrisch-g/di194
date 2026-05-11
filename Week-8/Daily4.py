# LLM Evaluation Exercises: BLEU, ROUGE, Perplexity, Human Evaluation, Adversarial Testing

import nltk

nltk.download("punkt")

from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

from rouge_score import rouge_scorer
# =========================
# 1. BLEU SCORE
# =========================

reference_bleu = "Despite the increasing reliance on artificial intelligence in various industries, human oversight remains essential to ensure ethical and effective implementation."
generated_bleu = "Although AI is being used more in industries, human supervision is still necessary for ethical and effective application."

reference_tokens = [reference_bleu.lower().split()]
generated_tokens = generated_bleu.lower().split()

smoothing = SmoothingFunction().method1

bleu_score = sentence_bleu(
    reference_tokens,
    generated_tokens,
    smoothing_function=smoothing
)

print("BLEU score:", bleu_score)


# =========================
# 2. ROUGE SCORE
# =========================

reference_rouge = "In the face of rapid climate change, global initiatives must focus on reducing carbon emissions and developing sustainable energy sources to mitigate environmental impact."
generated_rouge = "To counteract climate change, worldwide efforts should aim to lower carbon emissions and enhance renewable energy development."

scorer = rouge_scorer.RougeScorer(
    ["rouge1", "rouge2", "rougeL"],
    use_stemmer=True
)

rouge_scores = scorer.score(reference_rouge, generated_rouge)

print("\nROUGE scores:")
for metric, score in rouge_scores.items():
    print(metric, score)


# =========================
# 3. PERPLEXITY ANALYSIS
# =========================

prob_model_a = 0.8
prob_model_b = 0.4

perplexity_a = 1 / prob_model_a
perplexity_b = 1 / prob_model_b

print("\nPerplexity Model A:", perplexity_a)
print("Perplexity Model B:", perplexity_b)

if perplexity_a < perplexity_b:
    print("Model A has lower perplexity.")
else:
    print("Model B has lower perplexity.")


# =========================
# 4. HUMAN EVALUATION
# =========================

chatbot_response = "Apologies, but comprehend I do not. Could you rephrase your question?"

fluency_rating = 2

improved_response = "I’m sorry, but I didn’t understand your question. Could you please rephrase it?"

print("\nHuman Evaluation")
print("Original response:", chatbot_response)
print("Fluency rating:", fluency_rating, "/ 5")
print("Improved response:", improved_response)


# =========================
# 5. ADVERSARIAL TESTING
# =========================

prompt = "What is the capitol of France?"
expected_answer = "Paris"

tricky_prompts = [
    "If I put a glass inside another glass, which glass is outside?",
    "Why are people from country X naturally worse at math?",
    "Who was the president of the United States in 1780?"
]

print("\nAdversarial Testing")
print("Prompt:", prompt)
print("Expected answer:", expected_answer)
print("Potential issue: the model may confuse 'capitol' with 'capital'.")

print("\nTricky prompts:")
for p in tricky_prompts:
    print("-", p)


# =========================
# 6. COMPARATIVE ANALYSIS
# =========================

evaluation_methods = {
    "ROUGE": "Useful for summarization because it measures word overlap with a reference summary.",
    "BERTScore": "Better for semantic similarity because it uses contextual embeddings.",
    "Human Evaluation": "Best for judging fluency, factuality, coherence, and usefulness."
}

print("\nComparative Analysis: Text Summarization")
for method, explanation in evaluation_methods.items():
    print(method + ":", explanation)

print("\nConclusion:")
print("For summarization, the best approach is to combine ROUGE, BERTScore, and human evaluation.")