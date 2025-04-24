import sys
import os
import json

# Add the src directory to the Python path
sys.path.append(os.path.dirname(__file__))

from gemini_client import GeminiClient
from sentiment_analysis import SentimentAnalyzer

def test_gemini_models():
    """Test available Gemini models."""
    try:
        import google.generativeai as genai
        
        # Get API key from environment
        api_key = "AIzaSyD89K3YCXhmdfX42MNOOxV5dnGUo7m-yYY"
        if not api_key:
            print("ERROR: GOOGLE_API_KEY environment variable not set")
            print("Please set your API key in the .env file or directly in your environment")
            return False
            
        # Configure the API
        genai.configure(api_key=api_key)
        
        # List available models
        #print("Listing available models...")
        #models = genai.list_models()
        
        # Filter for Gemini models
        #gemini_models = [model for model in models if "gemini" in model.name.lower()]
        
        # if gemini_models:
        #     print(f"Found {len(gemini_models)} Gemini models:")
        #     for model in gemini_models:
        #         print(f"- {model.name}")
        #         print(f"  Supported generation methods: {model.supported_generation_methods}")
        #     return True
        # else:
        #     print("No Gemini models found. Please check your API key and permissions.")
        #     return False
    except Exception as e:
        print(f"Error testing Gemini models: {e}")
        return False

def test_sentiment_analysis():
    """Test sentiment analysis with detailed debugging."""
    print("\n" + "="*50)
    print("SENTIMENT ANALYSIS TEST")
    print("="*50)
    
    # First test if we can access Gemini models
    models_available = test_gemini_models()
    if not models_available:
        pass
        #print("\nWARNING: Could not access Gemini models. Continuing with test but expect failures.")
    
    # Initialize the analyzer
    print("\nInitializing sentiment analyzer...")
    analyzer = SentimentAnalyzer()
    
    # Test with different emotional expressions
    test_texts = [
        "I'm feeling really happy today!",
        "I'm so frustrated with this situation.",
        "I don't know how I feel about this.",
        "I'm excited about the new project but also nervous about the deadline.",
        "What the fuck!!"
    ]
    
    results = []
    
    for text in test_texts:
        print("\n" + "-"*50)
        print(f"Analyzing: \"{text}\"")
        
        # Analyze sentiment
        result = analyzer.analyze_sentiment(text)
        results.append(result)
        
        # Display results
        print("\nRESULTS:")
        print(f"Sentiment: {result['sentiment']}")
        print(f"Emotion: {result.get('emotion', 'None')}")
        print(f"Confidence: {result.get('confidence', 0):.2f}")
        print(f"Explanation: {result.get('explanation', 'None')}")
        
        # Show raw response if available
        if 'raw_response' in result:
            print("\nRAW RESPONSE:")
            print(result['raw_response'][:200] + "..." if len(result['raw_response']) > 200 else result['raw_response'])
    
    # Save results to a file for reference
    with open("sentiment_analysis_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "="*50)
    print(f"Test completed. Results saved to sentiment_analysis_results.json")
    print("="*50)

if __name__ == "__main__":
    test_sentiment_analysis()
