# -*- coding: utf-8 -*-
import logging
import requests
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


log = logging.getLogger(__name__)


def _download_request(url, verify=True):
    retry_strategy = Retry(
        total=5,
        backoff_factor=2,
        status_forcelist=[403, 429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)
    headers = {'user-agent': 'Mozilla Firefox Mozilla/5.0; metaodi website-monitor at github'}
    r = http.get(url, headers=headers, timeout=20, verify=verify)
    r.raise_for_status()
    return r


def download(url, encoding='utf-8', verify=True):
    r = _download_request(url, verify=verify)
    if encoding:
        r.encoding = encoding
    return r.text


def download_content(url, verify=True):
    r = _download_request(url, verify=verify)
    return r.content


def jsondownload(url, verify=True):
    r = _download_request(url, verify=verify)
    return r.json()


def download_file(url, path, verify=True):
    r = _download_request(url, verify=verify)
    with open(path, 'wb') as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)


def download_with_selenium(url, selector):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)

    driver.get(url)
    try:
        wait = WebDriverWait(driver, 20)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
        time.sleep(5)
        content = driver.page_source
    except TimeoutException:
        # if the selector was not found return a static string
        log.info(f"selector '{selector}' not found!")
        content = f"selector '{selector}' not found"
    finally:
        driver.quit()

    return content
