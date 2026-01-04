import os
import ssl
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def test_api_endpoint(api_url):
    try:
        # Added a 10s timeout to prevent the script from hanging indefinitely
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        print(f"API is working: {api_url}")
    except requests.exceptions.RequestException as err:
        print(f"HTTP Error: {err}")
        # Send more descriptive alerts
        send_email(
            subject="CRITICAL: API Endpoint Error",
            body=f"Target URL: {api_url}\nError Details: {str(err)}"
        )

def send_email(subject="API is down", body="API is down"):
    smtp_server = "smtp.gmail.com"
    port = 465  # SSL port
    
    # Retrieve credentials securely
    USERNAME = os.getenv("USER_EMAIL")
    PASSWORD = os.getenv("USER_PASSWORD") # MUST be a 16-character App Password

    if not USERNAME or not PASSWORD:
        print("Error: Missing credentials in environment variables.")
        return

    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = USERNAME
    message["To"] = USERNAME
    message.attach(MIMEText(body, "plain"))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(USERNAME, PASSWORD)
            server.send_message(message)
            print("Alert email sent successfully.")
    except smtplib.SMTPAuthenticationError:
        print("Authentication failed: Ensure you are using a Gmail 'App Password'.")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    # Use your actual health check endpoint
    TARGET_URL = "https://api.propertyproai.com/healthy"
    test_api_endpoint(TARGET_URL)
