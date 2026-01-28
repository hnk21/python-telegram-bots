import aiohttp, asyncio, os, json
from bs4 import BeautifulSoup
from collections import defaultdict
from datetime import date, datetime, timedelta
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Application, CommandHandler, ConversationHandler, ContextTypes, MessageHandler, filters

from utility.directory import find_folder

# Set directory for data folder
data_folder = "python-telegram-bots/data"
data_path = find_folder(data_folder)

### For standard.py > get_time()
weekdays_en_jp = {"Monday"   : "月", 
                  "Tuesday"  : "火",
                  "Wednesday": "水",
                  "Thursday" : "木",
                  "Friday"   : "金",
                  "Saturday" : "土",
                  "Sunday"   : "日"
                  }

### Log files
sleep_log   = "sleep_log.txt"
expense_log = "expense_log.txt"

### For news_node.py
# Threshold for last modified duration of file
hours = 6

# CNA
cna_url = "https://www.channelnewsasia.com/latest-news"
cna_html = "news_cna.html"
cna_json = "news_cna.json"

# Ground News
# Will have multiple .html files
# One .html for each topic in gn_topics
gn_base = "https://ground.news"
gn_url  = "https://ground.news/interest/"
gn_topics = {"stock-markets": "Stock Markets", 
             "tech": "Tech", 
             "asia": "Asia", 
             "north-america": "North America"}
gn_json = "news_gn.json"