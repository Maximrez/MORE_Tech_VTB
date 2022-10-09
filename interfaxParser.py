import json
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager


def is_news(x):
    x = str(x)
    if x is None:
        return False
    else:
        if x.startswith("/business"):
            return True
        return False


def interfax_parse(pages=5):
    url = r"https://www.interfax.ru/business/"
    resp = requests.get(url)

    profile_path = r'C:\Users\Максим\AppData\Roaming\Mozilla\Firefox\Profiles\ojy7pkea.default'
    options = Options()
    options.set_preference('profile', profile_path)
    service = Service(r'D:\python\VTB_tricks\geckodriver.exe')
    driver = Firefox(options=options, executable_path=GeckoDriverManager().install())
    driver.get(url)
    driver.implicitly_wait(15)
    cookies = driver.find_element("xpath", "/html/body/div[8]/span")
    cookies.click()

    for i in range(pages):
        try:
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "timeline__more")))
            count = 0
            while count < 15:
                try:
                    button = driver.find_element(By.CSS_SELECTOR, ".timeline__more")
                    button.click()
                    break
                except:
                    count += 1
                    driver.implicitly_wait(30)
        except:
            break

    driver.implicitly_wait(10)
    resp = driver.page_source
    driver.close()

    soup = BeautifulSoup(resp, 'lxml')
    links = [link.get('href') for link in soup.find_all('a')]
    news_link = list(filter(is_news, list(set(links))))
    news_link = list(map(str, news_link))
    clear_news = []
    data = []
    headers = []
    urls = []

    for link in news_link:
        if url.endswith(r"\world"):
            req = requests.get(url[:-6] + link)
            urls.append(url[:-6] + link)
        else:
            req = requests.get(url[:-9] + link)
            urls.append(url[:-9] + link)
        if req.status_code == 200:
            try:
                soup = BeautifulSoup(req.text, "lxml")
                ans = soup.find("article", {"itemprop": "articleBody"})
                headers.append(soup.find("h1", {"itemprop": "headline"}).text)
                clear_news.append(ans.text.strip())
                date = soup.find("a", {"class": "time"}).text.strip()
                data.append(date[7:])
            except:
                continue

    news = {i: {"url": urls[i], "header": headers[i].replace("\u2192", "-").replace("\u22c5", ' '),
                "date": data[i].replace("\u2192", "-").replace("\u22c5", ' '), "news": clear_news[i].replace("\u2192", "-").replace("\u22c5", ' ')} for i in
            range(len(data))}

    with open("data/interfax_news.json", "w", encoding='ISO-8859-1') as out:
        out.write(json.dumps(news, ensure_ascii=False))
