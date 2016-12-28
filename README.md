# MailID_Validator
Python script to validate the email address using syntax, MX record and mailbox verification.

# Installation
sudo pip install -r requirements.txt

# Steps
- Create a file named mail_ids.txt and copy all the mail ids in that file one by one.
- Run the script, python mailId_validator.py

# About the Code
It will only validate 2 mail ids for 10 minutes to avoid IP blacklist issue.
Finally the valid mail ids will be stored in a file valid_mail_ids.txt and invalid mail ids will be stored in a seperate file invalid_mail_ids.txt.


