from utility.helper import *
from utility.scraper import parse_html_cna, parse_html_gn, parse_html_nhk
from utility.formatter import format_markdown

# States
NEWSMENU, CNA, GRND, NHK = range(4)

# ---------------------------------------------------------------------------------------------------- #

async def news_node(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    print(f"\n>> news_node.py > news_node > User: {user["username"]}")
    name = user["first_name"]
    message = "\n".join([f"Welcome to the news node {name}", 
                         "/news_cna - Get news from CNA",
                         "/news_gn - Get news from Ground News",
                         "/news_nhk - Get news from NHK Japan",
                         "/cancel - Exit node"
                         ])
    await update.message.reply_text(message)
    return NEWSMENU

# ---------------------------------------------------------------------------------------------------- #
#                                                  CNA                                                 #
# ---------------------------------------------------------------------------------------------------- #

async def news_cna(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Getting news from ChannelNewsAsia...")

    # Check for .json file
    global cna_json_path
    to_update, cna_json_path = check_file_update(file=cna_json, folder_path=json_folder_path, hours=hours)

    # Run scraper if .json file does not exist or needs to be updated
    if to_update:
        print("\n>> news_node.py > news_cna \n> Running scraper.py > parse_html_cna to get .json file...")
        await parse_html_cna()
    else:
        print(f"\n>> news_node.py > news_cna \n> '{cna_json}' was last modified < {hours} hours ago, skipping scraping step.")

    with open(cna_json_path, 'r') as file:
        news_dict = json.load(file)
        if news_dict:
            SORT_ORDER = {"Business": 0, "World": 1, "Asia": 2, "East Asia": 3}
            message = "Select the news category.\n/cancel to return to news node."
            reply_keyboard = list(news_dict.keys())
            reply_keyboard.sort(key=lambda val : SORT_ORDER[val])
            reply_keyboard.append("/cancel")
            reply_keyboard = [reply_keyboard]
            await update.message.reply_text(message, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=False, one_time_keyboard=False, input_field_placeholder="Select category."))
            return CNA
        else:
            print(f"\n>> news_node.py > news_cna \n> Error occurred, news_dict is empty.")
            message = f"Error occurred, returning to news node."
            await update.message.reply_text(message)
            return NEWSMENU

async def show_cna(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    with open(cna_json_path, 'r') as file:
        news_dict = json.load(file)
    
    last_modified = datetime.fromtimestamp(os.path.getmtime(cna_json_path)).strftime("%Y-%m-%d・%H:%M")
    topic = update.message.text
    message = f"CNA: {topic}\nLast fetched {format_markdown(last_modified)}\n"
    
    for article in news_dict[topic]:
        title, link = format_markdown(article[0]), format_markdown(article[1])
        message += f"> [{title}]({link})\n\n"
    await update.message.reply_text(message, parse_mode="MarkdownV2")

# ---------------------------------------------------------------------------------------------------- #
#                                               Ground News                                            #
# ---------------------------------------------------------------------------------------------------- #

async def news_gn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Getting news from Ground News...")

    # Check for .json file
    global gn_json_path
    to_update, gn_json_path = check_file_update(file=gn_json, folder_path=json_folder_path, hours=hours)

    # Run scraper if .json file does not exist or needs to be updated
    if to_update:
        print("\n>> news_node.py > news_gn \n> Running scraper.py > parse_html_gn to get .json file...")
        await parse_html_gn()
    else:
        print(f"\n>> news_node.py > news_gn \n> '{gn_json}' was last modified < {hours} hours ago, skipping scraping step.")

    with open(gn_json_path, 'r') as file:
        news_dict = json.load(file)
        if news_dict:
            message = "Select the news category.\n/cancel to return to news node."
            reply_keyboard = list(news_dict.keys())
            reply_keyboard.append("/cancel")
            reply_keyboard = [reply_keyboard]
            await update.message.reply_text(message, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=False, one_time_keyboard=False, input_field_placeholder="Select category."))
            return GRND
        else:
            print(f"\n>> news_node.py > news_gn \n> Error occurred, news_dict is empty.")
            message = f"Error occurred, returning to news node."
            await update.message.reply_text(message)
            return NEWSMENU
  
async def show_gn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    with open(gn_json_path, 'r') as file:
        news_dict = json.load(file)
    last_modified = datetime.fromtimestamp(os.path.getmtime(gn_json_path)).strftime("%Y-%m-%d・%H:%M")
    topic = update.message.text
    message = f"Ground News: {topic}\nLast fetched {format_markdown(last_modified)}\n"
    for article in news_dict[topic]:
        title, link = format_markdown(article[0]), format_markdown(article[1])
        message += f"> [{title}]({link})\n\n"
    await update.message.reply_text(message, parse_mode="MarkdownV2")

# ---------------------------------------------------------------------------------------------------- #
#                                               NHK Japan                                              #
# ---------------------------------------------------------------------------------------------------- #

async def news_nhk(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Getting news from NHK Japan...")

    # Check for .json file
    global nhk_json_path
    to_update, nhk_json_path = check_file_update(file=nhk_json, folder_path=json_folder_path, hours=hours)

    # Run scraper if .json file does not exist or needs to be updated
    if to_update:
        print("\n>> news_node.py > news_nhk \n> Running scraper.py > parse_html_nhk to get .json file...")
        await parse_html_nhk()
    else:
        print(f"\n>> news_node.py > news_nhk \n> '{nhk_json}' was last modified < {hours} hours ago, skipping scraping step.")

    with open(nhk_json_path, 'r') as file:
        news_dict = json.load(file)
        if news_dict:
            message = "Select the news category.\n/cancel to return to news node."
            reply_keyboard = list(news_dict.keys())
            reply_keyboard.append("/cancel")
            reply_keyboard = [reply_keyboard]
            await update.message.reply_text(message, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=False, one_time_keyboard=False, input_field_placeholder="Select category."))
            return NHK
        else:
            print(f"\n>> news_node.py > news_cna \n> Error occurred, news_dict is empty.")
            message = f"Error occurred, returning to news node."
            await update.message.reply_text(message)
            return NEWSMENU
        
async def show_nhk(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    with open(nhk_json_path, 'r') as file:
        news_dict = json.load(file)
    last_modified = datetime.fromtimestamp(os.path.getmtime(nhk_json_path)).strftime("%Y-%m-%d・%H:%M")
    topic = update.message.text
    message = f"NHK Japan: {topic}\nLast fetched {format_markdown(last_modified)}\n"
    for article in news_dict[topic]:
        title, link = format_markdown(article[0]), format_markdown(article[1])
        message += f"> [{title}]({link})\n\n"
    await update.message.reply_text(message, parse_mode="MarkdownV2")