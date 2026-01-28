from utility.variables import *

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "\n".join(["おかえり、ポチタ。",
                         get_time(),
                          "Enter a command via the menu or /help."
                         ])  
    await update.message.reply_text(message)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "| /news | /sleep | /expense |"
    await update.message.reply_text(message)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    message = f"Did not understand '{user_message}'"
    await update.message.reply_text(message)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Exited current node.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# ---------------------------------------------------------------------------------------------------- #

def get_time():
    dt_now = datetime.now()
    curr_datetime = dt_now.strftime("%Y-%m-%d・%A・%H:%M")
    dt_end_today = dt_now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    sec_left = (dt_end_today - dt_now).total_seconds()
    
    hours_left, sec_remain = divmod(sec_left, 3600)
    mins_left, sec = divmod(sec_remain, 60)
    time_left = f"{int(hours_left)} 時間 {int(mins_left)} 分"

    # Convert weekdays from English to Japanese
    weekday = dt_now.strftime("%A")
    youbi = weekdays_en_jp[weekday]
    curr_datetime = curr_datetime.replace(weekday, youbi)

    message = f"「{curr_datetime}」\n今日を終わるまであと「{time_left}」"
    return message

# ---------------------------------------------------------------------------------------------------- #