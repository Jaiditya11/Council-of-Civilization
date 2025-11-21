import os
import glob
import uuid
from pypdf import PdfReader
from .vector_db import VectorDB
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_text_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def load_pdf_file(filepath):
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def chunk_text(text, chunk_size=1000, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def ingest_documents(memories_dir="memories", vector_db_path="chroma_db"):
    db = VectorDB(persist_directory=vector_db_path)
    
    # Iterate over subdirectories in memories/ (each is a domain)
    for domain in os.listdir(memories_dir):
        domain_path = os.path.join(memories_dir, domain)
        if not os.path.isdir(domain_path):
            continue
            
        logger.info(f"Processing domain: {domain}")
        
        # Find all files
        files = glob.glob(os.path.join(domain_path, "*"))
        
        documents = []
        metadatas = []
        ids = []
        
        for filepath in files:
            filename = os.path.basename(filepath)
            try:
                if filepath.endswith('.txt') or filepath.endswith('.md'):
                    text = load_text_file(filepath)
                elif filepath.endswith('.pdf'):
                    text = load_pdf_file(filepath)
                else:
                    logger.warning(f"Skipping unsupported file: {filename}")
                    continue
                
                chunks = chunk_text(text)
                for i, chunk in enumerate(chunks):
                    documents.append(chunk)
                    metadatas.append({"source": filename, "domain": domain, "chunk_id": i})
                    ids.append(f"{domain}_{filename}_{i}_{uuid.uuid4()}")
                    
            except Exception as e:
                logger.error(f"Error processing {filename}: {e}")
        
        if documents:
            db.add_documents(domain, documents, metadatas, ids)
            logger.info(f"Ingested {len(documents)} chunks for domain {domain}")

if __name__ == "__main__":
    ingest_documents()
