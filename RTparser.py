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
        if (x.find("article") != -1 or x.find("news") != -1) and not x.startswith("http") and len(x) > 20:
            return True
        return False


def rt_parse(pages=5):
    url = r"https://russian.rt.com/business"

    profile_path = r'C:\Users\ujifv\AppData\Roaming\Mozilla\Firefox\Profiles\ojy7pkea.default'
    options = Options()
    options.set_preference('profile', profile_path)
    service = Service(r'D:\python\VTB_tricks\geckodriver.exe')
    driver = Firefox(options=options, executable_path=GeckoDriverManager().install())
    driver.get(url)
    cookies = driver.find_element(By.XPATH, "/html/body/div[2]/div[7]/div/a")
    cookies.click()
    for i in range(pages):
        element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[4]/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/a")))
        count = 0
        while count < 15:
            try:
                button = driver.find_element(By.XPATH, "/html/body/div[2]/div[4]/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/a")
                button.click()
                break
            except:
                count += 1
                driver.implicitly_wait(30)

    driver.implicitly_wait(10)
    resp = driver.page_source
    driver.close()

    soup = BeautifulSoup(resp, 'lxml')
    links = [link.get('href') for link in soup.find_all('a')]
    news_link = list(filter(is_news, list(set(links))))

    clear_news = []
    data = []
    headers = []
    urls = []
    news_link = list(map(str, news_link))

    for i in range(len(news_link)):
        if "#href" in news_link[i]:
            x = news_link[i]
            news_link[i] = x[:x.index("#href")]

    for link in list(set(news_link)):

        if url.endswith(r"\world"):
            req = requests.get(url[:-6] + link)
            urls.append(url[:-6] + link)
        else:
            req = requests.get(url[:-9] + link)
            urls.append(url[:-9] + link)

        if req.status_code == 200:
            soup = BeautifulSoup(req.text, "lxml")
            ans = soup.findAll("div",
                               {"class": ["article__summary", "article__summary_article-page", "js-mediator-article"]})

            str_news = ""
            for n in ans:
                str_news += n.text.replace("\n", " ").replace('\xa0', ' ')

            clear_news.append(str_news.replace("  ", " "))
            data.append(soup.find("time", {"class": "date"}).text.strip()[:-7])
            headers.append(soup.find("h1", {"class": ["article__heading", "article__heading_article-page"]}).text)

    news = {i: {"url": urls[i], "header": headers[i], "date": data[i], "news": clear_news[i]} for i in range(len(data))}

    with open("data/rt_news.json", "w", encoding='utf-8') as out:
        out.write(json.dumps(news, ensure_ascii=False))
