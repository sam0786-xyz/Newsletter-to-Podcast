# gmail_reader.py
import os.path
import base64
from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_newsletter_content():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    # Find newsletters. A simple way is to search for 'unsubscribe' in the body
    # from specific senders you know.
    # Example query: 'from:(newsletter@example.com) "unsubscribe"'
    results = service.users().messages().list(
        userId='me',
        q='from:(the-ai-report@mail.beehiiv.com) is:unread', # Be specific to avoid processing all mail
        maxResults=1
    ).execute()
    
    messages = results.get('messages', [])
    if not messages:
        print('No new newsletters found.')
        return None

    msg_id = messages[0]['id']
    message = service.users().messages().get(userId='me', id=msg_id).execute()
    
    payload = message['payload']
    if 'parts' in payload:
        part = next(p for p in payload['parts'] if p['mimeType'] == 'text/html')
        data = part['body']['data']
    else:
        data = payload['body']['data']

    html_content = base64.urlsafe_b64decode(data).decode('utf-8')
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Mark the email as read so we don't process it again
    service.users().messages().modify(userId='me', id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()

    return soup.get_text(separator='\n', strip=True)

if __name__ == '__main__':
    content = get_newsletter_content()
    if content:
        print("Successfully extracted newsletter content.")
        # We would save this content to a file or pass it to the next step
        with open("newsletter_content.txt", "w") as f:
            f.write(content)