import os
import json
from datetime import datetime

class ConversationManager:
    def __init__(self, storage_dir="data/conversation_history"):
        """
        Initialize the conversation manager.
        
        Args:
            storage_dir (str): Directory to store conversation history
        """
        self.storage_dir = storage_dir
        self.ensure_storage_dir_exists()
        self.current_conversation = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def ensure_storage_dir_exists(self):
        """Ensure the storage directory exists."""
        os.makedirs(self.storage_dir, exist_ok=True)
        
    def add_message(self, message, role, sentiment_result=None):
        """
        Add a message to the current conversation.
        
        Args:
            message (str): The message text
            role (str): Either 'user' or 'assistant'
            sentiment_result (dict, optional): Sentiment analysis result for user messages
        """
        message_data = {
            "text": message,
            "role": role,
            "timestamp": datetime.now().isoformat()
        }
        
        if role == "user" and sentiment_result:
            message_data["sentiment"] = sentiment_result
            
        self.current_conversation.append(message_data)
        
    def get_conversation_history(self, max_messages=20):
        """
        Get the conversation history as a list of message texts.
        
        Args:
            max_messages (int): Maximum number of messages to return
            
        Returns:
            list: List of message texts alternating between user and assistant
        """
        messages = []
        for message in self.current_conversation[-max_messages:]:
            messages.append(message["text"])
            
        return messages
        
    def get_formatted_history(self):
        """
        Get the conversation history formatted for display.
        
        Returns:
            list: List of message dictionaries with role and text
        """
        return [{"role": msg["role"], "content": msg["text"]} for msg in self.current_conversation]
        
    def save_conversation(self):
        """Save the current conversation to a file."""
        if not self.current_conversation:
            return
            
        filename = f"{self.session_id}.json"
        filepath = os.path.join(self.storage_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(self.current_conversation, f, indent=2)
            
        return filepath
        
    def load_conversation(self, session_id):
        """
        Load a conversation from a file.
        
        Args:
            session_id (str): The session ID to load
            
        Returns:
            bool: True if successful, False otherwise
        """
        filename = f"{session_id}.json"
        filepath = os.path.join(self.storage_dir, filename)
        
        if not os.path.exists(filepath):
            return False
            
        try:
            with open(filepath, 'r') as f:
                self.current_conversation = json.load(f)
                self.session_id = session_id
            return True
        except Exception as e:
            print(f"Error loading conversation: {e}")
            return False
            
    def clear_conversation(self):
        """Clear the current conversation."""
        self.current_conversation = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
