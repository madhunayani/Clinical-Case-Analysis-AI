
***

# Clinical Case Analysis AI<div align="center">



</div>

<p align="center">
  <!-- Core Technologies -->
  <img alt="Python" src="https://img.shields.io/badge/python-3.10+-blue.svg">
  <img alt="Ollama" src="https://img.shields.io/badge/Ollama-Local%20LLM-purple.svg">
  <img alt="Llama 3.2" src="https://img.shields.io/badge/Model-Llama%203.2-hotpink.svg">
  
  <!-- AI & ML Concepts -->
  <br>
  <img alt="Generative AI" src="https://img.shields.io/badge/Generative%20AI-Enabled-orange">
  <img alt="LLM" src="https://img.shields.io/badge/LLM-Powered-brightgreen">
  <img alt="NLP" src="https://img.shields.io/badge/NLP-Core-yellow">
  
  <!-- Project Info -->
  <br>
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green.svg">
  <img alt="Status" src="https://img.shields.io/badge/status-complete-brightgreen.svg">
</p>


An end-to-end AI pipeline that automates the extraction of structured **Patient, Reporter, Event, and Product (PREP)** data from unstructured clinical case reports. This project dynamically sources data from the NCBI PubMed database, leverages a locally hosted Llama 3.2 model for advanced semantic analysis, and matches each case with relevant scientific literature to provide evidence-backed insights.

## Key Features*   **Dynamic Data Harvesting**: Automatically downloads and preprocesses thousands of real-world medical abstracts from NCBI PubMed using its robust E-utilities API.
*   **State-of-the-Art NLP**: Utilizes a powerful, locally hosted Llama 3.2 model (served via Ollama) to accurately parse complex clinical narratives into structured data points.
*   **Robust and Scalable Architecture**: Built with a professional, multi-stage pipeline that separates data ingestion, AI processing, and final analysis. This modular design makes the system scalable, maintainable, and easy to debug.
*   **Resilient Error Handling**: Includes built-in retry logic for network requests to handle temporary API or connection issues gracefully, ensuring the long-running process completes successfully.
*   **Evidence-Based Matching**: Programmatically searches PubMed to link each extracted clinical case with relevant scientific literature, providing an evidence-based context for each report.
*   **User-Friendly Reporting**: Generates a clean, final report in CSV format that consolidates all extracted information, making it easy to analyze and share.

## Tech Stack*   **Primary Language**: Python
*   **AI & Machine Learning**: Llama 3.2 (Local LLM), Ollama
*   **Data Sources & APIs**: NCBI E-utilities, PyMed
*   **Data Formats**: JSONL, CSV, XML
*   **Core Libraries**: `requests`, `tqdm`, `ollama`, `pymed`

## How It WorksThe project operates as a three-stage, sequential pipeline. Each script performs a distinct part of the workflow, creating intermediate files that serve as the input for the next stage.1.  **Stage 1: Data Harvesting (`harvester.py`)**
    *   Connects to the NCBI PubMed database.
    *   Searches for relevant clinical case reports based on a specific query.
    *   Downloads the raw text abstracts and saves them to `patients_abstracts.txt`.

2.  **Stage 2: AI-Powered Extraction (`prep_extractor.py`)**
    *   Reads the raw abstracts from the text file.
    *   Uses a local Llama 3.2 model to analyze each abstract and extract the four key PREP data points.
    *   Saves the structured data to an intermediate `prep_extractions.jsonl` file, ensuring progress is not lost.

3.  **Stage 3: Evidence Matching & Reporting (`article_matcher.py`)**
    *   Reads the structured PREP data from the JSONL file.
    *   Performs a targeted PubMed search for each case to find matching scientific articles.
    *   Consolidates all the information and generates the final, user-friendly report: `final_patient_reports.csv`.

## Getting Started### Prerequisites*   Python 3.10 or higher installed.
*   [Ollama](https://ollama.com/) installed and running on your local machine.
*   The Llama 3.2 model pulled via Ollama (`ollama pull llama3.2`).
*   A personal API key from [NCBI](https://www.ncbi.nlm.nih.gov/account/).

### Setup & Installation1.  **Clone the repository:**
    ```bash
    git clone https://github.com/madhunayani/Clinical-Case-Analysis-AI.git
    cd Clinical-Case-Analysis-AI
    ```

2.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure your API key and settings:**
    *   Open the `config.py` file.
    *   Add your NCBI email and API key.
    *   Set the `PATIENT_COUNT` to your desired number (e.g., 1000).

### Running the PipelineExecute the scripts in the following order from your terminal. Each script must complete successfully before running the next.

1.  **Harvest Data:**
    ```bash
    python harvester.py
    ```

2.  **Extract PREP Data:**
    ```bash
    python prep_extractor.py
    ```

3.  **Generate Final Report:**
    ```bash
    python article_matcher.py
    ```
The final, comprehensive report will be saved as `final_patient_reports.csv` in your project directory.

## LicenseThis project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
