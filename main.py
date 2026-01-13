"""
Auto-Content-Bot: AI-Powered Content Automation System
Main entry point for the CLI pipeline.
"""

from services.gmail_service import GmailService
from services.ai_engine import AIEngine
from services.wp_publisher import WordPressPublisher
from services.social_manager import SocialMediaManager
from config import Config


def print_banner():
    """Display startup banner with configuration status."""
    print("\n" + "=" * 60)
    print("AUTO-CONTENT-BOT - AI Content Automation System")
    print("=" * 60)

    status = Config.get_status()
    mode = "DEMO MODE" if status["demo_mode"] else "PRODUCTION MODE"
    print(f"Running in: {mode}\n")

    print("Integration Status:")
    print(f"  ├── OpenAI:    {'Connected' if status['openai'] else 'Mock Mode'}")
    print(f"  ├── WordPress: {'Connected' if status['wordpress'] else 'Mock Mode'}")
    print(f"  ├── Gmail:     {'Connected' if status['gmail'] else 'Mock Mode'}")
    print(f"  ├── LinkedIn:  {'Connected' if status['linkedin'] else 'Mock Mode'}")
    print(f"  └── Twitter:   {'Connected' if status['twitter'] else 'Mock Mode'}")
    print("=" * 60 + "\n")


def run_pipeline(custom_email: dict | None = None):
    """
    Main execution function for the Auto-Content-Bot.
    Orchestrates the flow: Email -> AI -> CMS -> Social Media -> Report.
    """

    print_banner()
    print("Starting Content Pipeline...\n")

    # 1. INITIALIZATION
    gmail_service = GmailService()
    ai_service = AIEngine()
    wp_service = WordPressPublisher()
    social_service = SocialMediaManager()

    # 2. INPUT (Email)
    email_data = custom_email or gmail_service.fetch_latest_email()

    if not email_data:
        print("No new tasks found. Exiting.")
        return {"status": "no_tasks"}

    print(f"\nProcessing email: {email_data['subject']}")
    print(f"From: {email_data['sender']}")
    print("-" * 50)

    # 3. PROCESSING (AI – mock or real)
    content_package = ai_service.generate_content_package(email_data)

    results = {
        "status": "success",
        "email": email_data,
        "generated_content": {},
        "published": {},
    }

    # 4A. WordPress Publishing
    if "blog_post" in content_package:
        blog = content_package["blog_post"]
        draft_link = wp_service.create_draft(blog["title"], blog["content"])
        results["published"]["wordpress"] = {
            "title": blog["title"],
            "link": draft_link,
        }
        results["generated_content"]["blog_post"] = blog

    # 4B. Social Media
    if "social_post" in content_package:
        results["published"]["linkedin"] = social_service.post_to_linkedin(
            content_package["social_post"]
        )

    if "twitter_post" in content_package:
        results["published"]["twitter"] = social_service.post_to_twitter(
            content_package["twitter_post"]
        )

    # 5. REPORT
    report_message = f"""
TASK COMPLETED SUCCESSFULLY

Generated Content:
{chr(10).join(f" - {k}" for k in content_package.keys())}

WordPress Draft:
{results["published"].get("wordpress", {}).get("link", "N/A")}
"""

    gmail_service.send_report(
        to_email=email_data["sender"],
        subject="Content Generation Complete",
        body=report_message,
    )

    print("\nPipeline finished successfully.")
    return results


def demo_mode():
    """Run pipeline with sample data (no Gmail API required)."""

    sample_email = {
        "id": "demo_001",
        "sender": "demo@example.com",
        "subject": "TASK: Create Marketing Content",
        "body": "Please generate marketing content for our new product.",
        "thread_id": "demo_thread_001",
    }

    return run_pipeline(custom_email=sample_email)


if __name__ == "__main__":
    import sys

    if "--demo" in sys.argv:
        demo_mode()
    else:
        run_pipeline()

