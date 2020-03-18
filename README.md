GMailTest.py - содержит тест на отправку сообщения через API
SeleniumGMailTests.py - содержит тест на отправку сообщения с использованием Selenium

pytest GMailTest.py::test_send_email --alluredir=/tmp/my_allure_results
pytest SeleniumGMailTests.py::test_mail_send_success --alluredir=/tmp/my_allure_results