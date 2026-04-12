# -------------------------------------------------- #
# imports                                            #
# -------------------------------------------------- #

import aiohttp, asyncio, os, json
from dotenv import load_dotenv, dotenv_values
from bs4 import BeautifulSoup
from collections import defaultdict
from datetime import date, datetime, timedelta
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Application, CommandHandler, ConversationHandler, ContextTypes, MessageHandler, filters

# -------------------------------------------------- #
# directory functions                                #
# -------------------------------------------------- #

# Finds target folder and returns its path
def find_folder(folder: str):
    for root, dirs, files in os.walk(os.getcwd()):
        if folder in root:
            print(f"\n>> helper.py > find_folder \n> Found target folder '{folder}' in '{root}'")
            return root

# Checks if file exists, if not - creates a new one, then returns its path
def check_file(file: str, folder_path: str):
    file_path = folder_path + "/" + file
    if not os.path.exists(file_path):
        with open(file_path, "w") as log:
            pass
        print(f"\n>> helper.py > check_file \n> Created '{file}' in '{folder_path}'")
    else:
        print(f"\n>> helper.py > check_file \n> Found '{file}' in '{folder_path}'")
    return file_path

# Checks if file needs to be created/updated depending on whether it was last modified more than some specified number hours ago
# Returns boolean value indicating whether file needs to be created/updated, and its file path
def check_file_update(file: str, folder_path: str, hours: int):
    file_path = folder_path + "/" + file
    to_update = True
    if os.path.exists(file_path):
        last_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
        hours_ago = (datetime.now() - last_modified).days * 24 + (datetime.now() - last_modified).seconds / 3600
        if hours_ago > hours:
            to_update = True
        else:
            to_update = False
        print(f"\n>> helper.py > check_file_update \n> Found '{file}', last modified {round(hours_ago, 0)} hours ago")
    else:
        print(f"\n>> helper.py > check_file_update \n> '{file}' not found in target folder '{folder_path}'")
        to_update = True
    return to_update, file_path

# -------------------------------------------------- #
# variables                                          #
# -------------------------------------------------- #

## Set path of data folder
data_folder = "python-telegram-bots/data"
data_path = find_folder(data_folder)
html_folder_path = data_path + "/_html"
json_folder_path = data_path + "/_json"

## Get variables from .env
load_dotenv()
telegram_token = os.getenv("TELEGRAM_API_TOKEN")
# notion_token = os.getenv("NOTION_API_TOKEN_1_EVENTS")
master = os.getenv("MASTER")

## For nodes > standard.py > get_time()
weekdays_en_jp = {"Monday"   : "月", 
                  "Tuesday"  : "火",
                  "Wednesday": "水",
                  "Thursday" : "木",
                  "Friday"   : "金",
                  "Saturday" : "土",
                  "Sunday"   : "日"
                  }

## data folder > .txt log files
sleep_log   = "sleep_log.txt"
expense_log = "expense_log.txt"

## For nodes > news_node.py 
hours = 6 # Threshold for last modified duration of file

# CNA
cna_url = "https://www.channelnewsasia.com/latest-news"
cna_html = "news_cna.html"
cna_json = "news_cna.json"

# Ground News
gn_url  = "https://ground.news/interest/"
gn_base = "https://ground.news"
gn_topics = {"stock-markets": "Stock Markets", 
             "tech": "Tech", 
             "asia": "Asia", 
             "north-america": "North America"}
gn_json = "news_gn.json"

# NHK Japan
nhk_url = "https://news.web.nhk/newsweb/genre/"
nhk_topics   = {"business": "経済", 
                "society": "社会", 
                "politics": "政治", 
                "international": "国際"}
nhk_json     = "news_nhk.json"