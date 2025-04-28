import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import your custom modules
from sentiment_analysis import SentimentAnalyzer
from response_generation import ResponseGenerator
from conversation_manager import ConversationManager

# Load environment variables
load_dotenv()

def get_sentiment_color(sentiment):
    """Return a color based on the sentiment."""
    if sentiment == "positive":
        return "#28a745"  # Green
    elif sentiment == "negative":
        return "#dc3545"  # Red
    else:
        return "#6c757d"  # Gray

def main():
    st.set_page_config(
        page_title="Sentiment-Aware Chatbot",
        page_icon="💬",
        layout="wide"
    )

    # Custom CSS
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

    # Sidebar
    with st.sidebar:
        st.title("Sentiment-Aware Chatbot")
        st.markdown("This chatbot uses Gemini API to detect emotions in your messages and respond appropriately.")

        if st.button("Clear Conversation"):
            st.session_state.conversation_manager.clear_conversation()
            st.session_state.messages = []
            st.rerun()

        if 'sentiment_stats' in st.session_state:
            st.subheader("Conversation Sentiment")
            st.bar_chart(st.session_state.sentiment_stats)

        st.markdown("---")
        st.markdown("Built with Gemini API")

    # Main Title
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

    # Display existing messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "user" and "sentiment" in message and message["sentiment"]:
                sentiment = message["sentiment"].get("sentiment", "neutral")
                emotion = message["sentiment"].get("emotion", "")

                sentiment_html = f"""
                <div>
                    {message["content"]}
                    <span class="sentiment-badge" style="background-color: {get_sentiment_color(sentiment)}">
                        {sentiment}{f" • {emotion}" if emotion else ""}
                    </span>
                </div>
                """
                st.markdown(sentiment_html, unsafe_allow_html=True)

                with st.expander("Sentiment Details"):
                    st.json(message["sentiment"])
            else:
                st.write(message["content"])

    # Input box
    if prompt := st.chat_input("Type your message here..."):
        # Analyze user input
        with st.spinner("Analyzing sentiment..."):
            sentiment_result = st.session_state.sentiment_analyzer.analyze_sentiment(prompt)
            sentiment = sentiment_result.get('sentiment', 'neutral')
            st.session_state.sentiment_stats[sentiment] += 1

        # Add user message to history
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "sentiment": sentiment_result
        })

        # Display user's message
        with st.chat_message("user"):
            sentiment = sentiment_result.get("sentiment", "neutral")
            emotion = sentiment_result.get("emotion", "")

            sentiment_html = f"""
            <div>
                {prompt}
                <span class="sentiment-badge" style="background-color: {get_sentiment_color(sentiment)}">
                    {sentiment}{f" • {emotion}" if emotion else ""}
                </span>
            </div>
            """
            st.markdown(sentiment_html, unsafe_allow_html=True)

            with st.expander("Sentiment Details"):
                st.json(sentiment_result)

        # Save user message to conversation manager
        st.session_state.conversation_manager.add_message(prompt, "user", sentiment_result)

        # Generate assistant response
        conversation_history = st.session_state.conversation_manager.get_conversation_history()

        with st.spinner("Thinking..."):
            response = st.session_state.response_generator.generate_response(
                prompt,
                sentiment_result,
                conversation_history
            )

        # Add assistant message
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        st.session_state.conversation_manager.add_message(response, "assistant", None)

        # Display assistant's message
        with st.chat_message("assistant"):
            st.write(response)

        # Save updated conversation
        st.session_state.conversation_manager.save_conversation()

if __name__ == "__main__":
    main()
