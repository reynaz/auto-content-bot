import time

class GmailListener:
    """
    Simulates the Gmail API interactions using IMAP logic equivalent.
    In a production environment, this would use `google-api-python-client`.
    """

    def check_new_emails(self):
        """
        Simulates checking the inbox for specific task-related emails.
        Returns a dictionary representing a structured email object.
        """
        print("📩 [GMAIL] Checking inbox for new task requests...")
        time.sleep(1)  # Simulate network delay

        # Mock Email Data
        # This simulates a request from a manager to create content for a product.
        mock_email = {
            "id": "msg_98765",
            "sender": "marketing_lead@giftservice.com",
            "subject": "TASK: Create Content for Eco-Friendly Notebook",
            "body": "We have a new product: 'Recycled Paper Notebook'. Please generate a blog post about the importance of sustainable stationery and a LinkedIn post. Price: $12."
        }
        
        print(f"📩 [GMAIL] New email found from: {mock_email['sender']}")
        return mock_email

    def send_report(self, to_email, subject, body):
        """
        Simulates sending a reporting email via SMTP/Gmail API.
        """
        print("\n--- 📤 SENDING EMAIL REPORT ---")
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print(f"Body: {body}")
        print("✅ [GMAIL] Email sent successfully.")
        print("-------------------------------")
