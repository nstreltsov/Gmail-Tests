from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import allure
import time

class LoginPage:
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.wait = WebDriverWait(webdriver, 30, 0.5)

    @allure.step("Войти пользователем {username}")
    def login(self, username, password):
        self.webdriver.find_element(By.ID, "identifierId").send_keys(username)
        self.webdriver.find_element(By.ID, "identifierNext").click()
        password_field = self.wait.until(lambda wd: wd.find_element(By.ID, "password"))
        time.sleep(2)
        password_field.find_element(By.TAG_NAME, "input").send_keys(password)
        self.webdriver.find_element(By.ID, "passwordNext").click()
        return InboxPage(self.webdriver)


class InboxPage:
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.wait = WebDriverWait(webdriver, 30, 0.5)

    @allure.step("Написать сообщение")
    def open_new_message_dialog(self):
        self.wait.until(
            lambda wd: self.webdriver.find_element(By.XPATH,
                                                   ".//div[./text()='Написать']")).click()
        dialog = self.wait.until(
            lambda x: self.webdriver.find_element(By.XPATH, "//div[@role = 'dialog']"))
        return NewMessageDialog(dialog)

    @allure.step("Открыть последнее отправленное сообщение")
    def open_last_message(self):
        self.wait.until(
            lambda wd: self.webdriver.find_element(By.XPATH,
                                                   ".//*[@role='tabpanel']//table/tbody/tr[1]")).click()
        return Message(self.webdriver)

    @allure.step("Ждать окончание отправки сообщения")
    def wait_for_sending_message(self):
        self.wait.until(
            lambda wd: self.webdriver.find_element(By.XPATH,
                                                   ".//*[text()='Письмо отправлено.']")).click()
class Message:

    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.wait = WebDriverWait(webdriver, 30, 0.5)

    def check_message(self, to_address, subject, message):
        assert to_address in self.wait.until(
            lambda wd: self.webdriver.find_element(By.XPATH,
                                                   ".//span[@email]/following-sibling::span[text()]")).text
        assert subject in self.wait.until(
            lambda wd: self.webdriver.find_element(By.XPATH,
                                                   ".//table//h2[text() and @data-thread-perm-id]")).text
        assert message in self.wait.until(
            lambda wd: self.webdriver.find_element(By.XPATH,
                                                   ".//*[@data-message-id]//div[text()][1]")).text

class NewMessageDialog:
    def __init__(self, element):
        self.element = element
        self.webdriver = element.parent
        self.wait = WebDriverWait(self.webdriver, 30, 0.5)

    @allure.step("Заполнить сообщение для [{to}] c  темой [{subject}] и телом [{body}]")
    def fill(self, to, subject, body):
        self.element.find_element(By.XPATH, "//form//textarea[@name='to']").send_keys(to)
        self.element.find_element(By.XPATH, "//form//input[@name='subjectbox']").send_keys(subject)
        self.element.find_element(By.XPATH, "//div[@role='textbox' and @aria-label='Тело письма']").send_keys(
            body)
        return self

    @allure.step("Отправить сообщение")
    def send(self):
        self.element.find_element(By.XPATH, "//div[@role='button' and text()='Отправить']").click()
        return InboxPage(self.webdriver)