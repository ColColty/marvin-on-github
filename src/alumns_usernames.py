import pymongo
import imaplib
import email
import re
import os


myclient = pymongo.MongoClient('mongodb://{}:{}@db:27017/'.format(os.getenv('DB_USERNAME'), os.getenv('DB_PASSWORD')))
mydb = myclient["alumnee"]
usernames = mydb.students_usernames

FROM_EMAIL = os.getenv('EMAIL_USERNAMES')
FROM_PWD = os.getenv('EMAIL_USERNAMES_PASSWORD')
STMP_PORT = os.getenv('EMAIL_USERNAMES_SMTP_PORT')
SMTP_SERVER = os.getenv('EMAIL_USERNAMES_SMTP_SERVER')


def getNewUsernames():
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL, FROM_PWD)
    mail.select('inbox')
    search_path = '(SUBJECT "{}")'.format(os.getenv('SUBJECT_EMAIL_USERNAMES'))
    type, data = mail.search(None, search_path)
    mail_ids = data[0]
    id_list = mail_ids.split()
    type, data = mail.fetch(id_list[0], '(RFC822)')

    for id in id_list:
        type, data = mail.fetch(id, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1].decode())
                email_subject = msg['subject']
                email_from = msg['from']
                email_body = '\n'.join([str(payload) for payload in msg.get_payload()]) if msg.is_multipart() else msg.get_payload()
                regex = re.search("Username\\s*:\\s*(.+)\\s*Email\\s*:\\s*([\\S]+@epitech.eu)", email_body)
                if regex == None:
                    continue
                if len([user for user in usernames.find({"username": regex.group(1), "email": regex.group(2)})]):
                    continue
                usernames.insert_one({"username": regex.group(1).strip(), "email": regex.group(2).strip()})


if __name__ == "__main__":
    getNewUsernames()