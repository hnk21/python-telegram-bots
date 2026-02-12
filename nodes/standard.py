from utility.variables import *

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    print(f"\n>> standard.py > start > User: {user["username"]}")
    name = user["first_name"]
    username = user["username"]
    if username == master:
        message = "\n".join(["おかえり、ポチタ。",
                            get_time(),
                            "Enter a command via the menu or /help."
                            ])
    else:
        message = "\n".join([f"Welcome, {name}",
                            "Enter a command via the menu or /help."])
    await update.message.reply_text(message)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "/news | /sleep | /expense"
    await update.message.reply_text(message)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    name = user["first_name"]
    user_message = update.message.text
    message = f"Yo {name}, I did not understand '{user_message}'"
    await update.message.reply_text(message)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Exited current node.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# ---------------------------------------------------------------------------------------------------- #

def get_time():
    dt_now = datetime.now()
    curr_datetime = dt_now.strftime("%Y-%m-%d（%A）%H:%M")
    dt_end_today = dt_now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    sec_left = (dt_end_today - dt_now).total_seconds()
    
    hours_left, sec_remain = divmod(sec_left, 3600)
    mins_left, sec = divmod(sec_remain, 60)
    time_left = f"{int(hours_left)} 時間 {int(mins_left)} 分"

    # Convert weekdays from English to Japanese
    weekday = dt_now.strftime("%A")
    youbi = weekdays_en_jp[weekday]
    curr_datetime = curr_datetime.replace(weekday, youbi)

    # Get day number of current year
    dt_start = datetime(dt_now.year, 1, 1)
    days_elapsed = (dt_now - dt_start).days
    days_left = 365 - days_elapsed

    message = f"「{curr_datetime}・Day #{days_elapsed+1}」\n今年の終わり後{days_left}日\n今日の終わり後{time_left}"
    return message

# ---------------------------------------------------------------------------------------------------- #