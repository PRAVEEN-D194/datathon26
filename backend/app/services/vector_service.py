import numpy as np
from typing import List, Dict, Any, Tuple
from app.core.logging import logger

class VectorService:
    def __init__(self):
        self.model = None
        self.index = None
        self.documents: List[Dict[str, Any]] = []
        self.embeddings: List[np.ndarray] = []
        
        # Try to load SentenceTransformers and FAISS
        try:
            from sentence_transformers import SentenceTransformer
            import faiss
            logger.info("Initializing SentenceTransformer and FAISS index...")
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            # Dimension of all-MiniLM-L6-v2 is 384
            self.index = faiss.IndexFlatL2(384)
            self.use_heavy_ml = True
        except ImportError as e:
            logger.warning(f"SentenceTransformers/FAISS not fully available ({e}). Using cosine-similarity fallback.")
            self.use_heavy_ml = False

    def add_documents(self, docs: List[Dict[str, Any]], text_field: str = "description"):
        """
        Embed and index a list of crime records or files.
        """
        if not docs:
            return
            
        self.documents.extend(docs)
        texts = [d.get(text_field, "") for d in docs]
        
        if self.use_heavy_ml and self.model and self.index:
            try:
                embeddings = self.model.encode(texts)
                embeddings_np = np.array(embeddings).astype('float32')
                self.index.add(embeddings_np)
                return
            except Exception as e:
                logger.error(f"Error indexing vectors with FAISS: {e}. Falling back...")
                
        # Cosine fallback embedding simulation (Bag of Words / hash matching)
        for text in texts:
            self.embeddings.append(self._get_simple_embedding(text))

    def _get_simple_embedding(self, text: str) -> np.ndarray:
        """Simple TF-IDF style BoW feature vector of size 128 for fallback."""
        words = text.lower().split()
        vector = np.zeros(128, dtype=np.float32)
        for w in words:
            # Simple hash indexing
            idx = hash(w) % 128
            vector[idx] += 1.0
        # Normalize
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        return vector

    def search_similar(self, query: str, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """
        Search for documents matching query text.
        """
        if not self.documents:
            return []
            
        top_k = min(top_k, len(self.documents))
        
        if self.use_heavy_ml and self.model and self.index:
            try:
                query_vector = self.model.encode([query])
                query_np = np.array(query_vector).astype('float32')
                distances, indices = self.index.search(query_np, top_k)
                
                results = []
                for i in range(len(indices[0])):
                    idx = indices[0][i]
                    if idx < len(self.documents):
                        # FAISS return L2 distance, convert to similarity metric
                        score = float(1.0 / (1.0 + distances[0][i]))
                        results.append((self.documents[idx], score))
                return results
            except Exception as e:
                logger.error(f"FAISS search failed: {e}. Falling back...")

        # Fallback manual similarity matching
        query_vector = self._get_simple_embedding(query)
        scores = []
        for idx, doc_vector in enumerate(self.embeddings):
            # Cosine similarity
            score = float(np.dot(query_vector, doc_vector))
            scores.append((self.documents[idx], score))
            
        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        return scores[:top_k]

# Singleton instance
vector_service = VectorService()
