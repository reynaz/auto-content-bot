import base64
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API scope
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def authenticate_gmail():
    """
    Handles OAuth authentication and returns a Gmail service object.
    """
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)
    return service

def fetch_threads(max_results=5, query=None):
    """
    Fetches Gmail threads.
    """
    service = authenticate_gmail()

    response = service.users().threads().list(
        userId="me",
        maxResults=max_results,
        q=query
    ).execute()

    threads = response.get("threads", [])
    return threads

def get_thread_messages(thread_id):
    """
    Returns all messages in a given thread.
    """
    service = authenticate_gmail()

    thread = service.users().threads().get(
        userId="me",
        id=thread_id,
        format="full"
    ).execute()

    return thread.get("messages", [])

def extract_message_body(message):
    """
    Extracts plain text body from a Gmail message.
    """
    payload = message.get("payload", {})
    parts = payload.get("parts")

    if not parts:
        data = payload.get("body", {}).get("data")
        if data:
            return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
        return ""

    for part in parts:
        mime_type = part.get("mimeType")
        body = part.get("body", {})
        data = body.get("data")

        if mime_type == "text/plain" and data:
            return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

    return ""

def get_thread_as_text(thread_id):
    """
    Combines all messages in a thread into a single text.
    """
    messages = get_thread_messages(thread_id)
    full_text = []

    for msg in messages:
        body = extract_message_body(msg)
        if body:
            full_text.append(body.strip())

    return "\n\n---\n\n".join(full_text)

