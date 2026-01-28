# python-telegram-bots
Last updated: 2026-01-28

Personal project, telegram bot as an assistant/pinboard.

Using Python, python-telegram-bot, https://docs.python-telegram-bot.org/en/v21.8/index.html.

----------

# Node Log

| Ready | Node    | To work on |
| ----- | ------- | ---------- |
|   o   | news    | NHK Japan. Bloomberg. |
|   o   | sleep   | Input checker for 24h time. Sleep analytics. |
|   x   | expense | . |

--------------------------------------------------------------------------------

# Commands

## Standard

### /start
Starts the bot and display opening message.

### /help
Displays available commands that starts a node/feature.

----------

## Features

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

----------

### /sleep
For logging sleep timings.

#### /sleep_add
Add a sleep timing to a sleep log file.

#### /sleep_view
Shows the entire sleep log.

#### /sleep_clear
Clears the sleep log file, have to manually input this command.

----------

### /expense
For logging simple expenses.

#### /expense_add
Add an expense.

#### /expense_view
Get total expenses for a selected year-month.

#### /expense_clear
Clears the expense log file, have to manually input this command.

--------------------------------------------------------------------------------

# Ideas for future features/nodes

## /workout
For setting and tracking exercise rep goals.

## /mail
Fetches mail from gmail.

--------------------------------------------------------------------------------