from utility.helper import *

# States
NOTIONMENU, JP_VOCAB_GET, JP_VOCAB_ANS, JP_VOCAB_UPD = range(4)
reply_keyboard = [["☓", "◯"]]

# ---------------------------------------------------------------------------------------------------- #

async def notion_node(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    print(f"\n>> notion.py > notion_node > User: {user["username"]}")
    name, username = user["first_name"], user["username"]
    if username == master:
        message = "\n".join(["Welcome to the Notion node",
                            "/notion_jp_vocab - 日本語の語彙を練習",
                            # "/notion_ - Do something on Notion",
                            # "/notion_ - Do something on Notion",
                            "/cancel - Exit node"
                            ])
    else:
        message = f"Hey '{name}' you can't access this node!"
    await update.message.reply_text(message)
    return NOTIONMENU

# ---------------------------------------------------------------------------------------------------- #

async def notion_jpvocab(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "語彙の練習：１から３０までの数字を入力してください"
    await update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
    return JP_VOCAB_GET

async def notion_jpvocab_get(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global page_size; page_size = update.message.text
    page_size = int(page_size)
    message = f"Fetching {page_size} entries..."
    payload = {
        "sorts": [ 
            {
                "property": "Revised", "direction": "ascending"
            }
        ],
        "filter": {
            "property": "State", "type": "select",
            "select": { "equals": "redo" }
        },
        "page_size": page_size,
        "in_trash": False,
        "result_type": "page"
    }
    success = notion_post_querydatasource(data_source_id = notion_datasource_id_jpvocab, payload = payload)
    if success:
        message += "ok\n"
        await update.message.reply_text(message)
        global curr; curr = 0
        with open(json_folder_path + "/" + jpvocab_json, 'r') as file:
            global vocab_dict
            vocab_dict = json.load(file)
        global pages_to_update; pages_to_update = defaultdict()
        message = "Press Start to commence practice"
        await update.message.reply_text(message, reply_markup=ReplyKeyboardMarkup([["Start"]], resize_keyboard=True, one_time_keyboard=False))
        return JP_VOCAB_ANS
    else:
        message += "failed, returning to the Notion menu"
        await update.message.reply_text(message)
        return NOTIONMENU

async def notion_jpvocab_ans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global curr
    vocab = vocab_dict[curr]
    vocabID = vocab["id"]
    properties   = vocab["properties"]
    vocabName    = properties["Name"]["title"][0]["text"]["content"]
    # vocabRevised = properties["Revised"]["date"]["start"]
    message = f"Vocab {curr+1} / {page_size} >>> {vocabName}"
    await update.message.reply_text(message, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=False))

    state_value = "ok" if update.message.text == "◯" else "redo"
    pages_to_update[vocabID] = state_value
    curr += 1

    if curr < page_size:
        return JP_VOCAB_ANS
    else:
        return JP_VOCAB_UPD


async def notion_jpvocab_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Practice Ended"
    await update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
    message = "Updating vocab database..."
    await update.message.reply_text(message)
    revised_value = datetime.now().strftime("%Y-%m-%d")
    successful_updates = 0
    for page_id, state_value in pages_to_update.items():
        payload = {
            "properties": {
                "State": {
                    "type": "select",
                    "select": { "name": state_value }
                },
                "Revised": {
                    "date": { "start": revised_value },
                    "type": "date"
                }
            }
        }
        success = notion_patch_updatepage(page_id = page_id, payload = payload)
        successful_updates += 1 if success else 0
    if successful_updates == page_size:
        message = "Update successful"
    elif successful_updates > 1:
        message = f"Update was partially successful, {successful_updates}/{page_size} notion pages were updated"
    else:
        message = "Update failed, no pages were updated"
    print(f"\n>> notion.py > notion_jpvocab_update > Updated {successful_updates}/{page_size} notion pages")
    await update.message.reply_text(message)
    message = "Returning to Notion menu..."
    await update.message.reply_text(message)
    return NOTIONMENU

# ---------------------------------------------------------------------------------------------------- #

def notion_post_querydatasource(data_source_id, payload):
    url = f"https://api.notion.com/v1/data_sources/{data_source_id}/query"
    pages = []    
    response = requests.post(url, json = payload, headers = notion_headers)
    if response:
        data = response.json()
        pages.extend(data.get("results", []))
        with open(json_folder_path + "/" + jpvocab_json, 'w') as file:
            json.dump(pages, file, indent=4)
        print("\n>> notion.py > notion_post_querydatasource > POST - Query Data Source > ok")
        return True
    else:
        print("\n>> notion.py > notion_post_querydatasource > POST - Query Data Source > failed")
        return False

def notion_patch_updatepage(page_id, payload):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    response = requests.patch(url, json = payload, headers = notion_headers)
    if response:
        print("\n>> notion.py > notion_patch_updatepage > PATCH - Update Page > ok")
        return True
    else:
        print("\n>> notion.py > notion_patch_updatepage > PATCH - Update Page > failed")
        return False
