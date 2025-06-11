# gmail_reader.py
import os.path
import base64
from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
NEWSLETTER_LABEL_ID = 'Label_2' 

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

    # Fetch unread messages with the specified label
    results = service.users().messages().list(
        userId='me',
        labelIds=[NEWSLETTER_LABEL_ID],
        q='is:unread'
    ).execute()
    
    messages = results.get('messages', [])
    if not messages:
        print('No new newsletters found under the specified label.')
        return None

    print(f"Found {len(messages)} new newsletters. Combining their content...")
    
    all_content = []
    message_ids_to_mark_read = []

    for msg_summary in messages:
        msg_id = msg_summary['id']
        message = service.users().messages().get(userId='me', id=msg_id).execute()
        
        # Extract subject for context
        subject = "No Subject"
        for header in message['payload']['headers']:
            if header['name'].lower() == 'subject':
                subject = header['value']
                break

        # Get message body
        payload = message['payload']
        data = ''
        if "parts" in payload:
            try:
                part = next(p for p in payload['parts'] if p['mimeType'] == 'text/html')
                data = part['body']['data']
            except StopIteration:
                try:
                    part = next(p for p in payload['parts'] if p['mimeType'] == 'text/plain')
                    data = part['body']['data']
                except StopIteration:
                    continue # Skip emails with no readable body
        else:
            data = payload['body']['data']

        decoded_data = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        
        if 'html' in locals().get('part', {}).get('mimeType', ''):
            soup = BeautifulSoup(decoded_data, 'html.parser')
            text_content = soup.get_text(separator='\n', strip=True)
        else:
            text_content = decoded_data

        # Prepend subject for better context for the LLM
        all_content.append(f"--- NEWSLETTER: {subject} ---\n\n{text_content}\n\n")
        message_ids_to_mark_read.append(msg_id)

    # Batch-modify messages to mark them as read
    if message_ids_to_mark_read:
        service.users().messages().batchModify(
            userId='me',
            body={
                'ids': message_ids_to_mark_read,
                'removeLabelIds': ['UNREAD']
            }
        ).execute()
        print(f"Marked {len(message_ids_to_mark_read)} newsletters as read.")

    return "\n".join(all_content)