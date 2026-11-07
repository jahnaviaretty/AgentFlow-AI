from typing import TypedDict


class TaskPlan(TypedDict):
    original_query: str
    steps: list[str]
    status: str


class PlannerAgent:
    """Breaks a user request into manageable tasks."""

    def create_plan(self, user_query: str) -> TaskPlan:

        if not user_query or not user_query.strip():
            raise ValueError("Please enter a valid task.")

        query = user_query.strip()

        plan = TaskPlan(
            original_query=query,
            steps=[
                "Understand and analyze the user's request.",
                "Identify the information or documents required.",
                "Research the relevant information.",
                "Execute the required task using available tools.",
                "Evaluate the result and prepare the final response."
            ],
            status="Plan created"
        )

        return plan


if __name__ == "__main__":
    planner = PlannerAgent()

    sample_query = "Analyze a PDF document and summarize its important points."

    result = planner.create_plan(sample_query)

    print("\nAGENTFLOW AI - PLANNER AGENT")
    print("-" * 40)
    print("User Request:", result["original_query"])
    print("\nGenerated Task Plan:")

    for number, step in enumerate(result["steps"], start=1):
        print(f"{number}. {step}")

    print("\nStatus:", result["status"])