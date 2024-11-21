from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

sbr_webdriver = os.environ['SBR_WEBDRIVER']

def scrape_html_site(website):
    print('Connecting to Scraping Browser...')
    sbr_connection = ChromiumRemoteConnection(sbr_webdriver, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating...')
        driver.get(website)
        print("Waiting captcha to solve...")
        solve_res = driver.execute(
            "executeCdpCommand",
            {
                "cmd": "Captcha.waitForSolve",
                "params": {"detectTimeout": 10000},
            },
        )
        print("Captcha solve status:", solve_res["value"]["status"])
        print('Navigated! Scraping page content...')
        html = driver.page_source
        print(html)
        return html

def get_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def process_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    for element in soup(["script", "style"]):
        element.extract()
    cleaned_body_content = soup.get_text(separator="\n")
    cleaned_body_content = "\n".join(
        line.strip() for line in cleaned_body_content.splitlines() if line.strip()
    )
    return cleaned_body_content

def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
