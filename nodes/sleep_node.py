from utility.helper import *

# States
SLEEPMENU, SLEEPADD = range(2)

# ---------------------------------------------------------------------------------------------------- #

async def sleep_node(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    print(f"\n>> sleep_node.py > sleep_node > User: {user["username"]}")
    name = user["first_name"]
    username = user["username"]
    if username == master:
        message = "\n".join(["Welcome to the sleep node",
                            "/sleep_add - Add sleep timings",
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
    result = sleep_manager(command="get", subcommand="last", input=None)
    global next_date

    # Sleep log is empty
    if result == None:
        next_date = datetime.now().strftime("%Y%m%d")
        next_date = date.strptime(next_date, "%Y%m%d")
        message = "\n".join([f"Sleep log is empty",
                            f"Enter new sleep timings (24h format, ; separated) from: {next_date}"
                            ])
    # Sleep log not empty
    else:
        last_date = result
        next_date = last_date + timedelta(days=1)
        message = "\n".join([f"Last date in sleep log: {last_date}",
                            f"Enter new sleep timings (24h format, ; separated) from: {next_date}"
                            ])
    await update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
    return SLEEPADD

async def sleep_add_update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    new_times = update.message.text
    message = f"Updating sleep log from {next_date}...\n"
    success = sleep_manager("add", None, [next_date, new_times])
    message += "done" if success else "failed"
    await update.message.reply_text(message)
    return SLEEPMENU

async def sleep_view(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = "Fetching all sleep timings...\n"
    sleep_log = sleep_manager(command="get", subcommand="all", input=None)
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
            # Split the input string into a list, using ; as the delimiter
            curr_date = input[0]
            times = input[1].split(";")

            with open(log_path, "a") as log:
                for new_time in times:
                    log.write(f"{curr_date},{new_time}\n")
                    curr_date += timedelta(days=1)
            print(f"\n>> sleep_node.py > sleep_manager \n> Updated {log_path}")
            return True
        
        elif command == "get":
            # Check if file is empty
            if os.path.getsize(log_path) == 0:
                print("\n>> sleep_node.py > sleep_manager \n> Log file is empty")
            else:
                with open(log_path, "r") as log:
                    # Return the last date in sleep log
                    if subcommand == "last":
                        last_date = log.readlines()[-1].split(":")[0]
                        y, m, d = int(last_date[0:4]), int(last_date[5:7]), int(last_date[8:10])
                        last_date = date(y, m, d)
                        return last_date
                    elif subcommand == "all":
                        result = []
                        i = 0
                        log = log.readlines()
                        log_size = len(log)
                        for line in log:
                            date_str, time_str = line.split(",")
                            if i == 0:
                                date_start = date_str
                            # If to retrieve last 10 records
                            # elif log_size - i <= 10:
                                # result.append(f"{time_str[0:2]}:{time_str[2:4]}")
                            result.append(f"{time_str[0:2]}:{time_str[2:4]}")
                            i += 1
                        date_end = date_str
                        result.insert(0, f"Found {log_size} records from {date_start} > {date_end}")
                        return "\n".join(result)

        elif command == "clear":
            with open(log_path, "w") as log:
                log.truncate(0)
            print(f"\n>> sleep_node.py > sleep_manager \n> Cleared {log_path}")
            return True
    except Exception as e:
        print(f"\n>> sleep_node.py > sleep_manager \n> Error: {e}")
        return False