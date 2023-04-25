import os
import imaplib
import email
from email.header import decode_header
from email.utils import parsedate_tz
import base64
from dotenv import load_dotenv
from pymongo import MongoClient


def get_data() -> list:
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    MAIL = os.getenv('MAIL')
    data = []
    mail_pass = TOKEN
    username = MAIL
    imap_server = "imap.mail.ru"
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(username, mail_pass)
    a = imap.select("INBOX")
    for i in str(imap.search(None, 'ALL')[1][0])[2:-1].split():
        res, msg = imap.fetch(str(i).encode(), '(RFC822)')
        msg = email.message_from_bytes(msg[0][1])

        letter_date = parsedate_tz(msg[
                                       "Date"])  # дата получения, приходит в виде строки, дальше надо её парсить в формат datetime
        letter_from = msg["Return-path"]  # e-mail отправителя

        subject = decode_header(msg["Subject"])[0][0]
        if type(subject) != str:
            subject = subject.decode()
        main_text = ''

        payload = msg.get_payload()
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain':
                    try:
                        main_text = base64.b64decode(part.get_payload()).decode()
                    except UnicodeDecodeError:
                        main_text = base64.b64decode(part.get_payload()).decode('latin-1')
                    except:
                        pass

        elif type(payload) == str:
            main_text = base64.b64decode(payload).decode()
        else:
            main_text = base64.b64decode(str(payload)).decode()

        data.append({
            'letter_date': letter_date,
            'letter_from': letter_from,
            'subject': subject,
            'main_text': main_text
        })

    return data


def main():
    data = get_data()

    client = MongoClient()
    db = client.email_message

    for i in data:
        msg_in_db = db.email_message.find(
            {
                'letter_date': i['letter_date'],
                'subject': i['subject'],
            }
        )
        if not list(msg_in_db):
            db.email_message.insert_one(i)


if __name__ == '__main__':
    main()
