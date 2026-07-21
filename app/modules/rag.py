import os
import re
import numpy as np

# Sample KSP Standard Operating Procedures (SOPs) and IPC Guideline Docs
KSP_GUIDELINES = [
    {
        "content": "IPC 420: Cheating and dishonestly inducing delivery of property. Penalty is imprisonment up to 7 years and fine. Non-bailable, cognizable offense.",
        "title": "IPC 420 - Cheating",
        "category": "Legal Code"
    },
    {
        "content": "IPC 379: Punishment for theft. Imprisonment up to 3 years, or fine, or both. Bailable, cognizable offense.",
        "title": "IPC 379 - Theft",
        "category": "Legal Code"
    },
    {
        "content": "IPC 354: Assault or criminal force to woman with intent to outrage her modesty. Imprisonment for 1 to 5 years and fine. Non-bailable, cognizable.",
        "title": "IPC 354 - Outraging Modesty",
        "category": "Legal Code"
    },
    {
        "content": "NDPS Act Sec 20: Seizure and punishment for contravention in relation to cannabis (Ganja). Small quantity: up to 1 year; Commercial quantity: 10 to 20 years rigorous imprisonment.",
        "title": "NDPS Act Sec 20 - Narcotics",
        "category": "Legal Code"
    },
    {
        "content": "IT Act Sec 66D: Punishment for cheating by personation by using computer resources. Imprisonment up to 3 years and fine up to Rs 1 Lakh.",
        "title": "IT Act Sec 66D - Cyber Fraud",
        "category": "Legal Code"
    },
    {
        "content": "SOP for Cyber Crime Financial Fraud: 1. Immediately request freezing of beneficiary bank accounts. 2. Fetch IP logs from ISP. 3. Register complaint on National Cyber Crime Reporting Portal (1930). 4. Request transaction chargeback history.",
        "title": "Cyber Fraud SOP",
        "category": "SOP"
    },
    {
        "content": "SOP for Narcotics Drug Seizure: 1. Inform nearest Gazetted Officer or Magistrate. 2. Conduct search in their presence under NDPS Section 50. 3. Draw samples in duplicate, seal with official seal. 4. Prepare Panchnama (seizure memo) with independent witnesses.",
        "title": "Narcotics Seizure SOP",
        "category": "SOP"
    },
    {
        "content": "SOP for Crime Scene Management: 1. Cordon off the area immediately. 2. Prevent contamination of physical evidence. 3. Call scientific officers / forensic team. 4. Record high-resolution photographs and videos of the scene.",
        "title": "Crime Scene SOP",
        "category": "SOP"
    }
]

# Simple Local Embeddings & Vector Store using NumPy
class LocalVectorStore:
    def __init__(self):
        self.vocab = {}
        self.docs = []
        self.vectors = []

    def _build_vocab(self):
        words = set()
        for doc in KSP_GUIDELINES:
            text = doc["content"] + " " + doc["title"] + " " + doc["category"]
            for w in re.findall(r'\w+', text.lower()):
                words.add(w)
        self.vocab = {w: i for i, w in enumerate(sorted(words))}

    def _get_vector(self, text):
        vec = np.zeros(max(len(self.vocab), 1))
        if not self.vocab:
            return vec
        for w in re.findall(r'\w+', text.lower()):
            if w in self.vocab:
                vec[self.vocab[w]] += 1
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec

    def fit_and_index(self):
        self._build_vocab()
        self.docs = KSP_GUIDELINES
        self.vectors = [self._get_vector(doc["content"]) for doc in self.docs]

    def similarity_search(self, query: str, k: int = 2):
        if not self.vectors:
            self.fit_and_index()
        query_vec = self._get_vector(query)
        scores = []
        for i, doc_vec in enumerate(self.vectors):
            dot_product = np.dot(query_vec, doc_vec)
            scores.append((dot_product, self.docs[i]))
        # Sort by similarity score descending
        scores.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in scores[:k]]

# Singleton instances for optional imports
_vector_store = LocalVectorStore()
_vector_store.fit_and_index()

def get_vector_store():
    return _vector_store

def retrieve_guidelines(query: str, k: int = 2):
    """
    Retrieves the top k most relevant guidelines/legal sections for a given query.
    """
    return _vector_store.similarity_search(query, k=k)

if __name__ == "__main__":
    res = retrieve_guidelines("How do I handle drug seizure and Ganja?")
    print("\nSearch results:")
    for r in res:
        print(f"- [{r['category']}] {r['title']}: {r['content']}")
