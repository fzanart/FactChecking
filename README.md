---
title: Fact checking pipeline
emoji: 🌎
colorFrom: green
colorTo: gray
sdk: gradio
sdk_version: 4.21.0
app_file: app.py
pinned: false
license: mit
python_version: 3.11
startup_duration_timeout: 2h
---




# FactChecking
FactChecking provides a robust pipeline for fact-checking climate change-related claims.   

Features

1. Document Retrieval:  
  Given a controversial claim, the system searches the internet for documents containing relevant information.
  It identifies and retrieves documents that may help in the validation of the claim.

2. Evidence Extraction:  
  Extracts specific text snippets or sentences from the retrieved documents.
  Focuses on extracting information directly related to the claim to provide relevant context.

3. Stance Detection:  
  Analyzes the extracted evidence to determine its stance regarding the claim.
  Classifies the stance as: no stance, support, or refute.

4. Claim Validation:  
  Assesses the overall validity of the claim based on the extracted evidence and stance detection results.
  Provides a clear conclusion on whether the claim is supported or refuted, along with the relevant context.
