from selenium import webdriver
import allure
import pages
import time
import pytest

LOGIN = 'applineautotests'
PASSWORD = 'appline2020'

@allure.step("Открыть Gmail")
def open_gmail():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("disable-dev-shm-usage");
    options.add_argument("no-sandbox");
    options.add_argument("window-size=1024,768");
    driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)
    driver.get('https://gmail.com')
    return pages.LoginPage(driver)

@allure.title("Проверка отправки сообщения GMail с помощью Selenium")
@allure.description("""Выполняется проверка того, что отправленное сообщение появляется в папке Входящие""")
@pytest.mark.parametrize('to_address,subject,message', [
    ('applineautotests@gmail.com', 'Autotest1', 'test'),
    ('applineautotests@gmail.com', 'Autotest2', 'test')
])
def test_send_message(to_address, subject, message):
    inbox_page = open_gmail().login(LOGIN, PASSWORD)
    inbox_page\
        .open_new_message_dialog()\
        .fill(to_address, subject, message)\
        .send()\
        .wait_for_sending_message()

    inbox_page.open_last_message().check_message(to_address, subject, message)
