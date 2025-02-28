# Chat GPT Solutions

The files in this folder represent a quick solution built with ChatGPT.

## The Prototype

The prototype works by:
1. **Loading a Catalogue of Agent Components**  
   - The catalogue consists of pre-defined **chunks** of agent instructions, code snippets, domain knowledge, and policies.  
   - Each chunk is labeled with a **title** and associated with an **original agent prompt** from which it was derived.

2. **User Query Processing**  
   - A user submits a request (e.g., "I need an agent that processes scRNA-seq data and performs clustering").  
   - The system uses **GPT-4** to select the most relevant chunks from the catalogue based on the query.

3. **Prompt Reconstruction**  
   - The selected chunks are **concatenated** in order to form a new, structured agent prompt.  
   - This reconstructed prompt is then passed to **GPT-4** for final execution, generating **Python code, analysis steps, or scientific reasoning** based on the assembled knowledge.

---

## The Benchmarking

The benchmarking works by:
1. **Creating a Gold Standard**  
   - A set of **original agent prompts** (fully-formed, correct instructions) is stored as reference data.  
   - Each original prompt is **chunked** into smaller sections and added to the catalogue.

2. **Generating Test Queries**  
   - Each original prompt is paired with a **user-like request** that should logically require the same content.  
   - These requests are designed to simulate a real-world scenario where a user asks for an agent.

3. **Running GPT-4 Selection**  
   - The model is shown the catalogue of chunks and asked to select the **minimal** set of pieces necessary to reconstruct a valid agent prompt for the given query.  
   - The system **records** which pieces were chosen.

4. **Reconstructing and Comparing**  
   - The selected chunks are concatenated into a reconstructed prompt.  
   - This **reconstructed** prompt is compared to the original using **BLEU scoring (text similarity)** and **semantic embedding similarity** (e.g., Sentence-BERT).  
   - Higher scores indicate that the LLM correctly **identified** and **reassembled** the intended agent instructions.

5. **Evaluating Performance**  
   - The benchmark computes metrics such as:
     - **Precision & Recall**: How many correct chunks were retrieved, and how many were missing?  
     - **BLEU Score**: How much text overlap exists between the original and the reconstructed prompts?  
     - **Cosine Similarity**: How close is the meaning of the reconstructed prompt to the original?  

6. **Interpreting Results**  
   - If the LLM **misses important pieces** or **includes incorrect ones**, the evaluation will reveal weaknesses in chunk selection.  
   - If similarity scores are **low**, we can refine how the catalogue is structured or how the selection query is framed.  

---

## Goals

This system provides a **quantitative method** for evaluating how well an LLM can reconstruct structured knowledge from fragmented sources. The insights gained can improve how **bioinformatics agents are designed, assembled, and deployed** for research applications.