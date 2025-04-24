import streamlit as st
import os
import sys

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from sentiment_analysis import SentimentAnalyzer
from response_generation import ResponseGenerator
from conversation_manager import ConversationManager

def get_sentiment_color(sentiment):
    """Get a color based on sentiment."""
    if sentiment == "positive":
        return "#28a745"  # Green
    elif sentiment == "negative":
        return "#dc3545"  # Red
    else:
        return "#6c757d"  # Gray

def main():
    # Set up the page
    st.set_page_config(
        page_title="Sentiment-Aware Chatbot",
        page_icon="💬",
        layout="wide"
    )
    
    # Add custom CSS for styling
    st.markdown("""
    <style>
    .sentiment-badge {
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.8em;
        color: white;
        display: inline-block;
        margin-left: 10px;
    }
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create sidebar
    with st.sidebar:
        st.title("Sentiment-Aware Chatbot")
        st.markdown("This chatbot uses Gemini API to detect emotions in your messages and respond appropriately.")
        
        # Add option to clear conversation
        if st.button("Clear Conversation"):
            st.session_state.conversation_manager.clear_conversation()
            st.session_state.messages = []
            st.rerun()
            
        # Display sentiment statistics if available
        if 'sentiment_stats' in st.session_state:
            st.subheader("Conversation Sentiment")
            stats = st.session_state.sentiment_stats
            
            # Create a simple bar chart
            st.bar_chart(stats)
            
        st.markdown("---")
        st.markdown("Built with Gemini API")
    
    # Main content
    st.title("Sentiment-Aware Chatbot")
    
    # Initialize session state
    if 'sentiment_analyzer' not in st.session_state:
        st.session_state.sentiment_analyzer = SentimentAnalyzer()
        
    if 'response_generator' not in st.session_state:
        st.session_state.response_generator = ResponseGenerator()
        
    if 'conversation_manager' not in st.session_state:
        st.session_state.conversation_manager = ConversationManager()
        
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        
    if 'sentiment_stats' not in st.session_state:
        st.session_state.sentiment_stats = {
            'positive': 0,
            'negative': 0,
            'neutral': 0
        }
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if "sentiment" in message and message["sentiment"]:
                sentiment = message["sentiment"].get("sentiment", "neutral")
                emotion = message["sentiment"].get("emotion", "")
                
                # Display message with sentiment badge
                sentiment_html = f"""
                <div>
                    {message["content"]}
                    <span class="sentiment-badge" style="background-color: {get_sentiment_color(sentiment)}">
                        {sentiment}{f" • {emotion}" if emotion else ""}
                    </span>
                </div>
                """
                st.markdown(sentiment_html, unsafe_allow_html=True)
                
                # Show sentiment details in an expander
                with st.expander("Sentiment Details"):
                    st.json(message["sentiment"])
            else:
                st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Analyze sentiment
        with st.spinner("Analyzing sentiment..."):
            sentiment_result = st.session_state.sentiment_analyzer.analyze_sentiment(prompt)
            
            # Update sentiment statistics
            sentiment = sentiment_result.get('sentiment', 'neutral')
            st.session_state.sentiment_stats[sentiment] += 1
        
        # Add user message to conversation manager
        st.session_state.conversation_manager.add_message(prompt, "user", sentiment_result)
        
        # Get conversation history
        conversation_history = st.session_state.conversation_manager.get_conversation_history()
        
        # Generate response
        with st.spinner("Thinking..."):
            response = st.session_state.response_generator.generate_response(
                prompt, 
                sentiment_result, 
                conversation_history
            )
        
        # Add assistant response to conversation manager
        st.session_state.conversation_manager.add_message(response, "assistant")
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response, "sentiment": sentiment_result})
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.write(response)
        
        # Save conversation
        st.session_state.conversation_manager.save_conversation()

if __name__ == "__main__":
    main()
