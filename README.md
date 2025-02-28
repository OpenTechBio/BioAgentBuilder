# Composer Agents for Bioinformatics

## Overview

This repository aims to **build effective "composer" agents** for bioinformatics, particularly in the domains of **single-cell** and **spatial single-cell** analysis within **neurobiology** and **cancer** research. 

The concept of a "composer" agent is to **assemble pieces** (code snippets, domain knowledge, policies) from a **catalogue** to generate an **integrated bioinformatics agent** capable of:

- **Loading and preprocessing data** (e.g., scRNA-seq, spatial transcriptomics)  
- **Performing standard QC and filtering**  
- **Running downstream analyses** (clustering, dimensional reduction, cell type annotation)  
- **Executing specialized tasks** (like spatial deconvolution, cell-cell interaction analysis, RNA velocity, batch correction, etc.)  

By customizing different catalogue entries for specific tasks, species, or data types, the composer can produce a final agent with all the necessary instructions and domain knowledge to tackle a specific user request or workflow.

## The Problem

Standardizing bioinformatics workflows for single-cell and spatial single-cell data analysis can be **time-consuming** and **error-prone**, especially when integrating multiple datasets, applying new tools, or dealing with specialized biological questions (neurobiology, oncology, etc.). 

**Typical challenges** include:
1. Selecting consistent code snippets or libraries for each analysis step.  
2. Incorporating relevant domain knowledge to interpret results (e.g., neuron-specific markers, cancer pathways).  
3. Enforcing agent policies (e.g., code-only responses, confidentiality, HPC usage).  
4. Handling **batch effects**, **cell type annotations**, or **multi-sample integration** with reproducible pipelines.  

**Solution**: Our composer agent dynamically **stitches** appropriate catalogue items (policies, domain knowledge, code templates, etc.) to generate a complete and specialized agent. This allows a flexible, modular approach to constructing analysis workflows.

## Inputs

1. **Agent Catalogue**:  
   - A JSON-based repository of code snippets, domain knowledge, policies, specialized functions for single-cell/spatial analysis, etc.  
   - Each catalogue item contains a `title` (hinting at its purpose) and `text` (the actual content injected into the final system prompt).

2. **User/Planner Instructions**:  
   - A higher-level plan or user instructions specifying which pieces to assemble, in what order, and any specialized parameters (e.g., choosing cancer vs. neuro domain, using scRNA-seq vs. scATAC-seq modules).

3. **Data Context** (optional):  
   - File paths or data references (e.g., .h5ad, .mtx, coordinates) to inform the composer how to load and process the dataset.

## Outputs

1. **Agent Prompt** (System Prompt for the Final Agent):  
   - A **consolidated prompt** that merges:
     - The relevant policies (professional conduct, code rules, HPC usage, etc.).
     - Domain-specific knowledge (markers, workflows, interpretive context for neuro or cancer).
     - Step-by-step function definitions or code snippets needed to complete the analysis.  
   - This final prompt is **automatically generated** by the composer, ensuring internal consistency and adherence to the provided plan.

2. **Executable Bioinformatics Agent**:  
   - Once the final prompt is deployed into a code-capable environment (e.g., a Jupyter kernel), it **executes** each step, loading data, performing QC, clustering, and more.  
   - The agent also returns **interpretations** of each step’s outputs (e.g., images, stats, differential expression results).

## How to Use

1. **Review the Catalogue**: Examine the available pieces. Decide which are needed for your specific single-cell or spatial data task (e.g., `Load Data`, `QC`, `Spatial Deconvolution`, etc.).  
2. **Assemble**: Combine the chosen pieces into a **final agent prompt**. This is done via the composer logic, which merges the text from each relevant catalogue entry.  
3. **Execute**: Provide the final system prompt to a code execution environment. The resulting agent is now specialized to run your single-cell or spatial workflow.  
4. **Iterate**: If the user needs additional analyses or domain expansions, insert new or updated pieces into the catalogue, then rebuild the agent.

## Example Scenario

- A user has **Slide-seq** data for **brain tissue**. They want to integrate scRNA-seq data to deconvolute spot-level cell types.  
- The composer selects:  
  - **Core Global Agent Policy**  
  - **Spatial Data Loading**  
  - **Neurobiology Domain Knowledge**  
  - **Tangram Deconvolution**  
  - **Agent Policy: Final Reporting**  
- The composer merges these items and injects the final text into a system prompt.  
- The agent proceeds with data loading, QC, clustering, and Tangram-based mapping, returning interpretative text for each step.

## Contributing

- **Add** new catalogue items (policies, domain knowledge, code templates) by following the existing JSON format.  
- **Edit** or refine existing items for more precise coverage (e.g., new QC methods, domain expansions for immunotherapy, neurodegenerative diseases, etc.).  
- **Test** your changes by assembling a new agent and running an end-to-end analysis pipeline.

## License

This project is distributed under the terms of [License Name Here]. Refer to `LICENSE` for details.