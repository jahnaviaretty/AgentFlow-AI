from pathlib import Path
from pypdf import PdfReader


class ResearchAgent:
    """Extracts and researches information from PDF documents."""

    def read_pdf(self, file_path: str) -> str:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {file_path}"
            )

        if path.suffix.lower() != ".pdf":
            raise ValueError("Only PDF files are supported.")

        reader = PdfReader(str(path))

        extracted_text = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text()

            if text:
                extracted_text.append(
                    f"Page {page_number}:\n{text}"
                )

        if not extracted_text:
            return "No readable text found in this PDF."

        return "\n\n".join(extracted_text)


if __name__ == "__main__":
    researcher = ResearchAgent()

    print("AGENTFLOW AI - RESEARCH AGENT")
    print("-" * 40)
    print("Research Agent initialized successfully!")
    print("Ready to read PDF documents.")