from utility.helper import *

# States
EXPMENU, EXPADD_TYP, EXPADD_AMT, EXPGET_TYP, EXPGET_DATE = range(5)
reply_keyboard = [["Food", "Stuff"]]

# ---------------------------------------------------------------------------------------------------- #

async def expense_node(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    print(f"\n>> expense_node.py > expense_node > User: {user["username"]}")
    name = user["first_name"]
    username = user["username"]
    if username == master:
        message = "\n".join(["Welcome to the expense node",
                            "/expense_add - Add an expense",
                            "/expense_view - View expenses",
                            "/cancel - Exit node",
                            "Use command 'expense_clear' to clear log"
                            ])
    else:
        message = f"Hey {name} you can't access this node!"
    await update.message.reply_text(message)
    return EXPMENU

# ---------------------------------------------------------------------------------------------------- #

async def expense_add_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Adding expenses - Select type of expense"
    await update.message.reply_text(message, reply_markup=ReplyKeyboardMarkup(reply_keyboard, 
                                                                              resize_keyboard=True, 
                                                                              one_time_keyboard=False, 
                                                                              input_field_placeholder="Select type of expense"))
    return EXPADD_TYP

async def expense_add_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Enter expense amount(s), multiple amounts must be separated with a '+'"
    global exp_type
    exp_type = update.message.text
    await update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
    return EXPADD_AMT

async def expense_add_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Updating expense log...\n"
    exp_amounts = update.message.text
    exp_date = date.today().strftime("%Y%m%d")
    success = expense_update(expense_date=exp_date, expense_type=exp_type, expense_amounts=exp_amounts)
    message += "done" if success else "failed"
    await update.message.reply_text(message)
    return EXPMENU

def expense_update(expense_date: str, expense_type: str, expense_amounts: str):
    try:
        expense_log_path = check_file(file=expense_log, folder_path=data_path)
        
        # Check if provided input has multiple amounts
        if "+" in expense_amounts:
            expenses = expense_amounts.split("+")
            total_amount = 0
            for i in expenses:
                total_amount += float(i)
        else:
            total_amount = float(expense_amounts)
        total_amount = str(round(total_amount, 2))

        with open(expense_log_path, "a") as log:
            log.write(f"{expense_date},{expense_type},{total_amount}\n")
            print(f"\n>> expense_node.py > expense_update \n> Added expense: {expense_date},{expense_type},{total_amount}")
        
        return True
    except Exception as e:
        print(f"\n>> expense_node.py > expense_update \n> Error: {e}")
        return False

# ---------------------------------------------------------------------------------------------------- #

async def expense_view_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Viewing expenses - Select type of expense"
    await update.message.reply_text(message, reply_markup=ReplyKeyboardMarkup(reply_keyboard, 
                                                                              resize_keyboard=True, 
                                                                              one_time_keyboard=False, 
                                                                              input_field_placeholder="Select type of expense"))
    return EXPGET_TYP

async def expense_view_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Enter the year and month (yyyymm)"
    global exp_type
    exp_type = update.message.text
    await update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
    return EXPGET_DATE

async def expense_view_get(update: Update, context: ContextTypes.DEFAULT_TYPE):
    exp_yearmonth = update.message.text
    message = f"Retrieving {exp_type} expenses for {exp_yearmonth}...\n"
    result = expense_get(expense_type=exp_type, yearmonth=exp_yearmonth)
    message += result if result else "failed"
    await update.message.reply_text(message)
    return EXPMENU

def expense_get(expense_type: str, yearmonth: str):
    try:
        expense_sum = float()

        log_path = check_file(file=expense_log, folder_path=data_path)
        with open(log_path, "r") as log:
            expenses = log.readlines()
            for exp in expenses:
                e = exp.split(",")
                e_date, e_type, e_amount = e[0], e[1], e[2]
                if e_date[0:6] == yearmonth and e_type == expense_type:
                    expense_sum += float(e_amount)
        
        get_result = f"Total Amount: ${round(expense_sum, 2)}"
        print("\n>> expense_node.py > expense_get \n> Retrieved expenses.")
        return get_result
    except Exception as e:
        print(f"\n>> expense_node.py > expense_get \n> Error: {e}")
        return False

# ---------------------------------------------------------------------------------------------------- #

async def expense_clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Clearing expense log...\n"
    success = expense_reset()
    message += "done" if success else "failed"
    await update.message.reply_text(message)
    return EXPMENU

def expense_reset():
    try:
        log_path = check_file(file=expense_log, folder_path=data_path)
        with open(log_path, "w") as log:
            log.truncate(0)
        print(f"\n>> expense_node.py > expense_reset \n> Cleared {log_path}")
        return True
    except Exception as e:
        print(f"\n>> expense_node.py > expense_reset \n> Error: {e}")
        return False