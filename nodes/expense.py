from utility.helper import *

# States
EXPMENU, EXPADD_TYP, EXPADD_AMT, EXPGET_TYP, EXPGET_DATE, EXPCLEAR = range(6)
reply_keyboard_type = [["食", "交通", "物"]]
reply_keyboard_confirm = [["⭕", "❌"]]

# -------------------------------------------------- #
#   Main node menu                                   #
# -------------------------------------------------- #

async def expense_node(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    print(f"\n>> expense.py > expense_node > User: {user["username"]}")
    name, username = user["first_name"], user["username"]
    if username == master:
        message = "\n".join(["Welcome to the expense node",
                            "/add - Add an expense",
                            "/view - View expenses",
                            "/cancel - Exit node"
                            ])
    else:
        message = f"Hey '{name}' you can't access this node!"
    await update.message.reply_text(message)
    return EXPMENU

# -------------------------------------------------- #
# Functions for adding expense                       #
# -------------------------------------------------- #

async def expense_add_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Adding expenses - Select type of expense"
    await update.message.reply_text(message, reply_markup = ReplyKeyboardMarkup(reply_keyboard_type, resize_keyboard = True, one_time_keyboard = False, input_field_placeholder = "Select type of expense"))
    return EXPADD_TYP

async def expense_add_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global exp_type
    exp_type = update.message.text

    message = "Enter expense amount(s), '+' separated"
    await update.message.reply_text(message, reply_markup = ReplyKeyboardRemove())
    return EXPADD_AMT

async def expense_add_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Updating expense log...\n"

    exp_amounts = update.message.text
    exp_date = date.today().strftime("%Y%m%d")

    success = expense_update(expense_date = exp_date, expense_type = exp_type, expense_amounts = exp_amounts)
    message += "ok" if success else "failed"
    await update.message.reply_text(message)
    return EXPMENU

def expense_update(expense_date: str, expense_type: str, expense_amounts: str):
    print(f"\n>> expense_node.py > expense_update")
    try:
        expense_path = check_file(file = expense_log, folder_path = data_path)
        
        # If provided input has multiple amounts
        if "+" in expense_amounts:
            expenses = expense_amounts.split("+")
            total_amount = 0
            for i in expenses:
                total_amount += float(i)
        else:
            total_amount = float(expense_amounts)
        total_amount = str(round(total_amount, 2))

        # Update .txt log
        with open(expense_path, "a") as log:
            log.write(f"{expense_date},{expense_type},{total_amount}\n")
            print(f"> Added expense: {expense_date},{expense_type},{total_amount}")

        ### TO CONVERT EXPENSE LOGGING FROM .txt TO .db
        # Update .db

        
        return True
    except Exception as e:
        print(f"> Error: {e}")
        return False

# -------------------------------------------------- #
# Functions for viewing expense                      #
# -------------------------------------------------- #

async def expense_view_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Viewing expenses - Select type of expense"
    await update.message.reply_text(message, reply_markup=ReplyKeyboardMarkup(reply_keyboard_type, resize_keyboard=True, one_time_keyboard=False, input_field_placeholder="Select type of expense"))
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
    result = expense_get(expense_type = exp_type, yearmonth = exp_yearmonth)
    message += result if result else "failed"
    await update.message.reply_text(message)
    return EXPMENU

def expense_get(expense_type: str, yearmonth: str):
    print("\n>> expense_node.py > expense_get")
    try:
        expense_sum = float()

        expense_path = check_file(file = expense_log, folder_path = data_path)
        with open(expense_path, "r") as log:
            expenses = log.readlines()
            for exp in expenses:
                e = exp.split(",")
                e_date, e_type, e_amount = e[0], e[1], e[2]
                if e_date[0:6] == yearmonth and e_type == expense_type:
                    expense_sum += float(e_amount)
        
        get_result = f"Total Amount = ${round(expense_sum, 2)}"
        print(f"> Retrieved {expense_type} expenses for {yearmonth}")
        return get_result
    except Exception as e:
        print(f"> Error: {e}")
        return False

# -------------------------------------------------- #
# Functions for clearing expense data                #
# -------------------------------------------------- #

async def expense_clear_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Clearing expense log - Are you sure?"
    await update.message.reply_text(message, reply_markup = ReplyKeyboardMarkup(reply_keyboard_confirm, resize_keyboard = True, one_time_keyboard = False, input_field_placeholder = "Confirm clearing expense log?"))
    return EXPCLEAR

async def expense_clear_execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    confirm = update.message.text

    if confirm == "⭕":
        message = "Clearing expense log..."
        success = expense_clear()
        message += "ok" if success else "failed"
    else:
        message = "Cancelled"
    
    return EXPMENU

def expense_clear():
    print("\n>> expense_node.py > expense_clear")
    try:
        expense_path = check_file(file = expense_log, folder_path = data_path)
        with open(expense_path, "w") as log:
            log.truncate(0)
        print(f"> Cleared {expense_path}")
        return True
    except Exception as e:
        print(f"> Error: {e}")
        return False