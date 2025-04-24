import google.generativeai as genai
import os

class GeminiClient:
    def __init__(self):
        """Initialize the Gemini API client with gemini-1.5-flash."""
        api_key = "AIzaSyD89K3YCXhmdfX42MNOOxV5dnGUo7m-yYY"
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        
        genai.configure(api_key=api_key)

        # Preferred model name
        self.model_name = "models/gemini-1.5-flash"
        
        try:
            # Optional: Validate if the preferred model exists
            models = genai.list_models()
            available_models = [model.name for model in models]
            
            if self.model_name not in available_models:
                raise ValueError(f"Preferred model {self.model_name} is not available.")
            
            print(f"Using Gemini model: {self.model_name}")
            self.model = genai.GenerativeModel(self.model_name)
        
        except Exception as e:
            print(f"Error initializing Gemini model: {e}")
            raise
        
    def generate_content(self, prompt):
        """Generate content using Gemini API."""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating content: {e}")
            return None
            
    def create_chat(self, history=None):
        """Create a chat session with optional history."""
        if history is None:
            history = []
        
        return self.model.start_chat(history=history)
