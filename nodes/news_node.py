from utility.variables import *
from utility.directory import *
from utility.scraper import scrape_parse_cna, scrape_parse_gn
from utility.formatter import format_markdown

# States
NEWSMENU, CNA, GRND = range(3)

# ---------------------------------------------------------------------------------------------------- #

async def news_node(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = "\n".join(["Welcome to the news node", 
                         "/news_cna - Get news from CNA",
                         "/news_gn - Get news from Ground News",
                        #  "/news_bb - Get news from Bloomberg",
                        #  "/news_yh - Get news from Yahoo News",
                        #  "/news_yh - Get news from NHK Japan",
                         "/cancel - Exit node"
                         ])
    await update.message.reply_text(message)
    return NEWSMENU

# ---------------------------------------------------------------------------------------------------- #
#                                                  CNA                                                 #
# ---------------------------------------------------------------------------------------------------- #

async def news_cna(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print(">> news_node.py > news_cna")
    await update.message.reply_text("Getting news from channelnewsasia...")

    # Check for .json file
    to_update, json_path = check_file_update(file=cna_json, path=data_path, hours=hours)
    print(f"> JSON path = {json_path}")
    global cna_json_path 
    cna_json_path = json_path

    # Run scraper if .json file does not exist or needs to be updated
    if to_update:
        print("> Running scraper.py > scrape_parse_cna to get .json file...")
        await scrape_parse_cna(save_folder=data_path)
    else:
        print(f"> '{cna_json}' was last modified less than {hours} hours ago, skipping scraping step.")

    with open(cna_json_path, 'r') as file:
        news_dict = json.load(file)
        if news_dict:
            SORT_ORDER = {"Business": 0, "World": 1, "Asia": 2, "East Asia": 3}
            message = "Select the news category.\n/cancel to return to news node."
            reply_keyboard = list(news_dict.keys())
            reply_keyboard.sort(key=lambda val : SORT_ORDER[val])
            reply_keyboard.append("/cancel")
            reply_keyboard = [reply_keyboard]
            await update.message.reply_text(message, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=False, 
                                                                                        one_time_keyboard=False, 
                                                                                        input_field_placeholder="Select category."))
            return CNA
        else:
            print(f"> Error occurred, news_dict is empty.")
            message = f"Error occurred, returning to news node."
            await update.message.reply_text(message)
            return NEWSMENU

async def show_cna(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    with open(cna_json_path, 'r') as file:
        news_dict = json.load(file)
    last_modified = datetime.fromtimestamp(os.path.getmtime(cna_json_path)).strftime("%Y-%m-%d・%H:%M")
    topic = update.message.text
    message = f"CNA: {topic}\nLast fetched {last_modified}\n"
    for article in news_dict[topic]:
        message += f"> [{article[0]}]({article[1]})\n\n"    
    message = format_markdown(text=message)
    await update.message.reply_text(message, parse_mode="MarkdownV2")

# ---------------------------------------------------------------------------------------------------- #
#                                               Ground News                                            #
# ---------------------------------------------------------------------------------------------------- #

async def news_gn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print(">> news_node.py > news_gn")
    await update.message.reply_text("Getting news from Ground News...")

    # Check for .json file
    to_update, json_path = check_file_update(file=gn_json, path=data_path, hours=hours)
    print(f"> JSON path = {json_path}")
    global gn_json_path
    gn_json_path = json_path

    # Run scraper if .json file does not exist or needs to be updated
    if to_update:
        print("> Running scraper.py > scrape_parse_gn to get .json file...")
        await scrape_parse_gn(save_folder=data_path)
    else:
        print(f"> '{gn_json}' was last modified less than {hours} hours ago, skipping scraping step.")

    with open(gn_json_path, 'r') as file:
        news_dict = json.load(file)
        if news_dict:
            message = "Select the news category.\n/cancel to return to news node."
            reply_keyboard = list(news_dict.keys())
            reply_keyboard.append("/cancel")
            reply_keyboard = [reply_keyboard]
            await update.message.reply_text(message, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=False, 
                                                                                        one_time_keyboard=False, 
                                                                                        input_field_placeholder="Select category."))
            return GRND
        else:
            print(f"> Error occurred, news_dict is empty.")
            message = f"Error occurred, returning to news node."
            await update.message.reply_text(message)
            return NEWSMENU
  
async def show_gn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    with open(gn_json_path, 'r') as file:
        news_dict = json.load(file)
    last_modified = datetime.fromtimestamp(os.path.getmtime(gn_json_path)).strftime("%Y-%m-%d・%H:%M")
    topic = update.message.text
    message = f"Ground News: {topic}\nLast fetched {last_modified}\n"
    for article in news_dict[topic]:
        message += f"> [{article[0]}]({article[1]})\n\n"    
    message = format_markdown(text=message)
    await update.message.reply_text(message, parse_mode="MarkdownV2")