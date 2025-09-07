# article_matcher.py

import json
import csv
from pymed import PubMed
from config import MY_EMAIL

def batch_match_articles(input_file, output_file):
    """
    Reads structured PREP data from a JSONL file, matches each entry to a
    PubMed article, and saves the final, combined results to a CSV file.
    """
    print(f"\n--- Final Stage: Starting Article Matching from '{input_file}' ---")
    all_final_results = []
    
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
        print(f"Found {len(lines)} records to process.")
    except FileNotFoundError:
        print(f"\nError: The intermediate file '{input_file}' was not found.")
        print("Please run 'python prep_extractor.py' first to create it.")
        return

    # Initialize the PubMed client once
    pubmed = PubMed(tool="MyHealthcareAgent", email=MY_EMAIL)
    
    for i, line in enumerate(lines):
        prep_data = json.loads(line)
        event = prep_data.get("EVENT")
        product = prep_data.get("PRODUCT")
        
        print(f"\nProcessing record #{i + 1}...")
        print(f"  -> Searching PubMed for EVENT: '{event}' and PRODUCT: '{product}'...")

        # If essential data is missing, we can't search
        if not event or not product or event == "Not found" or product == "Not found":
            prep_data["Matched Article Title"] = "Search not possible (missing data)."
            prep_data["Matched PubMed ID"] = "N/A"
            all_final_results.append(prep_data)
            print("     -> Skipping search due to missing data.")
            continue
            
        try:
            # Perform the targeted search on PubMed
            query = f'("{product}"[Title/Abstract]) AND ("{event}"[Title/Abstract])'
            results = pubmed.query(query, max_results=1)
            
            # Get the top result
            top_article = next(results)
            prep_data["Matched Article Title"] = top_article.title
            prep_data["Matched PubMed ID"] = top_article.pubmed_id
            print("     -> Success: Found a matching article.")

        except StopIteration:
            # This happens if the search returns no results
            prep_data["Matched Article Title"] = "No matching article found."
            prep_data["Matched PubMed ID"] = "N/A"
            print("     -> No articles found for this specific query.")
            
        all_final_results.append(prep_data)
        
    # --- Writing the Final CSV Report ---
    if not all_final_results:
        print("\nNo data was processed. The final CSV file will not be created.")
        return
        
    # Define the column headers for the spreadsheet
    headers = [
        "Original Description", "PATIENT", "REPORTER", "EVENT", 
        "PRODUCT", "Matched Article Title", "Matched PubMed ID"
    ]
    
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            # Use DictWriter to easily write rows from our list of dictionaries
            writer = csv.DictWriter(outfile, fieldnames=headers, extrasaction='ignore')
            
            # Write the header row
            writer.writeheader()
            
            # Write all the data rows
            writer.writerows(all_final_results)
            
        print(f"\n--- PROJECT COMPLETE! ---")
        print(f"Final report has been successfully saved to '{output_file}'.")
        print("You can now open this file in Excel or any spreadsheet software.")

    except Exception as e:
        print(f"\nAn error occurred while writing the final CSV file: {e}")


if __name__ == "__main__":
    # The input is the intermediate file created by the prep_extractor.py script
    input_filename = "prep_results.jsonl"
    
    # The final output is our user-friendly CSV report
    output_filename = "final_patient_reports.csv"
    
    # Run the final stage of the pipeline
    batch_match_articles(input_filename, output_filename)
