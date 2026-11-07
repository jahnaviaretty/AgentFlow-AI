import re
from collections import Counter


class PythonTools:
    """Provides text analysis tools for AI agents."""

    def analyze_text(self, text: str) -> dict:

        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        words = re.findall(r"\b[\w']+\b", text.lower())
        sentences = re.split(r"[.!?]+", text)

        word_count = len(words)
        sentence_count = sum(
            1 for sentence in sentences if sentence.strip()
        )

        common_words = Counter(words).most_common(5)

        return {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "unique_words": len(set(words)),
            "most_common_words": common_words
        }


if __name__ == "__main__":
    tool = PythonTools()

    sample_text = """
    Artificial intelligence helps machines learn.
    Machine learning is a part of artificial intelligence.
    AI agents can analyze information and execute tasks.
    """

    result = tool.analyze_text(sample_text)

    print("\nAGENTFLOW AI - PYTHON TOOLS")
    print("-" * 40)

    for key, value in result.items():
        print(f"{key}: {value}")