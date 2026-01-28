from utility.variables import *
from utility.directory import check_file

## States
EXPMENU, EXPADD_TYP, EXPADD_AMT, EXPGET_TYP, EXPGET_DATE = range(5)
reply_keyboard = [["Food", "Stuff"]]

# ---------------------------------------------------------------------------------------------------- #

async def expense_node(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "\n".join(["Welcome to the expense node",
                         "/expense_add - Add an expense",
                         "/expense_view - View expenses",
                         "/cancel - Exit node",
                         "Use command 'expense_clear' to clear log"
                         ])
    await update.message.reply_text(message)
    return EXPMENU

# ---------------------------------------------------------------------------------------------------- #

async def expense_add_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Adding new expense\nSelect the type of expense"
    await update.message.reply_text(message, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=False, input_field_placeholder="Select expense type."))
    return EXPADD_TYP

async def expense_add_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global exp_type
    exp_type = update.message.text
    message = "Enter the expense amount"
    await update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
    return EXPADD_AMT

async def expense_add_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    exp_amount = update.message.text
    exp_date = date.today().strftime("%Y%m%d")
    message = "Updating expense log..."
    success = expense_update(expense_date=exp_date, expense_type=exp_type, expense_amount=exp_amount)
    if success:
        message += "done"
    else:
        message += "failed"
    await update.message.reply_text(message)
    return EXPMENU

# ---------------------------------------------------------------------------------------------------- #

async def expense_view_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Viewing expenses\nSelect the type of expense"
    await update.message.reply_text(message, reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=False, input_field_placeholder="Select expense type."))
    return EXPGET_TYP

async def expense_view_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global exp_type
    exp_type = update.message.text
    message = "Enter the year and month (yyyymm)"
    await update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
    return EXPGET_DATE

async def expense_view_get(update: Update, context: ContextTypes.DEFAULT_TYPE):
    exp_yearmonth = update.message.text
    message = f"Retrieving {exp_type} expenses for {exp_yearmonth}...\n"
    result = expense_get(expense_type=exp_type, yearmonth=exp_yearmonth)
    if result:
        message += result
    else:
        message += "failed"
    await update.message.reply_text(message)
    return EXPMENU

# ---------------------------------------------------------------------------------------------------- #

async def expense_clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Clearing expense log...\n"
    success = expense_reset()
    if success:
        message += "done"
    else:
        message += "failed"
    await update.message.reply_text(message)
    return EXPMENU

# ---------------------------------------------------------------------------------------------------- #

def expense_update(expense_date: str, expense_type: str, expense_amount: float):
    print(">> expense_node.py > expense_update")
    try:
        log_path = check_file(file=expense_log, path=data_path)
        with open(log_path, "a") as log:
            log.write(f"{expense_date},{expense_type},{expense_amount}\n")
            print(f"> Added expense: {expense_date},{expense_type},{expense_amount}")
        return True
    except Exception as e:
        print(f"> Error: {e}")
        return False

def expense_get(expense_type: str, yearmonth: str):
    print(">> expense_node.py > expense_get")
    try:
        expense_sum = float()
        log_path = check_file(file=expense_log, path=data_path)
        with open(log_path, "r") as log:
            expenses = log.readlines()
            for exp in expenses:
                e = exp.split(",")
                e_date, e_type, e_amount = e[0], e[1], e[2]
                if e_date[0:6] == yearmonth and e_type == expense_type:
                    expense_sum += float(e_amount)
        get_result = f"Total amount: ${expense_sum}"
        print("> Retrieved expenses.")
        return get_result
    except Exception as e:
        print(f"> Error: {e}")
        return False

def expense_reset():
    print(">> expense_node.py > expense_reset")
    try:
        log_path = check_file(file=expense_log, path=data_path)
        with open(log_path, "w") as log:
            log.truncate(0)
        print(f"> Cleared {log_path}")
        return True
    except Exception as e:
        print(f"> Error: {e}")
        return False

# ---------------------------------------------------------------------------------------------------- #