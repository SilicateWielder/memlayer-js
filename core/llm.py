import openai
from core.config import settings

class LLMInterface:
    def __init__(self, api_key: str = settings.OPENAI_API_KEY):
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set in the environment.")
        self.client = openai.OpenAI(api_key=api_key)

    def get_embedding(self, text: str, model: str = "text-embedding-3-large") -> list[float]:
        """
        Generates an embedding for the given text using a specified OpenAI model.
        """
        text = text.replace("\n", " ")
        try:
            response = self.client.embeddings.create(input=[text], model=model)
            return response.data[0].embedding
        except Exception as e:
            print(f"Error getting embedding: {e}")
            # In a real app, you'd have more robust error handling
            return []

# A global instance that can be imported and used throughout the application
llm_interface = LLMInterface()