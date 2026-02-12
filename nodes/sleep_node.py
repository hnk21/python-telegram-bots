from utility.variables import *

## States
SLEEPMENU, SLEEPADD = range(2)

# ---------------------------------------------------------------------------------------------------- #

async def sleep_node(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    print(f"\n>> sleep_node.py > sleep_node > User: {user["username"]}")
    name = user["first_name"]
    username = user["username"]
    if username == master:
        message = "\n".join(["Welcome to the sleep node",
                            "/sleep_add - Add sleep timing",
                            "/sleep_view - View sleep log",
                            "/cancel - Exit node",
                            "Use command 'sleep_clear' to clear log"
                            ])
    else:
        message = f"Hey {name} you can't access this node!"
    await update.message.reply_text(message)
    return SLEEPMENU

# ---------------------------------------------------------------------------------------------------- #

async def sleep_add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    result = sleep_manager(command="get", subcommand="latest", input=None)
    global next_date
    # Sleep log is empty
    if result == None:
        next_date = datetime.now().strftime("%Y-%m-%d")
        message = "\n".join([f"Sleep log is empty",
                            f"Enter new sleep timing (hhmm) for: {next_date}"
                            ])
    # Sleep log not empty
    else:
        last_date = result
        next_date = last_date + timedelta(days=1)
        message = "\n".join([f"Last date in sleep log: {last_date}",
                            f"Enter new sleep timing (hhmm) for: {next_date}"
                            ])
    await update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
    return SLEEPADD

async def sleep_add_update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    new_time = update.message.text
    message = f"Updating sleep log for {next_date}...\n"
    success = sleep_manager("add", None, [next_date, new_time])
    if success:
        message += "done"
    else:
        message += "failed"
    await update.message.reply_text(message)
    return SLEEPMENU

async def sleep_view(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = "Getting the 10 most recent sleep timings...\n"
    sleep_log = sleep_manager(command="get", subcommand="recent", input=None)
    if sleep_log:
        message += sleep_log
    elif sleep_log == None:
        message += "Sleep log is empty"
    else:
        message += "failed"
    await update.message.reply_text(message)
    return SLEEPMENU

async def sleep_clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = "Clearing sleep log...\n"
    success = sleep_manager(command="clear", subcommand=None, input=None)
    if success:
        message += "done"
    else:
        message += "failed"
    await update.message.reply_text(message)
    return SLEEPMENU

# ---------------------------------------------------------------------------------------------------- #

def sleep_manager(command: str, subcommand: str, input: str):
    try:
        log_path = check_file(file=sleep_log, folder_path=data_path)
        
        if command == "add":
            with open(log_path, "a") as log:
                log.write(f"{input[0]}:{input[1]}\n")
            print(f"\n>> sleep_node.py > sleep_manager \n> Updated {log_path}")
            return True
        
        elif command == "get":
            # Check if file is empty
            if os.path.getsize(log_path) == 0:
                print("\n>> sleep_node.py > sleep_manager \n> Log file is empty")
            else:
                with open(log_path, "r") as log:
                    # Return latest date in sleep log
                    if subcommand == "latest":
                        last_date = log.readlines()[-1].split(":")[0]
                        y, m, d = int(last_date[0:4]), int(last_date[5:7]), int(last_date[8:10])
                        last_date = date(y, m, d)
                        return last_date
                    # Return last 10 records in sleep log
                    elif subcommand == "recent":
                        result = []
                        i = 0
                        log = log.readlines()
                        log_size = len(log)
                        for line in log:
                            date_str, time_str = line.split(":")
                            if i == 0:
                                date_start = date_str
                            elif log_size - i <= 10:
                                result.append(f"{time_str[0:2]}:{time_str[2:4]}")
                            i += 1
                        date_end = date_str
                        result.insert(0, f"Found {log_size} records from {date_start} > {date_end}")
                        # result.insert(1, f"Showing records from {date_start} > {date_end}")
                        return "\n".join(result)

        elif command == "clear":
            with open(log_path, "w") as log:
                log.truncate(0)
            print(f"\n>> sleep_node.py > sleep_manager \n> Cleared {log_path}")
            return True
    except Exception as e:
        print(f"\n>> sleep_node.py > sleep_manager \n> Error: {e}")
        return False

# ---------------------------------------------------------------------------------------------------- #