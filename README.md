# python-telegram-bots
Last updated: 2026-04-25

Personal project, telegram bot as an assistant/pinboard.

Using python-telegram-bot, as the front end interaction

https://docs.python-telegram-bot.org/en/v21.8/index.html

--------------------------------------------------

# Idea Backlog
 
- **AI node**
    - Google Gemini
    - Prepare different rules to control the response allowed for the LLM, each catered to specific answer requirements
        - General query
        - News article summariser
        - Answer as a certain character (e.g. Chainsawman Pochita)
            - Joke feature, not sure where to go with this
- **Notion node**
    - akr workspace > 2_BUNKA > Japanese vocab training
        - Return overall result of practice (which words ok, which words redo)
    - akr workspace > 1_EVENTS
        - Fetch today's events
        - Fetch this week's events
- Convert data logging from .txt to .db sqlite3
    - Expense node
    - Sleep node
- Expense node
    - Analysis? Amount spent over each month, return .png of chart
- Sleep node
    - Analysis?

--------------------------------------------------

# Commands

## Basic

### /start
Starts the bot and display opening message.

### /help
Displays available commands that starts a node/feature.

--------------------------------------------------

## Public Nodes

### /news
Pulls news article titles and links from selected sites.
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

--------------------------------------------------

## Personal Nodes

### /notion
Integration with personal Notion workspace.

### /steam

### /ai

### /sleep
For logging sleep timings.

- /sleep_add
    - Add a sleep timing to a sleep log file.
- /sleep_view
    - Returns the entire sleep log.
- /sleep_clear
    - Clears the sleep log file. Manually typed command.

### /expense
For logging simple expenses.

- /expense_add
    - Add an expense.
- /expense_view
    - Get total expenses for a inputted year-month.
- /expense_clear
    - Clears the expense log file, Manually typed command.

--------------------------------------------------