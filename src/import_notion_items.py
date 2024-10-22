import requests
import os
from dotenv import load_dotenv

load_dotenv()

NOTION_API_TOKEN = os.getenv('NOTION_API_TOKEN')
DATABASE_ID = os.getenv('DATABASE_ID')

headers = {
        "Authorization": f"Bearer {NOTION_API_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

def get_notion_items():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("results", [])
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

def extract_information_from_notion_item(item):
    # Extract the relevant fields
    page_id = item.get('id', 'N/A')
    properties = item.get('properties', {})

    # Startup name (from 'Name' field)
    startup_name = properties.get('Name', {}).get('title', [])
    startup_name = startup_name[0]['plain_text'] if startup_name else 'N/A'

    # Startup notes (from 'Notizen' field)
    notes = properties.get('Notizen', {}).get('rich_text', [])
    startup_notes = notes[0]['plain_text'] if notes else 'N/A'

    # Email (from 'Email' field)
    email = properties.get('Email', {}).get('email', 'N/A')

    # Antwort (from 'Antwort' field)
    antwort_field = properties.get('Antwort', {}).get('select', None)
    antwort = antwort_field['name'] if antwort_field else 'N/A'

    # Automate (from 'Automate' field)
    automate_field = properties.get('Automate', {}).get('select', None)
    automate = automate_field['name'] if automate_field else 'N/A'

    # Telegram (from 'Telegram' field)
    telegram = properties.get('Telegram', {}).get('rich_text', [])
    telegram_contact = telegram[0]['plain_text'] if telegram else 'N/A'

    return {
        'page_id': page_id,
        'startup_name': startup_name,
        'startup_notes': startup_notes,
        'email': email,
        'antwort': antwort,
        'automate': automate,
        'telegram_contact': telegram_contact
    }


def update_notion_page(page_id, email_body):
    update_url = f"https://api.notion.com/v1/pages/{page_id}"
    append_url = f"https://api.notion.com/v1/blocks/{page_id}/children"

    # Data to append a paragraph block with the provided text
    append_data = {
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": email_body
                            }
                        }
                    ]
                }
            }
        ]
    }

    # Send PATCH request to append the email body as a text block
    append_response = requests.patch(append_url, headers=headers, json=append_data)
    
    
    if append_response.status_code == 200:
        print(f"Email body appended successfully to page {page_id}.")
    else:
        print(f"Failed to append email body to page {page_id}. Status code: {append_response.status_code}")
        print(append_response.json())

    # Data to update the 'Antwort' property
    update_data = {
        "properties": {
            "Antwort": {
                "select": {"name": "Warte auf Rückmeldung"}
            }
        }
    }

    # Send PATCH request to update the 'Antwort' property
    update_response = requests.patch(update_url, headers=headers, json=update_data)
    
    if update_response.status_code == 200:
        print(f"'Antwort' property updated successfully for page {page_id}.")
    else:
        print(f"Failed to update 'Antwort' property for page {page_id}. Status code: {update_response.status_code}")
        print(update_response.json())