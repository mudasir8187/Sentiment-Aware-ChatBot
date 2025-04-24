import json
from gemini_client import GeminiClient

class SentimentAnalyzer:
    def __init__(self):
        """Initialize the sentiment analyzer."""
        self.gemini_client = GeminiClient()
        
    def analyze_sentiment(self, text):
        """
        Analyze the sentiment of the given text using Gemini API.
        
        Args:
            text (str): The text to analyze
            
        Returns:
            dict: A dictionary containing sentiment analysis results
        """
        if not text:
            return {
                'sentiment': 'neutral',
                'confidence': 1.0,
                'emotion': None,
                'explanation': 'Empty input'
            }
        
        # Create a prompt for sentiment analysis with explicit formatting instructions
        prompt = f"""
        Task: Analyze the sentiment and emotion in the following text.
        
        Text to analyze: "{text}"
        
        Instructions:
        1. Determine if the sentiment is positive, negative, or neutral
        2. Identify a specific emotion if present (e.g., happy, sad, angry, afraid, surprised, disgusted)
        3. Provide a brief explanation for your analysis
        4. Rate your confidence in this analysis on a scale of 0.0 to 1.0
        
        Format your response as a valid JSON object with these exact keys:
        {{
          "sentiment": "positive/negative/neutral",
          "confidence": 0.0-1.0,
          "emotion": "specific emotion or null if none detected",
          "explanation": "brief explanation of your analysis"
        }}
        
        Return ONLY the JSON object, nothing else.
        """
        
        try:
            # Generate response from Gemini
            response_text = self.gemini_client.generate_content(prompt)
            
            if not response_text:
                return {
                    'sentiment': 'neutral',
                    'confidence': 0.5,
                    'emotion': None,
                    'explanation': 'Failed to get response from Gemini API'
                }
            
            # Extract JSON from response
            try:
                # Clean the response text to ensure it's valid JSON
                json_str = response_text.strip()
                
                # Remove any markdown code block formatting if present
                if json_str.startswith('```json'):
                    json_str = json_str[7:]
                elif json_str.startswith('```'):
                    json_str = json_str[3:]
                
                if json_str.endswith('```'):
                    json_str = json_str[:-3]
                
                json_str = json_str.strip()
                
                # Debug output
                print(f"Attempting to parse JSON: {json_str[:100]}...")
                
                # Parse JSON
                result = json.loads(json_str)
                
                # Ensure required fields are present
                if 'sentiment' not in result:
                    result['sentiment'] = 'neutral'
                if 'confidence' not in result:
                    result['confidence'] = 0.5
                if 'emotion' not in result:
                    result['emotion'] = None
                if 'explanation' not in result:
                    result['explanation'] = 'No explanation provided'
                    
                return result
                
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
                print(f"Response text: {response_text}")
                
                # If JSON parsing fails, extract information manually
                sentiment = "neutral"
                emotion = None
                explanation = "Failed to parse JSON response"
                
                # Try to extract sentiment from text
                if "positive" in response_text.lower():
                    sentiment = "positive"
                elif "negative" in response_text.lower():
                    sentiment = "negative"
                
                # Try to extract emotion keywords
                emotion_keywords = {
                    'happy': ['happy', 'joy', 'delighted', 'pleased', 'glad', 'excited'],
                    'sad': ['sad', 'unhappy', 'depressed', 'down', 'miserable', 'heartbroken'],
                    'angry': ['angry', 'mad', 'furious', 'annoyed', 'irritated', 'frustrated'],
                    'afraid': ['afraid', 'scared', 'frightened', 'terrified', 'anxious', 'worried'],
                    'surprised': ['surprised', 'shocked', 'amazed', 'astonished', 'stunned'],
                    'disgusted': ['disgusted', 'revolted', 'repulsed', 'sickened']
                }
                
                for emo, keywords in emotion_keywords.items():
                    if any(keyword in response_text.lower() for keyword in keywords):
                        emotion = emo
                        break
                
                return {
                    'sentiment': sentiment,
                    'confidence': 0.5,
                    'emotion': emotion,
                    'explanation': explanation,
                    'raw_response': response_text
                }
                
        except Exception as e:
            # Handle API errors
            print(f"Error in sentiment analysis: {e}")
            return {
                'sentiment': 'neutral',
                'confidence': 0.0,
                'emotion': None,
                'explanation': f'Error: {str(e)}'
            }
