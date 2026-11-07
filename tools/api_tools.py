import requests


class APITools:
    """Provides safe HTTP API operations for agents."""

    def get_request(self, url: str, params: dict = None):
        if not url.startswith(("https://", "http://")):
            raise ValueError("Only HTTP and HTTPS URLs are supported.")

        try:
            response = requests.get(
                url,
                params=params,
                timeout=10
            )

            response.raise_for_status()

            try:
                return response.json()

            except ValueError:
                return response.text

        except requests.RequestException as error:
            return {
                "error": str(error)
            }


if __name__ == "__main__":
    api = APITools()

    print("\nAGENTFLOW AI - API TOOLS")
    print("-" * 40)

    # Public test API
    result = api.get_request(
        "https://jsonplaceholder.typicode.com/todos/1"
    )

    print("API Response:")
    print(result)