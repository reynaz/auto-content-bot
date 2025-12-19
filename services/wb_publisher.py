import time
import random

class WordPressPublisher:
    """
    Handles interactions with the WordPress REST API.
    Currently running in MOCK mode for demonstration/testing purposes.
    """
    
    def __init__(self):
        # In production, credentials would be loaded from .env here
        self.base_url = "https://anotherway0.wordpress.com/wp-json/wp/v2/posts"

    def create_draft(self, title, content):
        """
        Simulates creating a draft post on the WordPress site.
        """
        print(f"\n--- 📡 CONNECTING TO WORDPRESS ---")
        print(f"Target Endpoint: {self.base_url}")
        print(f"Action: Create Draft Post")
        print(f"Post Title: {title}")
        
        # Simulate network latency
        time.sleep(1.5) 
        
        # Mocking the API response
        mock_id = random.randint(1000, 9999)
        mock_link = f"https://anotherway0.wordpress.com/?p={mock_id}&preview=true"
        
        print(f"✅ [WORDPRESS] Draft created successfully. (ID: {mock_id})")
        print(f"🔗 Preview Link: {mock_link}")
        print("-----------------------------------\n")
        
        return mock_link
