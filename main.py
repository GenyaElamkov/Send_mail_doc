"""
Скрипт отправляет pdf документы на
"""

import configparser
import mimetypes
import os
import smtplib
import ssl
import time
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr, make_msgid

config = configparser.ConfigParser()
config.read('./settings.ini', encoding='utf-8')

from_mail = config['EMAIL_FROM']['FROM_MAIL']  # Почта отправителя.
password = config['EMAIL_FROM']['PASSWORD']  # Пароль отправителя.
sender_name = config['EMAIL_FROM'][
    'SENDER_NAME']  # Отображение имени отправителя рядом с почтой.

to_mail = config['EMAIL_TO']['TO_MAIL']  # Почта принимающая.
recipient_name = config['EMAIL_TO'][
    'RECIPIENT_NAME']  # Отображение имени почты кому приходит письмо.

host_smtp = config['SMTP_SSL']['HOST_SMTP']  # Хост для исходящий сообщений.
port = int(config['SMTP_SSL']['PORT'])  # Порт для исходящих сообщений.

subject = config['SUBJECT']['SUBJECT']  # Тема письма.

# # For read mail.
imap_server = config['IMAP']['IMAP_SERVER']  # Хост для входящий сообщений.


def send_email(dir_name: str) -> str:
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL(host_smtp, port, context=context) as s:
            s.login(from_mail, password)
            # s.set_debuglevel(1)
            msg = MIMEMultipart()
            msg['From'] = formataddr((sender_name, from_mail))
            msg['To'] = formataddr((recipient_name, to_mail))
            msg['Subject'] = subject
            msg['Message-ID'] = make_msgid()

            print("Collecting...")
            files = os.listdir(dir_name)
            for file in files:
                ftype, encoding = mimetypes.guess_type(file)
                file_type, subtype = ftype.split("/")

                with open(f"Отправить/{file}", "rb") as f:
                    att = MIMEApplication(f.read(), subtype)

                att.add_header('Content-Disposition', 'attachment',
                               filename=file)
                msg.attach(att)

                s.sendmail(from_mail, to_mail, msg.as_string())

        return 'Сообщение отправлено успешно!'
    except Exception as _ex:
        return f"{_ex}\nПожалуйста, проверьте свой логин или пароль!"


def main() -> None:
    dir_name = "Отправить"
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)

    print(
        "Скрипт отправляет pdf документы на почту.\nНастройка почты в файле setting.ini\n")
    print(send_email(dir_name))
    time.sleep(10)


if __name__ == "__main__":
    main()
