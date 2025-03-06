import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Your SEMrush API key
SEMRUSH_API_KEY = os.getenv("SEMRUSH_API_KEY")
DOMAIN = "yourdomain.com"  # Replace with your domain
DATABASE_FILE = "rankings.json"

# SEMrush API endpoint
API_URL = "https://api.semrush.com/"

# Telegram settings (optional)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_rankings():
    """Fetch rankings from SEMrush API."""
    params = {
        "type": "domain_ranks",
        "key": SEMRUSH_API_KEY,
        "display_limit": "10",  # Adjust as needed
        "export_columns": "Db,Po,Url,Keyword",
        "domain": DOMAIN,
        "database": "us"  # Change to your target country database (e.g., 'uk', 'de', etc.)
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.text.split("\n")  # Split into lines
    else:
        print("Error fetching rankings:", response.text)
        return None

def load_previous_rankings():
    """Load previous rankings from file."""
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_current_rankings(rankings):
    """Save current rankings to file."""
    with open(DATABASE_FILE, "w") as f:
        json.dump(rankings, f, indent=4)

def send_telegram_alert(message):
    """Send an alert via Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.get(url, params=params)

def compare_rankings():
    """Compare rankings and detect significant changes."""
    previous = load_previous_rankings()
    current = get_rankings()
    if not current:
        return
    
    alert_messages = []
    new_rankings = {}
    
    for line in current[1:]:  # Skip the header
        if not line.strip():
            continue
        parts = line.split(";")  # SEMrush data is CSV-like (semicolon-separated)
        if len(parts) < 4:
            continue
        
        keyword = parts[3]
        position = int(parts[1])
        new_rankings[keyword] = position
        
        previous_position = previous.get(keyword, None)
        
        if previous_position:
            change = position - previous_position
            if abs(change) >= 5:  # Alert if ranking changes by 5 or more positions
                alert_messages.append(f"🔻 Keyword: {keyword} dropped from {previous_position} to {position}")
                
    save_current_rankings(new_rankings)
    
    if alert_messages:
        alert_text = "\n".join(alert_messages)
        print("Sending alerts:", alert_text)
        send_telegram_alert(alert_text)
    else:
        print("No major ranking changes detected.")

if __name__ == "__main__":
    compare_rankings()
