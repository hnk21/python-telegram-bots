# python-telegram-bots
Last updated: 2026-04-12

Personal project, telegram bot as an assistant/pinboard.

Using Python, python-telegram-bot, https://docs.python-telegram-bot.org/en/v21.8/index.html.

----------

# Idea Backlog
 
- Convert data logging to sqlite3
- Notion Node
    - Pull events from akr workspace > 1_EVENTS page
    - Not sure what to do with akr workspace > 2_BUNKA, hnk workspace yet 
- AI Summarizer Node
    - Input url to LLM via LLM API, have it return a summmary
- AI Chatbot that speaks like Pochita
    - For fun

--------------------------------------------------------------------------------

# Commands

## Basic

### /start
Starts the bot and display opening message.

### /help
Displays available commands that starts a node/feature.

----------

## Nodes

### /news
News scraper.
- Channel News Asia
    - https://www.channelnewsasia.com/latest-news, for the following categories: 
    - Business, World, Asia, East Asia 
- Ground News
    - https://ground.news/interest/stock-markets
    - https://ground.news/interest/tech
    - https://ground.news/interest/asia
    - https://ground.news/interest/north-america
- NHK Japan
    - https://news.web.nhk/newsweb/genre/, for the following categories:
    - business, society, politics, international

----------

### /sleep
For logging sleep timings.

- /sleep_add
    - Add a sleep timing to a sleep log file.
- /sleep_view
    - Shows the entire sleep log.
- /sleep_clear
    - Clears the sleep log file. Manually typed command.

----------

### /expense
For logging simple expenses.

- /expense_add
    - Add an expense.
- /expense_view
    - Get total expenses for a inputted year-month.
- /expense_clear
    - Clears the expense log file, Manually typed command.

--------------------------------------------------------------------------------