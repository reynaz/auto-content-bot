# services/gmail_service.py

from services.gmail_api import (
    fetch_threads,
    get_thread_as_text
)


class GmailService:
    def __init__(self):
        pass

    def fetch_latest_email(self):
        """
        Fetches the latest Gmail thread and formats it
        into a pipeline-friendly structure.
        """

        threads = fetch_threads(max_results=1)

        if not threads:
            return None

        thread_id = threads[0]["id"]
        body_text = get_thread_as_text(thread_id)

        return {
            "id": thread_id,
            "sender": "unknown@gmail.com",   # ileri aşamada header'dan çekilir
            "subject": "Automated Gmail Task",
            "body": body_text,
            "thread_id": thread_id
        }

    def send_report(self, to_email, subject, body):
        """
        Placeholder for sending report emails.
        Gmail API send can be added later.
        """
        print("\n--- REPORT EMAIL (MOCK) ---")
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print(body)
        print("--- END REPORT ---\n")

