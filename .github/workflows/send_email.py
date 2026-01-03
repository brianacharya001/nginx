from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

def test_api_endpoint(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        print("API is working")
    except requests.exceptions.RequestException as errh:
        print("Http Error:", errh)
        send_email(
            "API Endpoint Error!!!",
            f"There was an error accessing the API endpoint: {api_url} "+ str(errh),
        )

def send_email(
    subject="API is down",
    body="API is down",
):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    USERNAME = os.getenv("USER_EMAIL")
    PASSWORD = os.getenv("USER_PASSWORD")

    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = USERNAME
    message["To"] = USERNAME
    message.attach(MIMEText(body, "plain"))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(USERNAME, PASSWORD)
            server.sendmail(USERNAME, USERNAME, message.as_string())
            print("Email sent successfully")
    except Exception as e:
        print("Error sending email: ", e)

if __name__ == "__main__":
    api_url = "https://api.propertyproai.com/healthy"
    test_api_endpoint(api_url)
