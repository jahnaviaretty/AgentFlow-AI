
import ast
import operator
import re


class ExecutionAgent:
    """Safely performs calculations and extracts PDF information."""

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    STOPWORDS = {
        "what", "which", "who", "when", "where", "why", "how",
        "is", "are", "was", "were", "the", "a", "an", "in",
        "on", "at", "of", "for", "to", "from", "and", "or",
        "with", "this", "that", "these", "those", "my", "your",
        "their", "it", "be", "do", "does", "can", "could",
        "listed", "include", "includes", "included", "show",
        "tell", "give", "please", "me", "about", "mentioned",
        "explain", "describe", "summarize"
    }

    SECTION_PATTERNS = {
        "skills": r"technical\s+skills",
        "education": r"education",
        "experience": r"experience",
        "projects": r"projects",
        "certificates": r"certificates|certifications",
        "objective": r"objective"
    }

    SECTION_ENDINGS = {
        "skills": (
            r"experience|projects|certificates|certifications|"
            r"objective|education"
        ),
        "education": (
            r"technical\s+skills|skills|experience|projects|"
            r"certificates|certifications|objective"
        ),
        "experience": (
            r"projects|certificates|certifications|objective|education"
        ),
        "projects": (
            r"certificates|certifications|objective|education"
        ),
        "certificates": (
            r"objective|education|technical\s+skills|experience|projects"
        ),
        "objective": (
            r"education|technical\s+skills|experience|projects"
        )
    }

    SKILL_CATEGORIES = [
        "Programming Languages",
        "Libraries & Frameworks",
        "Frameworks",
        "Data Visualization",
        "Databases",
        "AI/ML Technologies",
        "Web Technologies",
        "Tools & Platforms"
    ]

    def calculate(self, expression: str):
        """Evaluate mathematical expressions without eval()."""
        try:
            tree = ast.parse(expression, mode="eval")
            return self._evaluate(tree.body)
        except (
            ValueError, TypeError, ZeroDivisionError,
            OverflowError, SyntaxError
        ) as error:
            return f"Calculation error: {error}"

    def _evaluate(self, node):
        if isinstance(node, ast.Constant):
            if type(node.value) in (int, float):
                return node.value
            raise ValueError("Only numbers are allowed.")

        if isinstance(node, ast.BinOp):
            operation = self.OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported operation.")

            left = self._evaluate(node.left)
            right = self._evaluate(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError("Exponent is too large.")

            result = operation(left, right)

            if isinstance(result, (int, float)) and abs(result) > 1e100:
                raise ValueError("Result is too large.")

            return result

        if isinstance(node, ast.UnaryOp):
            operation = self.OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported operation.")

            return operation(self._evaluate(node.operand))

        raise ValueError("Invalid mathematical expression.")

    def _clean_text(self, text):
        text = text.replace("\x00", " ")
        text = text.replace("\u00a0", " ")
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _get_keywords(self, text):
        words = re.findall(r"\b[a-zA-Z0-9+#.]+\b", text.lower())

        return {
            word for word in words
            if word not in self.STOPWORDS and len(word) > 1
        }

    def _detect_section(self, query):
        query = query.lower()

        if "skill" in query or "technical" in query:
            return "skills"
        if "education" in query or "degree" in query:
            return "education"
        if "internship" in query or "experience" in query:
            return "experience"
        if "project" in query:
            return "projects"
        if "certif" in query:
            return "certificates"
        if "objective" in query or "summary" in query:
            return "objective"

        return None

    def _extract_requested_section(self, text, section):
        """Extract content between resume section headings."""

        start_pattern = self.SECTION_PATTERNS[section]

        start_match = re.search(
            rf"(?<![a-zA-Z])(?:{start_pattern})(?![a-zA-Z])",
            text,
            re.IGNORECASE
        )

        if not start_match:
            return ""

        remaining = text[start_match.end():]
        end_pattern = self.SECTION_ENDINGS[section]

        end_match = re.search(
            rf"(?<![a-zA-Z])(?:{end_pattern})(?![a-zA-Z])",
            remaining,
            re.IGNORECASE
        )

        if end_match:
            remaining = remaining[:end_match.start()]

        return remaining.strip(" :-•|")

    def _extract_items(self, text):
        """Split skill categories and remove duplicate categories."""

        category_names = [
            "Programming Languages",
            "Libraries & Frameworks",
            "Data Visualization",
            "Databases",
            "AI/ML Technologies",
            "Web Technologies",
            "Tools & Platforms",
            "Frameworks"
        ]

        category_pattern = (
            r"(?<![A-Za-z&])(?:"
            + "|".join(re.escape(name) for name in category_names)
            + r")\s*:"
        )

        text = re.sub(
            category_pattern,
            lambda match: "\n" + match.group(0),
            text,
            flags=re.IGNORECASE
        )

        raw_items = re.split(r"[•▪●·\n]+", text)

        selected = []
        seen_categories = set()
        seen_items = set()

        for item in raw_items:
            item = self._clean_text(item).strip(" :-|")

            if len(item) < 2:
                continue

            category_match = re.match(
                r"^([^:]{2,45}):\s*(.*)$",
                item
            )

            if category_match:
                category = category_match.group(1).strip()
                content = category_match.group(2).strip()

                if category.lower() == "frameworks":
                    category = "Libraries & Frameworks"

                category_key = category.lower()

                if category_key in seen_categories:
                    continue

                seen_categories.add(category_key)

                if content:
                    selected.append(f"{category}: {content}")

                continue

            normalized = re.sub(r"\s+", " ", item).lower()

            if normalized not in seen_items:
                seen_items.add(normalized)
                selected.append(item)

        return selected

    def answer_from_context(self, query: str, retrieved_context: list):
        """Extract relevant information from retrieved PDF chunks."""

        if not retrieved_context:
            return "No relevant information was found in the uploaded PDF."

        requested_section = self._detect_section(query)

        all_text = " ".join(
            self._clean_text(item.get("chunk", ""))
            for item in retrieved_context
        )

        if requested_section:
            section_text = self._extract_requested_section(
                all_text, requested_section
            )

            if not section_text:
                return (
                    f"The {requested_section} section was not found "
                    "in the retrieved PDF content."
                )

            all_text = section_text

        selected_items = self._extract_items(all_text)

        if not selected_items:
            return "No matching information was found in the uploaded PDF."

        return (
            "Answer based on the uploaded PDF:\n\n"
            + "\n".join(
                f"- {item}" for item in selected_items[:15]
            )
        )


if __name__ == "__main__":

    executor = ExecutionAgent()

    print("AGENTFLOW AI - EXECUTION AGENT")
    print("-" * 40)

    print("Calculation test:", executor.calculate("25 * 4 + 10"))

    sample_context = [
        {
            "chunk": (
                "Objective: Motivated student. Education: B.Tech. "
                "Technical Skills: Programming Languages: Python, SQL, "
                "Java (Basic) • Libraries & Frameworks: Pandas, NumPy, "
                "Scikit-learn, Flask, Streamlit, LangChain • "
                "Data Visualization: Power BI, Matplotlib, Seaborn, "
                "MS Excel • Databases: MySQL, SQLite"
            )
        },
        {
            "chunk": (
                "Frameworks: Pandas, NumPy, Scikit-learn, Flask, "
                "Streamlit, LangChain • Data Visualization: Power BI, "
                "Matplotlib, Seaborn, MS Excel • Databases: MySQL, "
                "SQLite • AI/ML Technologies: Machine Learning, "
                "Random Forest, FAISS, Hugging Face"
            )
        }
    ]

    print("\nDocument Answer:")
    print(
        executor.answer_from_context(
            "What technical skills are listed?",
            sample_context
        )
    )

    print("\nExecution completed!")
