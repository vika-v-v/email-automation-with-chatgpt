from import_notion_items import get_notion_items, extract_information_from_notion_item, update_notion_page
from chatgpt_email import generate_email
from email_sender import send_email

def print_notion_items(items):
    for item in items:
        information = extract_information_from_notion_item(item)
        if(information['antwort'] == 'Nicht begonnen'):
            print(extract_information_from_notion_item(item))
            print('_' * 80)  # Separator for readability

            if(information['automate'] == 'Yes (email)'):
                email_body = 'bla' #generate_email(information['startup_name'], information['startup_notes'])
                print(email_body)

                #send_email(information['email'], "Запрошення представити Ваш стартап в Німеччині", email_body)
                update_notion_page(information['page_id'], email_body)





# Assuming the function get_updated_items() is already defined and returns the items
items = get_notion_items()
print_notion_items(items)
