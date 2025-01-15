# AI-Based Search Module

## Overview
The AI-Based Search Module is designed to address the challenge of finding the perfect product online by interpreting user prompts and recommending relevant products. The system uses a lightweight AI model (Llama 3.2) with FAISS embeddings for a knowledge base-driven keyword extraction process. It ensures that recommendations are based on existing product data.

---

## Motivation
This project was inspired by a real-life scenario where finding the right gift on short notice was challenging. The goal is to provide a virtual customer service experience, allowing users to describe their needs in natural language while the system generates precise keywords to find the perfect match from a product database.

---

## Features
1. **AI-Powered Keyword Extraction**:
   - Uses Llama 3.2 lightweight 11B model via Groq API.
   - Generates keywords based on product descriptions, categories, and names.

2. **Knowledge Base Integration**:
   - Embeddings are created using FAISS and stored for efficient similarity searches.
   - Ensures generated keywords align with available database entries.

3. **Image Collection and Filtering**:
   - Collects images using Selenium and Pinterest.
   - Filters product images using the `colander.py` script powered by AI classification.

4. **Database Management**:
   - Stores product details, images, and URLs in a structured database.
   - Updates knowledge base embeddings daily to maintain relevance.

---

## Project Structure
```
📁 project_root/
├── 📁 ai_module/
│   ├── q_to_k.py                # Handles prompt-to-keyword generation.
│   ├── embeddings.py            # Creates and searches FAISS embeddings.
│   ├── colander.py              # Filters images to classify product images.
├── 📁 database/
│   ├── knowledgebase_index.faiss # FAISS index for knowledge base.
│   ├── metadata.json            # Metadata for FAISS.
├── 📁 media/                    # Stores filtered product images.
├── 📁 temp/                     # Temporary storage for downloaded images.
├── extract_images.py            # Selenium script for image collection.
├── main.py                      # Entry point for the AI-powered search module.
├── setup.py                     # Initializes and processes project data.
├── runserver.py                 # Launches the Uvicorn server.
├── requirements.txt             # Python dependencies.
└── README.md                    # Project documentation.
```

---

## Setup and Usage

### Prerequisites
- Python 3.8 or higher
- ChromeDriver installed
- Necessary API keys for Groq and Pinterest (set in `config.py`)

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd project_root
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure API keys in `config.py`:
   ```python
   GROQ_API_KEY = "your-groq-api-key"
   emailp = "your-pinterest-email"
   passwordp = "your-pinterest-password"
   ```

4. Set up the database and embeddings:
   - Ensure `metadata.json` and `knowledgebase_index.faiss` are populated.

### Execution Process
1. **Setup Scripts**:
   - Use the `setup.py` script to initialize necessary modules and process data:
     ```bash
     python setup.py
     ```
     - Executes the following steps:
       1. Runs `search.py` for data extraction.
       2. Runs `extract_image.py` to collect images via Selenium.
       3. Runs `extract_knowledgebase.py` to populate the knowledge base.
       4. Runs `embeddings.py` to create and update FAISS embeddings.

2. **Start Server**:
   - Launch the Uvicorn server with the `runserver.py` script:
     ```bash
     python runserver.py
     ```
     - Starts the application, making it accessible locally with hot-reloading enabled.

3. **Selenium Script for Image Collection**:
   - Add images to temp_media from URLs of `urls.txt` and uses llama 3.3 vision to classify the image if it is a product.
   - Run the script to collect and filter images:
     ```bash
     python extract_images.py
     ```
   - Valid images are stored in the `media/` folder, and their metadata is updated in the database.

---

## Selenium Image Collection Workflow
- **Login to Pinterest**: Automates login to Pinterest using provided credentials.
- **Image Collection**: Scrapes images from given URLs and stores them temporarily.
- **Image Filtering**: Passes images through the `colander.py` script to classify and save product images.
- **Database Insertion**: Saves valid images and their associated URLs to the database.



## Technical Details
- **FAISS**:
  - Used for fast similarity search in the knowledge base.
  - Embeddings created with `all-MiniLM-L6-v2` model.

- **Llama 3.2 via Groq**:
  - Processes prompts and generates relevant keywords.

- **Image Classification**:
  - AI classifier identifies product images.


## Contact
For questions or support, feel free to contact the project maintainer.
