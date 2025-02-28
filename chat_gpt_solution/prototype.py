import openai
import json

# 1. Set your OpenAI API key (replace with your real key):
openai.api_key = "YOUR_API_KEY"

# 2. Load the entire catalogue
with open("catalogue.json", "r") as f:
    catalogue_data = json.load(f)

# The catalogue structure: 
#   {
#     "catalogue": [
#       {"title": "title1", "text": "..."}, 
#       {"title": "title2", "text": "..."},
#       ...
#     ]
#   }

catalogue_items = catalogue_data["catalogue"]

# 3. Let's define a user prompt or request:
user_request = (
    "I have Slide-seq data from a mouse brain, and I'd like to deconvolute the spots "
    "using single-cell RNA-seq reference data. Please guide me on how to load, QC, "
    "and run a spatial mapping algorithm (Tangram)."
)

# 4. Step One: Ask GPT-4 which pieces from the catalogue are relevant.
#    We'll feed the entire list of titles (or full items if needed) and the user request.
#    Then GPT-4 can return a list of piece indices or titles it wants.

# Prepare a message describing the task:
selection_instructions = f"""
You are an assistant that helps choose the most relevant knowledge pieces from a bioinformatics catalogue.
The user request is: "{user_request}"

Below is the entire catalogue, each item with a title and text.
Return a JSON list of the item 'titles' you recommend to solve the user's request.
If you think multiple items are relevant, list them all. If not, limit to the minimal necessary set.

CATALOGUE:
"""

# We can include each piece's index and title for GPT's reference:
for i, item in enumerate(catalogue_items):
    selection_instructions += f"\n{i}. TITLE: {item['title']}"

# Now we do a ChatCompletion call where we ask GPT to choose
selection_response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": "You are an intelligent system that can select relevant knowledge from a provided catalogue."
        },
        {
            "role": "user",
            "content": selection_instructions
        }
    ],
    temperature=0.0  # Encourage deterministic output for selection
)

selection_text = selection_response["choices"][0]["message"]["content"]
print("GPT-4's selection response:\n", selection_text)

# Parse the GPT output:
# Example expected format:
#   ["Global Agent Policy (Core Guidelines)", 
#    "Spatial Transcriptomics Preprocessing (General Guidance)", 
#    ... ]
# We'll assume GPT returns valid JSON or a text that we can parse as JSON
import ast
try:
    chosen_titles = ast.literal_eval(selection_text)
    if not isinstance(chosen_titles, list):
        chosen_titles = []
except:
    # fallback if GPT didn't produce a strict JSON list, do some manual parsing
    chosen_titles = []

if not chosen_titles:
    # If GPT didn't provide anything, fallback to a default or handle the error
    print("No valid titles found. Defaulting to an empty list.")
    chosen_titles = []

# 5. Compose the final system prompt using the text of the chosen pieces
chosen_texts = []
for item in catalogue_items:
    if item["title"] in chosen_titles:
        chosen_texts.append(f"## {item['title']}\n\n{item['text']}\n")

final_system_prompt = "\n".join(chosen_texts)

# 6. Step Two: Re-invoke GPT-4 with the final system prompt + user request.
#    Now GPT-4 has only the relevant pieces for context, along with the user's question.
agent_response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": final_system_prompt},  # the chosen items
        {"role": "user", "content": user_request}
    ],
    temperature=0.3,
    max_tokens=1200
)

assistant_answer = agent_response["choices"][0]["message"]["content"]
print("\n===== FINAL AGENT ANSWER =====\n")
print(assistant_answer)