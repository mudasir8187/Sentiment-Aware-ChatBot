from sentiment_analysis import SentimentAnalyzer
from response_generation import ResponseGenerator

analyzer = SentimentAnalyzer()
generator = ResponseGenerator()

# Test with different emotional expressions
test_texts = [
    "I'm feeling really happy today!",
    "I'm so frustrated with this situation.",
    "I don't know how I feel about this.",
    "I'm excited about the new project but also nervous about the deadline."
]

for text in test_texts:
    sentiment_result = analyzer.analyze_sentiment(text)
    response = generator.generate_response(text, sentiment_result)
    
    print(f"User: {text}")
    print(f"Sentiment: {sentiment_result['sentiment']}, Emotion: {sentiment_result.get('emotion', 'none')}")
    print(f"Bot: {response}")
    print("-" * 50)
