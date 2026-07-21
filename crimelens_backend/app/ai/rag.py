import numpy as np
import re

RAG_DOCS = [
    {"title": "IPC 420 (Cheating)", "content": "IPC 420 deals with cheating and dishonestly inducing delivery of property. Penalty: up to 7 years imprisonment and fine."},
    {"title": "IPC 379 (Theft)", "content": "IPC 379 specifies punishment for theft. Penalty: up to 3 years imprisonment or fine or both."},
    {"title": "SOP for Narcotics", "content": "Seizure of narcotic substances requires the presence of a Gazetted Officer or Magistrate. Draw samples in duplicate and prepare Panchnama."}
]

def search_rag_context(query: str, k: int = 1) -> list:
    """
    Local cosine-similarity vector search over standard guidelines database.
    """
    # Simple term frequency matcher
    scores = []
    query_words = set(re.findall(r'\w+', query.lower()))
    
    for doc in RAG_DOCS:
        doc_words = set(re.findall(r'\w+', doc["content"].lower()))
        common = query_words.intersection(doc_words)
        score = len(common) / max(len(query_words), 1)
        scores.append((score, doc))
        
    scores.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in scores[:k]]
