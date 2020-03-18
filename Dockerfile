FROM python:3.7-alpine
COPY GMailTest.py GMailTest.py
RUN pip install pytest
RUN pip install allure-pytest
RUN pip install allure-python-commons
RUN pip install selenium
CMD ["pytest", "GMailTest.py::test_send_email", "--alluredir=/tmp/my_allure_results"]
CMD ["pytest", "SeleniumGMailTests.py::test_send_message", "--alluredir=/tmp/my_allure_results"]