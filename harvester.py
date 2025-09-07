# harvester.py

import requests
from config import NCBI_API_KEY
import time
from xml.etree import ElementTree

def fetch_patient_descriptions(output_file, max_articles=1000):
    """
    Searches PubMed and saves abstracts to a text file with detailed logging and retry logic.
    """
    if not NCBI_API_KEY or NCBI_API_KEY == "your_ncbi_api_key_here":
        print("Error: NCBI API Key is not set in config.py.")
        return

    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    search_term = "(adverse drug reaction[Title/Abstract]) AND (case report[Title/Abstract])"
    print(f"Searching PubMed with query: \"{search_term}\"")

    esearch_params = {
        "db": "pubmed", "term": search_term, "retmax": max_articles,
        "usehistory": "y", "api_key": NCBI_API_KEY, "retmode": "json"
    }
    
    try:
        esearch_req = requests.get(base_url + "esearch.fcgi", params=esearch_params)
        esearch_req.raise_for_status()
        esearch_data = esearch_req.json()
        webenv = esearch_data["esearchresult"]["webenv"]
        query_key = esearch_data["esearchresult"]["querykey"]
        count = int(esearch_data["esearchresult"]["count"])
        print(f"Found {count} articles. Will fetch details for up to {max_articles}.")
    except Exception as e:
        print(f"Error during ESearch: {e}")
        return

    batch_size = 200
    all_abstracts = []
    for start in range(0, min(count, max_articles), batch_size):
        print(f"\n[+] Preparing to fetch batch starting at article {start}...")
        efetch_params = {
            "db": "pubmed", "retmode": "xml", "retstart": start,
            "retmax": batch_size, "webenv": webenv,
            "query_key": query_key, "api_key": NCBI_API_KEY
        }
        
        for attempt in range(3):
            try:
                print(f"  [+] Attempt {attempt + 1}/3: Sending EFetch request to NCBI...")
                efetch_req = requests.get(base_url + "efetch.fcgi", params=efetch_params, timeout=60)
                efetch_req.raise_for_status()
                print("  [+] EFetch response received successfully.")

                root = ElementTree.fromstring(efetch_req.content)
                articles_in_batch = root.findall(".//PubmedArticle")

                for article in articles_in_batch:
                    abstract_node = article.find(".//AbstractText")
                    if abstract_node is not None and abstract_node.text:
                        all_abstracts.append(abstract_node.text.replace("\n", " ").strip())
                
                print("  [+] Finished processing batch.")
                break 
            
            except Exception as e:
                print(f"  [!] Attempt {attempt + 1} failed with error: {e}")
                if attempt < 2:
                    print("      Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    print("  [!] All retry attempts failed for this batch. Moving on.")
        
        time.sleep(1)
            
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for abstract in all_abstracts:
                f.write(abstract + "\n")
        print(f"\nSuccess! Saved {len(all_abstracts)} abstracts to '{output_file}'.")
    except Exception as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    output_filename = "patients.txt"
    # The only change is on the next line
    fetch_patient_descriptions(output_filename, max_articles=1000)
