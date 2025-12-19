"""
Auto-Content-Bot Dashboard
A simple web interface to trigger and monitor content automation workflows.
"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import threading
import json
from datetime import datetime

from main import run_pipeline, demo_mode
from config import Config
from services.gmail_listener import GmailListener
from services.ai_engine import AIEngine
from services.wp_publisher import WordPressPublisher
from services.social_manager import SocialMediaManager

app = Flask(__name__)
CORS(app)

# Store execution logs
execution_logs = []
current_task = None


def add_log(message: str, level: str = "info"):
    """Add a log entry with timestamp."""
    log_entry = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "level": level,
        "message": message
    }
    execution_logs.append(log_entry)
    # Keep only last 100 logs
    if len(execution_logs) > 100:
        execution_logs.pop(0)


@app.route('/')
def dashboard():
    """Render the main dashboard page."""
    return render_template('dashboard.html')


@app.route('/api/status')
def get_status():
    """Get current system status and configuration."""
    status = Config.get_status()
    return jsonify({
        "status": "online",
        "demo_mode": status["demo_mode"],
        "integrations": {
            "openai": {"connected": status["openai"], "name": "OpenAI GPT-4"},
            "wordpress": {"connected": status["wordpress"], "name": "WordPress"},
            "gmail": {"connected": status["smtp"], "name": "Gmail/SMTP"},
            "linkedin": {"connected": status["linkedin"], "name": "LinkedIn"},
            "twitter": {"connected": status["twitter"], "name": "Twitter/X"}
        },
        "current_task": current_task,
        "logs": execution_logs[-20:]  # Last 20 logs
    })


@app.route('/api/run', methods=['POST'])
def run_automation():
    """Trigger the content automation pipeline."""
    global current_task
    
    data = request.get_json() or {}
    use_demo = data.get('demo', True)
    custom_email = data.get('email', None)
    
    if current_task and current_task.get('status') == 'running':
        return jsonify({"error": "A task is already running"}), 400
    
    current_task = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "status": "running",
        "started_at": datetime.now().isoformat(),
        "type": "demo" if use_demo else "production"
    }
    
    add_log("🚀 Starting content automation pipeline...", "info")
    
    def execute_pipeline():
        global current_task
        try:
            if custom_email:
                add_log(f"📧 Processing custom email: {custom_email.get('subject', 'N/A')}", "info")
                results = run_pipeline(custom_email=custom_email)
            elif use_demo:
                add_log("🎮 Running in demo mode with sample data", "info")
                results = demo_mode()
            else:
                add_log("📩 Checking for new emails...", "info")
                results = run_pipeline()
            
            current_task["status"] = "completed"
            current_task["results"] = results
            current_task["completed_at"] = datetime.now().isoformat()
            add_log("✅ Pipeline completed successfully!", "success")
            
        except Exception as e:
            current_task["status"] = "failed"
            current_task["error"] = str(e)
            add_log(f"❌ Pipeline failed: {str(e)}", "error")
    
    # Run in background thread
    thread = threading.Thread(target=execute_pipeline)
    thread.start()
    
    return jsonify({
        "message": "Pipeline started",
        "task_id": current_task["id"]
    })


@app.route('/api/preview', methods=['POST'])
def preview_content():
    """Preview AI-generated content without publishing."""
    data = request.get_json() or {}
    
    email_data = {
        "id": "preview",
        "sender": "preview@dashboard.local",
        "subject": data.get('subject', 'Preview Request'),
        "body": data.get('body', 'Generate sample content'),
        "thread_id": "preview_thread"
    }
    
    add_log(f"👁️ Generating preview for: {email_data['subject']}", "info")
    
    try:
        ai_service = AIEngine()
        content = ai_service.generate_content_package(email_data)
        add_log("✅ Preview generated successfully", "success")
        
        return jsonify({
            "status": "success",
            "content": content
        })
    except Exception as e:
        add_log(f"❌ Preview failed: {str(e)}", "error")
        return jsonify({"error": str(e)}), 500


@app.route('/api/generate', methods=['POST'])
def generate_single():
    """Generate a single content type."""
    data = request.get_json() or {}
    content_type = data.get('type', 'blog_post')
    request_text = data.get('request', '')
    
    if not request_text:
        return jsonify({"error": "Request text is required"}), 400
    
    add_log(f"📝 Generating {content_type}...", "info")
    
    try:
        ai_service = AIEngine()
        
        if content_type == 'blog_post':
            result = ai_service.generate_blog_post(request_text)
        elif content_type == 'case_study':
            result = ai_service.generate_case_study(request_text)
        elif content_type == 'social_post':
            platform = data.get('platform', 'LinkedIn')
            result = ai_service.generate_social_post(request_text, platform)
        elif content_type == 'product_description':
            result = ai_service.generate_product_description(request_text)
        else:
            return jsonify({"error": f"Unknown content type: {content_type}"}), 400
        
        add_log(f"✅ {content_type} generated", "success")
        return jsonify({"status": "success", "content": result})
        
    except Exception as e:
        add_log(f"❌ Generation failed: {str(e)}", "error")
        return jsonify({"error": str(e)}), 500


@app.route('/api/publish', methods=['POST'])
def publish_content():
    """Publish content to a specific platform."""
    data = request.get_json() or {}
    platform = data.get('platform', '')
    content = data.get('content', {})
    
    add_log(f"📤 Publishing to {platform}...", "info")
    
    try:
        if platform == 'wordpress':
            wp_service = WordPressPublisher()
            title = content.get('title', 'Untitled')
            body = content.get('content', '')
            link = wp_service.create_draft(title, body)
            result = {"platform": "wordpress", "link": link}
            
        elif platform == 'linkedin':
            social_service = SocialMediaManager()
            text = content.get('text', '')
            result = social_service.post_to_linkedin(text)
            
        elif platform == 'twitter':
            social_service = SocialMediaManager()
            text = content.get('text', '')
            result = social_service.post_to_twitter(text)
            
        else:
            return jsonify({"error": f"Unknown platform: {platform}"}), 400
        
        add_log(f"✅ Published to {platform}", "success")
        return jsonify({"status": "success", "result": result})
        
    except Exception as e:
        add_log(f"❌ Publishing failed: {str(e)}", "error")
        return jsonify({"error": str(e)}), 500


@app.route('/api/logs')
def get_logs():
    """Get execution logs."""
    return jsonify({"logs": execution_logs})


@app.route('/api/clear-logs', methods=['POST'])
def clear_logs():
    """Clear execution logs."""
    global execution_logs
    execution_logs = []
    add_log("🧹 Logs cleared", "info")
    return jsonify({"status": "cleared"})


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌐 AUTO-CONTENT-BOT DASHBOARD")
    print("="*60)
    print("Starting web server...")
    print("Open http://localhost:5000 in your browser")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000)
