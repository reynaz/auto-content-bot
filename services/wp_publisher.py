"""
WordPress Publisher Service - REST API Integration
Handles creating posts, drafts, and managing content on WordPress sites.
"""
import time
import random
import requests
from requests.auth import HTTPBasicAuth
from config import Config


class WordPressPublisher:
    """
    WordPress REST API integration for content publishing.
    Supports draft creation, publishing, and content management.
    """
    
    def __init__(self):
        self.base_url = Config.WP_URL
        self.auth = None
        self.use_real_api = False
        
        if Config.is_wordpress_configured() and not Config.DEMO_MODE:
            self.auth = HTTPBasicAuth(Config.WP_USER, Config.WP_APP_PASSWORD)
            self._verify_connection()
        else:
            print("📝 [WORDPRESS] Running in DEMO mode.")

    def _verify_connection(self):
        """Verify WordPress API connection."""
        try:
            response = requests.get(
                f"{self.base_url}/users/me",
                auth=self.auth,
                timeout=10
            )
            if response.status_code == 200:
                user = response.json()
                print(f"📝 [WORDPRESS] Connected as: {user.get('name', 'User')}")
                self.use_real_api = True
            else:
                print(f"⚠️ [WORDPRESS] Connection failed (Status: {response.status_code})")
        except Exception as e:
            print(f"⚠️ [WORDPRESS] Connection error: {e}")

    def create_draft(self, title: str, content: str, excerpt: str = "") -> str:
        """
        Create a draft post on WordPress.
        Returns the preview link.
        """
        print(f"\n--- 📡 CONNECTING TO WORDPRESS ---")
        print(f"Action: Create Draft Post")
        print(f"Post Title: {title}")
        
        if self.use_real_api:
            return self._create_real_post(title, content, excerpt, status="draft")
        else:
            return self._create_mock_post(title, "draft")

    def publish_post(self, title: str, content: str, excerpt: str = "") -> str:
        """
        Publish a post directly to WordPress.
        Returns the public link.
        """
        print(f"\n--- 📡 PUBLISHING TO WORDPRESS ---")
        print(f"Post Title: {title}")
        
        if self.use_real_api:
            return self._create_real_post(title, content, excerpt, status="publish")
        else:
            return self._create_mock_post(title, "publish")

    def _create_real_post(self, title: str, content: str, excerpt: str, status: str) -> str:
        """Create a real post via WordPress REST API."""
        try:
            payload = {
                "title": title,
                "content": content,
                "excerpt": excerpt or content[:150] + "...",
                "status": status,
                "format": "standard"
            }
            
            response = requests.post(
                f"{self.base_url}/posts",
                auth=self.auth,
                json=payload,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                post = response.json()
                link = post.get('link', '')
                post_id = post.get('id', '')
                
                if status == "draft":
                    preview_link = f"{link}?preview=true"
                    print(f"✅ [WORDPRESS] Draft created (ID: {post_id})")
                    print(f"🔗 Preview: {preview_link}")
                    return preview_link
                else:
                    print(f"✅ [WORDPRESS] Post published (ID: {post_id})")
                    print(f"🔗 Live URL: {link}")
                    return link
            else:
                print(f"❌ [WORDPRESS] Failed: {response.status_code} - {response.text}")
                return self._create_mock_post(title, status)
                
        except Exception as e:
            print(f"❌ [WORDPRESS] Error: {e}")
            return self._create_mock_post(title, status)

    def _create_mock_post(self, title: str, status: str) -> str:
        """Create a mock post for demo purposes."""
        time.sleep(1.5)  # Simulate network latency
        
        mock_id = random.randint(1000, 9999)
        base_domain = self.base_url.replace('/wp-json/wp/v2', '') if self.base_url else 'https://demo.wordpress.com'
        
        if status == "draft":
            mock_link = f"{base_domain}/?p={mock_id}&preview=true"
            print(f"✅ [WORDPRESS] Draft created (ID: {mock_id}) - DEMO MODE")
        else:
            mock_link = f"{base_domain}/post-{mock_id}/"
            print(f"✅ [WORDPRESS] Post published (ID: {mock_id}) - DEMO MODE")
        
        print(f"🔗 Link: {mock_link}")
        print("-----------------------------------\n")
        
        return mock_link

    def update_post(self, post_id: int, title: str = None, content: str = None, status: str = None) -> bool:
        """Update an existing post."""
        print(f"📝 [WORDPRESS] Updating post {post_id}...")
        
        if self.use_real_api:
            try:
                payload = {}
                if title:
                    payload['title'] = title
                if content:
                    payload['content'] = content
                if status:
                    payload['status'] = status
                
                response = requests.patch(
                    f"{self.base_url}/posts/{post_id}",
                    auth=self.auth,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    print(f"✅ [WORDPRESS] Post {post_id} updated successfully.")
                    return True
                else:
                    print(f"❌ [WORDPRESS] Update failed: {response.status_code}")
                    return False
            except Exception as e:
                print(f"❌ [WORDPRESS] Error: {e}")
                return False
        else:
            time.sleep(0.5)
            print(f"✅ [WORDPRESS] Post {post_id} updated (DEMO MODE)")
            return True

    def get_posts(self, status: str = "any", per_page: int = 10) -> list:
        """Get list of posts from WordPress."""
        if self.use_real_api:
            try:
                params = {"per_page": per_page}
                if status != "any":
                    params["status"] = status
                
                response = requests.get(
                    f"{self.base_url}/posts",
                    auth=self.auth,
                    params=params,
                    timeout=30
                )
                
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                print(f"⚠️ [WORDPRESS] Error fetching posts: {e}")
        
        # Mock posts
        return [
            {"id": 1001, "title": {"rendered": "Sample Post 1"}, "status": "publish"},
            {"id": 1002, "title": {"rendered": "Draft Post"}, "status": "draft"}
        ]

    def upload_media(self, file_path: str, title: str = "") -> dict:
        """
        Upload media (images) to WordPress.
        Returns media object with ID and URL.
        """
        print(f"📷 [WORDPRESS] Uploading media: {file_path}")
        
        if self.use_real_api:
            try:
                with open(file_path, 'rb') as f:
                    filename = file_path.split('/')[-1]
                    headers = {
                        'Content-Disposition': f'attachment; filename="{filename}"'
                    }
                    
                    response = requests.post(
                        f"{self.base_url}/media",
                        auth=self.auth,
                        headers=headers,
                        data=f,
                        timeout=60
                    )
                    
                    if response.status_code in [200, 201]:
                        media = response.json()
                        print(f"✅ [WORDPRESS] Media uploaded (ID: {media['id']})")
                        return {
                            "id": media['id'],
                            "url": media['source_url']
                        }
            except Exception as e:
                print(f"❌ [WORDPRESS] Media upload failed: {e}")
        
        # Mock response
        return {
            "id": random.randint(100, 999),
            "url": f"https://demo.wordpress.com/wp-content/uploads/sample.jpg"
        }
