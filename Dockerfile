FROM python:3.7-alpine
USER root
COPY pages.py pages.py
COPY chromedriver chromedriver
COPY SeleniumGMailTests.py SeleniumGMailTests.py
COPY GMailTest.py GMailTest.py
RUN pip install pytest
RUN pip install allure-pytest
RUN pip install allure-python-commons
RUN pip install selenium

# Installs latest Chromium package.
RUN echo @edge http://nl.alpinelinux.org/alpine/edge/community > /etc/apk/repositories \
    && echo @edge http://nl.alpinelinux.org/alpine/edge/main >> /etc/apk/repositories \
    && apk add --no-cache \
    libstdc++@edge \
    chromium@edge \
    harfbuzz@edge \
    nss@edge \
    freetype@edge \
    ttf-freefont@edge \
    && rm -rf /var/cache/* \
    && mkdir /var/cache/apk

# Add Chrome as a user
RUN mkdir -p /usr/src/app \
    && adduser -D chrome \
    && chown -R chrome:chrome /usr/src/app
#
CMD ["pytest", "GMailTest.py::test_send_email", "SeleniumGMailTests.py::test_send_message", "--alluredir=/tmp/my_allure_results"]

