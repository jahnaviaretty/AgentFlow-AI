
import re
from pathlib import Path
from pypdf import PdfReader


class DocumentLoader:
    """Loads, cleans and splits PDF documents into meaningful chunks."""

    def load_pdf(self, file_path: str) -> str:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if path.suffix.lower() != ".pdf":
            raise ValueError("Only PDF documents are supported.")

        reader = PdfReader(str(path))
        pages = []

        for page_number, page in enumerate(reader.pages, start=1):

            text = page.extract_text()

            if text:
                text = self.clean_text(text)
                pages.append(text)

        return "\n\n".join(pages)

    def clean_text(self, text: str) -> str:
        """Remove unnecessary whitespace and normalize PDF text."""

        text = text.replace("\x00", " ")
        text = text.replace("\u00a0", " ")

        # Fix words broken by PDF line wrapping.
        text = re.sub(r"(?<=[a-zA-Z])-\s*\n\s*(?=[a-z])", "", text)

        # Preserve paragraph boundaries.
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r" *\n *", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    def split_text(
        self,
        text: str,
        chunk_size: int = 500,
        overlap: int = 50
    ) -> list:

        if chunk_size <= 0:
            raise ValueError("Chunk size must be positive.")

        if overlap < 0 or overlap >= chunk_size:
            raise ValueError("Overlap must be smaller than chunk size.")

        # Split by paragraphs before combining them into chunks.
        paragraphs = [
            paragraph.strip()
            for paragraph in text.split("\n")
            if paragraph.strip()
        ]

        chunks = []
        current_chunk = []
        current_word_count = 0

        for paragraph in paragraphs:

            words = paragraph.split()

            if not words:
                continue

            if len(words) > chunk_size:

                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                    current_chunk = []
                    current_word_count = 0

                start = 0

                while start < len(words):
                    end = start + chunk_size
                    chunks.append(" ".join(words[start:end]))
                    start += chunk_size - overlap

                continue

            if current_word_count + len(words) > chunk_size:

                if current_chunk:
                    chunks.append(" ".join(current_chunk))

                previous_words = " ".join(current_chunk).split()
                current_chunk = previous_words[-overlap:] if overlap else []
                current_word_count = len(current_chunk)

            current_chunk.extend(words)
            current_word_count += len(words)

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks


if __name__ == "__main__":

    loader = DocumentLoader()

    sample_text = (
        "Artificial intelligence helps machines learn from data.\n\n"
        "Machine learning is a branch of artificial intelligence.\n\n"
        "RAG combines information retrieval with language generation."
    )

    chunks = loader.split_text(
        sample_text,
        chunk_size=10,
        overlap=2
    )

    print("\nAGENTFLOW AI - DOCUMENT LOADER")
    print("-" * 40)
    print("Total chunks:", len(chunks))

    for index, chunk in enumerate(chunks, start=1):
        print(f"\nChunk {index}: {chunk}")
