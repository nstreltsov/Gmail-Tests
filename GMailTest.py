import smtplib
import imaplib
import allure
import datetime
import email
import pytest

FROM_ADDRESS = 'applineautotests@gmail.com'
LOGIN = 'applineautotests'
PASSWORD = 'appline2020'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
IMAP_SERVER = 'imap.gmail.com'

@allure.title("Проверка отправки сообщения GMail с помощью API")
@allure.description("""Выполняется проверка того, что отправленное сообщение появляется в папке Отправленные""")
@pytest.mark.parametrize('to_address,subject,message', [
    ('applineautotests@gmail.com', 'Autotest1', 'test'),
    ('applineautotests@gmail.com', 'Autotest2', 'test')
])
def test_send_email(to_address, subject, message):
    step_send_message(to_address, 'Subject: {}\n\n{}'.format(subject, message))
    step_check_message('"Inbox"', subject, message)
    step_check_message('"[Gmail]/Sent Mail"', subject, message)

@allure.step('send message {0} {1}')
def step_send_message(to_address, message):
    smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp.starttls()
    smtp.login(LOGIN, PASSWORD)
    smtp.sendmail(FROM_ADDRESS, to_address, message)
    smtp.quit()

@allure.step('check message {0} {1} {2}')
def step_check_message(folder, subject, message):
    imap = imaplib.IMAP4_SSL(IMAP_SERVER)
    imap.login(LOGIN, PASSWORD)
    imap.select(folder)
    date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")

    result, data = imap.uid('search', None,
                            '(SENTSINCE {date} HEADER Subject "{subject}")'.format(
                                date=date, subject=subject))
    latest_email_uid = data[0].split()[-1]
    result, data = imap.uid('fetch', latest_email_uid, '(RFC822)')
    raw_email = data[0][1]
    email_message = email.message_from_bytes(raw_email)
    print(email_message['Date'])
    if email_message.is_multipart():
        for payload in email_message.get_payload():
            if payload.get_content_type() == 'text/plain':
                assert message in payload.get_payload()