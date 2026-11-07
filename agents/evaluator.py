
import re


class EvaluatorAgent:
    """Evaluates response relevance using keywords and intent evidence."""

    STOPWORDS = {
        "what", "which", "who", "when", "where", "why", "how",
        "is", "are", "was", "were", "the", "a", "an", "in",
        "on", "at", "of", "for", "to", "from", "and", "or",
        "with", "this", "that", "these", "those", "my", "your",
        "me", "do", "does", "can", "could", "please", "tell",
        "give", "show", "list", "listed", "explain", "describe",
        "summarize", "resume"
    }

    INTENT_INDICATORS = {
        "skills": [
            "programming languages",
            "libraries",
            "frameworks",
            "data visualization",
            "databases",
            "technologies",
            "tools",
            "platforms",
            "python",
            "sql",
            "java",
            "machine learning"
        ],
        "projects": [
            "developed", "built", "implemented",
            "application", "project", "github"
        ],
        "education": [
            "bachelor", "b.tech", "degree",
            "university", "college", "cgpa"
        ],
        "experience": [
            "internship", "intern", "company",
            "professional experience", "work experience"
        ],
        "certificates": [
            "certification", "certificate",
            "oracle", "salesforce", "servicenow",
            "forage"
        ]
    }

    def _tokens(self, text):
        return {
            word for word in re.findall(
                r"[a-zA-Z0-9+#.]+", text.lower()
            )
            if word not in self.STOPWORDS and len(word) > 1
        }

    def _detect_intent(self, query):
        query = query.lower()

        if "skill" in query or "technical" in query:
            return "skills"

        if "project" in query:
            return "projects"

        if "education" in query or "degree" in query:
            return "education"

        if "internship" in query or "experience" in query:
            return "experience"

        if "certif" in query:
            return "certificates"

        return None

    def evaluate(self, query: str, response: str) -> dict:

        if not query or not query.strip():
            raise ValueError("User query cannot be empty.")

        if not response or not response.strip():
            return {
                "score": 0,
                "status": "Needs improvement",
                "feedback": "The response is empty."
            }

        query_words = self._tokens(query)
        response_words = self._tokens(response)

        matched_words = query_words.intersection(response_words)

        keyword_relevance = (
            len(matched_words) / len(query_words)
            if query_words else 0
        )

        intent = self._detect_intent(query)

        if intent:
            indicators = self.INTENT_INDICATORS[intent]

            matched_indicators = [
                indicator for indicator in indicators
                if indicator in response.lower()
            ]

            intent_relevance = min(
                len(matched_indicators) / 4, 1.0
            )

            relevance = (
                0.70 * intent_relevance
                + 0.30 * keyword_relevance
            )

        else:
            relevance = keyword_relevance

        score = round(relevance * 100)

        if score >= 70:
            status = "Good response"
            feedback = (
                "The response contains relevant information "
                "related to the user's question."
            )
        elif score >= 40:
            status = "Partially relevant"
            feedback = (
                "The response contains some relevant information, "
                "but may need more details."
            )
        else:
            status = "Needs improvement"
            feedback = (
                "The response may not contain enough information "
                "related to the user's question."
            )

        return {
            "score": score,
            "status": status,
            "feedback": feedback
        }


if __name__ == "__main__":

    evaluator = EvaluatorAgent()

    query = "What certifications are listed in my resume?"

    response = """
    ServiceNow Micro-Certification
    Data Visualization – Forage
    Oracle AI / Oracle University Certification
    Salesforce Agentforce Certification
    """

    result = evaluator.evaluate(query, response)

    print("\nAGENTFLOW AI - EVALUATOR AGENT")
    print("-" * 40)
    print("Query:", query)
    print("Evaluation Score:", result["score"], "%")
    print("Status:", result["status"])
    print("Feedback:", result["feedback"])
