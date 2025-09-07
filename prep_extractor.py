# prep_extractor.py

import json
import ollama

def extract_prep_data(text_description):
    """Uses a local Llama 3.2 model via Ollama to extract PREP data."""
    prompt = f"""
    From the following medical case description, extract these four details:
    1. PATIENT: The age and gender.
    2. REPORTER: The name or title of the person reporting.
    3. EVENT: The primary medical event or symptom.
    4. PRODUCT: The drug or medical product involved.

    If a detail is not found, write "Not found".
    Provide the output as a simple list, exactly in this format:
    PATIENT: [result]
    REPORTER: [result]
    EVENT: [result]
    PRODUCT: [result]

    Here is the text to analyze:
    "{text_description}"
    """
    try:
        response = ollama.chat(
            model='llama3.2',
            messages=[{'role': 'user', 'content': prompt}]
        )
        raw_output = response['message']['content']
        prep_data = {}
        for line in raw_output.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                prep_data[key.strip()] = value.strip()
        return prep_data
    except Exception as e:
        print(f"   Error communicating with local Ollama server: {e}")
        return None

def batch_extract(input_file, output_file, max_patients=1000):
    """Reads patient descriptions and saves their PREP extractions to a JSONL file."""
    print(f"--- Stage 1: Starting PREP Extraction from '{input_file}' using local Llama 3.2 ---")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found. Run harvester.py first.")
        return

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for i, description in enumerate(lines):
            if i >= max_patients:
                break
            
            description = description.strip()
            if not description: continue

            print(f"\nProcessing abstract #{i + 1}...")
            prep_result = extract_prep_data(description)

            if prep_result:
                prep_result["Original Description"] = description
                outfile.write(json.dumps(prep_result) + "\n")
                print("   -> Success. Saved to intermediate file.")
            else:
                print("   -> Failed to extract PREP data for this abstract.")
                
    print(f"\n--- Stage 1 Complete. All PREP extractions saved to '{output_file}' ---")

if __name__ == "__main__":
    input_filename = "patients.txt"
    output_filename = "prep_results.jsonl"
    # The only change is on the next line
    batch_extract(input_filename, output_filename, max_patients=1000)
