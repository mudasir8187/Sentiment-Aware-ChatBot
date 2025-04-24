from gemini_client import GeminiClient

class ResponseGenerator:
    def __init__(self):
        """Initialize the response generator."""
        self.gemini_client = GeminiClient()
        
    def generate_response(self, user_input, sentiment_result, conversation_history=None):
        """
        Generate a response using Gemini API based on user input and sentiment analysis.
        
        Args:
            user_input (str): The user's message
            sentiment_result (dict): The sentiment analysis result
            conversation_history (list, optional): List of previous messages
            
        Returns:
            str: The generated response
        """
        if not user_input:
            return "I didn't catch that. Could you please say something?"
            
        # Extract sentiment and emotion from the analysis result
        sentiment = sentiment_result.get('sentiment', 'neutral')
        emotion = sentiment_result.get('emotion', None)
        
        # Create a system prompt that includes sentiment information
        system_prompt = f"""
        You are an empathetic and supportive AI assistant similar to Replika. 
        The user's message has been analyzed as having a {sentiment} sentiment.
        """
        
        if emotion:
            system_prompt += f" They appear to be feeling {emotion}."
            
        system_prompt += """
        Respond in a way that acknowledges their emotional state and provides an appropriate, 
        supportive response. Keep your response concise (1-3 sentences) and conversational.
        Do not explicitly mention that you detected their sentiment or emotion - just respond naturally.
        """
        
        # Format conversation history for the prompt
        formatted_history = ""
        if conversation_history and len(conversation_history) > 0:
            formatted_history = "Previous conversation:\n"
            for i, message in enumerate(conversation_history[-10:]):  # Last 10 messages
                role = "User" if i % 2 == 0 else "Assistant"
                formatted_history += f"{role}: {message}\n"
        
        # Create the full prompt
        prompt = f"""
        {system_prompt}
        
        {formatted_history}
        
        User: {user_input}
        
        Assistant:
        """
        
        try:
            # Generate response from Gemini
            response = self.gemini_client.generate_content(prompt)
            
            if not response:
                return "I'm having trouble processing that right now. Could you try saying that differently?"
                
            return response.strip()
            
        except Exception as e:
            # Handle API errors
            print(f"Error generating response: {e}")
            return "I'm having trouble connecting right now. Please try again in a moment."
