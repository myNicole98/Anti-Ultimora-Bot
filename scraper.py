from bs4 import BeautifulSoup
import configparser
import requests

# Config initialization
config = configparser.ConfigParser()
config.read('config.ini')

def channel_updater(channel):
    URL = f"https://t.me/s/{channel}"
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html5lib')
    messages = soup.find_all("div", class_="tgme_widget_message_text")
    return messages

def channel_scraper(count, messages):
    lastmessage = messages[len(messages)-count].text
    return lastmessage