
import pickle
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.pipeline import FeatureUnion


class VectorStore:
    """Stores document chunks and retrieves relevant information."""

    def __init__(self):
        self.vectorizer = FeatureUnion([
            (
                "word",
                TfidfVectorizer(
                    lowercase=True,
                    ngram_range=(1, 2),
                    token_pattern=r"(?u)\b\w+\b",
                    sublinear_tf=True
                )
            ),
            (
                "character",
                TfidfVectorizer(
                    analyzer="char_wb",
                    ngram_range=(2, 5),
                    sublinear_tf=True
                )
            )
        ])

        self.chunks = []
        self.vectors = None

    def add_documents(self, chunks: list):
        if not chunks:
            raise ValueError("No document chunks provided.")

        self.chunks = chunks

        self.vectors = self.vectorizer.fit_transform(chunks)

        print(f"Successfully indexed {len(chunks)} chunks.")

    def search(self, query: str, top_k: int = 3):
        if self.vectors is None:
            raise ValueError("Please add documents before searching.")

        if not query or not query.strip():
            raise ValueError("Search query cannot be empty.")

        if top_k < 1:
            raise ValueError("top_k must be at least 1.")

        query_vector = self.vectorizer.transform([query])

        scores = cosine_similarity(
            query_vector,
            self.vectors
        )[0]

        ranked_indices = scores.argsort()[::-1][:top_k]

        results = []

        for index in ranked_indices:
            score = float(scores[index])

            if score > 0:
                results.append({
                    "chunk": self.chunks[index],
                    "score": round(score, 4)
                })

        return results

    def save(self, file_path: str):
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "wb") as file:
            pickle.dump({
                "vectorizer": self.vectorizer,
                "chunks": self.chunks,
                "vectors": self.vectors
            }, file)

        print("Vector store saved successfully.")

    def load(self, file_path: str):
        with open(file_path, "rb") as file:
            data = pickle.load(file)

        self.vectorizer = data["vectorizer"]
        self.chunks = data["chunks"]
        self.vectors = data["vectors"]

        print("Vector store loaded successfully.")


if __name__ == "__main__":
    store = VectorStore()

    sample_chunks = [
        "Python supports integers, floats, strings and boolean data types.",
        "Machine learning enables computers to learn from data.",
        "RAG retrieves relevant documents before generating answers.",
        "Artificial intelligence enables machines to perform intelligent tasks."
    ]

    store.add_documents(sample_chunks)

    query = "What are Python data types?"

    print("\nAGENTFLOW AI - VECTOR SEARCH")
    print("-" * 40)
    print("Search query:", query)

    results = store.search(query, top_k=2)

    for number, result in enumerate(results, start=1):
        print(f"\nResult {number}")
        print("Score:", result["score"])
        print("Content:", result["chunk"])
