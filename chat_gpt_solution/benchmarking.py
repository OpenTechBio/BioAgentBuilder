import json
import openai
import nltk
import re
import random
from nltk.translate.bleu_score import sentence_bleu
from sentence_transformers import SentenceTransformer, util

nltk.download('punkt')  # needed for BLEU tokenization
openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your actual API key


# 1. Define or load a small set of original agent prompts.
#    In real usage, these might be longer or more numerous.
original_prompts = {
    "PromptA": """You are a specialized coder agent focused on scRNA-seq analysis.
Follow these rules:
1. Only output Python code.
2. Remain polite and professional.
3. Use scanpy for single-cell analysis.
""",
    "PromptB": """You are an agent specialized in spatial transcriptomics (Slide-seq).
Rules:
1. Load coordinate data from text files.
2. Use tangram for single-cell mapping.
3. Summarize the results with caution and do not reveal private data.
"""
}

# 2. A function to chunk each prompt into smaller pieces. 
#    You can customize this to your liking (e.g., splitting by paragraphs, lines, or rules).
def chunk_prompt(prompt_text, max_chunk_length=100):
    """
    Splits a prompt into smaller textual chunks of up to max_chunk_length characters.
    This is a simple demonstration; real chunking can be more sophisticated.
    """
    # Split by sentences or lines for demonstration
    # We'll do a naive approach: split on periods, keep them short
    sentences = re.split(r'(?<=[.])\s', prompt_text.strip())
    chunks = []
    temp_chunk = []

    for sentence in sentences:
        if len(" ".join(temp_chunk) + sentence) < max_chunk_length:
            temp_chunk.append(sentence)
        else:
            chunks.append(" ".join(temp_chunk))
            temp_chunk = [sentence]

    # Add remaining chunk if not empty
    if temp_chunk:
        chunks.append(" ".join(temp_chunk))

    # Clean up whitespace
    chunks = [c.strip() for c in chunks if c.strip()]

    return chunks


# 3. Chunk each original prompt and build a master catalogue.
catalogue = []
for prompt_id, (prompt_name, prompt_text) in enumerate(original_prompts.items()):
    sub_chunks = chunk_prompt(prompt_text, max_chunk_length=120)
    for i, chunk_text in enumerate(sub_chunks):
        catalogue_item = {
            "title": f"{prompt_name}_chunk{i}",
            "prompt_name": prompt_name,
            "chunk_id": i,
            "text": chunk_text
        }
        catalogue.append(catalogue_item)

# Let's see what we have in the catalogue
print("=== Catalogue Items ===")
for item in catalogue:
    print(item)

# 4. Create test queries that mimic user requests for each prompt.
#    For demonstration, we'll keep them quite simple.
test_queries = {
    "PromptA": "I need an agent for scRNA-seq. It should only output Python code, be polite, and use scanpy.",
    "PromptB": "I want to load Slide-seq coordinates, use tangram for mapping, and keep data private."
}

# 5. A helper function to get chunk selection from GPT-4
def llm_select_catalogue_items(catalogue_list, user_query):
    """
    We provide GPT-4 with a list of chunk titles and a user query.
    GPT-4 is asked to return a JSON list of titles that it deems relevant.
    """
    # Construct a message describing the catalogue
    catalogue_summary = "Here are the catalogue items:\n"
    for idx, cat_item in enumerate(catalogue_list):
        catalogue_summary += f"{idx}. TITLE: {cat_item['title']}\n"

    # We'll ask GPT-4 to pick relevant chunk titles
    system_prompt = """You are a system that selects the minimal set of catalogue items that best answer the user query."""
    user_prompt = f"""
User request: {user_query}

{catalogue_summary}

Return a JSON list (e.g. ["PromptA_chunk0", "PromptA_chunk1", ...]) of the chunk titles you select. 
Only return the list, nothing else.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.0,
        max_tokens=500
    )

    content = response["choices"][0]["message"]["content"]
    # Attempt to parse the GPT output as JSON
    print("=== GPT-4 chunk selection response ===")
    print(content)
    try:
        selected_titles = json.loads(content)
        if not isinstance(selected_titles, list):
            selected_titles = []
    except:
        selected_titles = []

    return selected_titles


# 6. A function to compute two metrics: BLEU score and embedding-based similarity
#    using a sentence transformer. We can treat the entire text as one "sentence".
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

def measure_metrics(original_text, reconstructed_text):
    """
    Return BLEU and embedding similarity for the two strings.
    """

    # BLEU typically needs reference and candidate in tokenized form:
    ref_tokens = nltk.word_tokenize(original_text)
    cand_tokens = nltk.word_tokenize(reconstructed_text)

    bleu = sentence_bleu([ref_tokens], cand_tokens)

    # Embedding similarity
    emb1 = embed_model.encode(original_text, convert_to_tensor=True)
    emb2 = embed_model.encode(reconstructed_text, convert_to_tensor=True)
    cos_sim = float(util.pytorch_cos_sim(emb1, emb2)[0][0])

    return {
        "BLEU": bleu,
        "CosineSimilarity": cos_sim
    }


# 7. Run the entire selection, reconstruction, and evaluation pipeline.
results = {}
for prompt_name, query_text in test_queries.items():
    # original text
    original_text = original_prompts[prompt_name]

    # LLM selects chunk titles
    selected_titles = llm_select_catalogue_items(catalogue, query_text)

    # Reconstruct
    reconstructed_text = ""
    for title in selected_titles:
        # find matching item in catalogue
        item = next((i for i in catalogue if i["title"] == title), None)
        if item:
            reconstructed_text += item["text"] + "\n"

    # Measure
    metrics = measure_metrics(original_text, reconstructed_text)
    results[prompt_name] = {
        "selected_titles": selected_titles,
        "reconstructed_text": reconstructed_text,
        "metrics": metrics
    }


# 8. Print the final results
print("\n=== FINAL RESULTS ===")
for prompt_name, data in results.items():
    print(f"Prompt: {prompt_name}")
    print(f"Selected Titles: {data['selected_titles']}")
    print(f"Reconstructed Text:\n{data['reconstructed_text']}")
    print(f"Metrics: {data['metrics']}")
    print("-" * 40)