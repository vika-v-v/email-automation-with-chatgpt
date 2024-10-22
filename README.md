# About
This repository contains the Python script used to automate the sending of emails. It takes the notion database and sends emails to all contacts marked as not contacted. The email is edited with ChatGPT-4 before sending to better suit the recipient. After the email is sent the status in the notion database is updated and the email copy is saved as a text in the database item.

# Database structure
In my case, I am emailing the startups to propose the collab, so the script is using this strcuture, but you can change it if needed.
The Notion database should contain such columns:
- "Name" (of the recepient)
- "Notitzen" (notes of the recepient to help ChatGPT form the email)
- "Antwort" (whether or not got the responce. The email will only be sent to the recepients with "Nicht begonnen" (not started) value and it will be changed to "Warte auf Rückmeldung" (expecting answer) as soon as the email is sent)
- "Automate" (whether or not to send email using this script, the value should be "Yes (email)" to proceed)
- "Email" (the email of the recepient)
- Any other columns you need will not affect this script

# Gestting started:
## First time:
- call in Terminal <code>python -m venv venv</code> - this will create a new virtual environment to add dependencies.
- call <code>venv\Scripts\activate</code> - activate the environment.
- call <code>pip install -r requirements.txt</code> - install the dependencies.
- create a file called ".env" and put there such variables:
<pre>
NOTION_API_TOKEN="ntn_612..." # create a new integration and use the secret (https://www.notion.so/profile/integrations), do not forget to go to your database page and click ●●● -> Connections -> Connect to -> Select your integration
DATABASE_ID="your_database_id" # the value between www.notion.so/ and ?v in the database URL
OPENAI_API_KEY="sk-proj-2sr..." # get it here: https://platform.openai.com/api-keys
SENDER_EMAIL="email@any.com"
EMAIL_PASSWORD='email-password'
PATH_TO_CHROMEDRIVER="C:\Program Files\chromedriver-win64\chromedriver.exe" # download the chromedriver that matches the chrome version you are using under https://www.chromedriverdownload.com/en/downloads/chromedriver-129-download
</pre>
- call <code>python src\main.py</code>
- [optional] call <code>deactivate</code>

Further changes:
- You can change the email under src/chatgpt_email.py in the prompt variable.
- Change your email provider under src/email_sender.py, the script uses silenium to send the email, so you might need to change the paths of the elements.
- Change your database structure under src/import_notion_items.py

## Every other time:
- call <code>venv\Scripts\activate</code>
- call <code>python src\main.py</code>
- [optional] call <code>deactivate</code>
