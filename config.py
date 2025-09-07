# config.py

# Your email address for making polite requests to the PubMed API.
MY_EMAIL = "madhunayani12@gmail.com"

# Your secret API key from OpenRouter.
OPENROUTER_API_KEY = "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"

NCBI_API_KEY = "ef4f204e594e4fa7ea4b132e805aa8e4d608"

PATIENT_COUNT = 1000

RAW_DATA_FILE = "patients_abstracts.txt"

INTERMEDIATE_FILE = "prep_extractions.jsonl"

FINAL_REPORT_FILE = "final_patient_reports.csv"

# --- Model and API Settings ---
# The name of the local model to use in Ollama.
LOCAL_LLM_MODEL = 'llama3.2'



# A small delay (in seconds) to add between each call to the local LLM 
# to prevent overwhelming the model and ensure stability during long runs.
LLM_REQUEST_DELAY = 0.5 # Half a second