import requests
from typing import Dict, Optional

class DLMCommunicator:
    def __init__(self, base_url: str, api_key: Optional[str] = None, bearer_token: Optional[str] = None):
        """
        Initializes the DLMCommunicator with authentication details.

        :param base_url: The base URL of the mod-dlm API (e.g., 'https://mod.construction').
        :param api_key: API key for access (optional).
        :param bearer_token: Bearer token (JWT) for access (optional).
        """
        self.base_url = base_url
        self.headers = {}
        if api_key:
            self.headers["X-API-KEY"] = api_key
        if bearer_token:
            self.headers["Authorization"] = f"Bearer {bearer_token}"

    def create_element(self, element_data: Dict) -> Dict:
        """
        Sends a JSON payload to create a new element.

        :param element_data: The JSON object containing element data.
        :return: The response JSON from the API.
        :raises: Exception if the API call fails.
        """
        url = f"{self.base_url}/element"
        response = requests.post(url, json=element_data, headers=self.headers)

        if response.status_code == 201:
            return response.json()
        else:
            # Raise exception for unsuccessful API calls
            raise Exception(
                f"Failed to create element: {response.status_code} - {response.text}"
            )

if __name__ == "__main__":
    # Example element data
    element_data = {
        "name": "Wall Panel",
        "description": "A modular wall panel.",
        "boundingBox": {"width": 2000, "height": 3000, "depth": 150},
        "images": [],
        "buildingSystem": "Wall",
        "productCategory": "Solid Wall Panels",
        "material": {
            "finishMaterial": "Timber",
            "structuralMaterial": "Steel"
        },
        "dimensional": {
            "width": {"min": 1.5, "max": 2.5},
            "height": {"min": 2.5, "max": 3.5},
            "length": {"min": 0.5, "max": 1.0}
        }
    }

    # Initialize communicator
    base_url = "https://mod.construction"  # Replace with the actual base URL
    api_key = "your_api_key_here"  # Replace with your actual API key
    bearer_token = None  # Use bearer_token if applicable

    communicator = DLMCommunicator(base_url=base_url, api_key=api_key, bearer_token=bearer_token)

    try:
        response = communicator.create_element(element_data)
        print("Element created successfully:", response)
    except Exception as e:
        print("Error:", e)
