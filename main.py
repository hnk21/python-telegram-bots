from utility.helper import *
from nodes.standard import *
from nodes.sleep_node import *
from nodes.news_node import *
from nodes.expense_node import *

def main(api_token):
    application = Application.builder().token(api_token).concurrent_updates(True).read_timeout(30).write_timeout(30).build()

    ### sleep handler ###
    sleep_node_handler = ConversationHandler(
        entry_points = [CommandHandler("sleep", sleep_node)],
        states = {SLEEPMENU: [MessageHandler(filters.Regex("^/sleep_add$"), sleep_add),
                              MessageHandler(filters.Regex("^/sleep_view$"), sleep_view),
                              MessageHandler(filters.Regex("^/sleep_clear$"), sleep_clear)],
                  SLEEPADD:  [MessageHandler(filters.Regex("^(?:(?:[0-1][0-9]|2[0-3])[0-5][0-9])(?:;(?:[0-1][0-9]|2[0-3])[0-5][0-9])*$"), sleep_add_update)]
                  },
        fallbacks = [CommandHandler("cancel", cancel)] )
    application.add_handler(sleep_node_handler)

    ### news handler ###
    news_node_handler = ConversationHandler(
        entry_points = [CommandHandler("news", news_node)],
        states = {NEWSMENU: [MessageHandler(filters.Regex("^/news_cna$"), news_cna),
                             MessageHandler(filters.Regex("^/news_gn$"), news_gn),
                             MessageHandler(filters.Regex("^/news_nhk$"), news_nhk)
                             ],
                  CNA: [MessageHandler(filters.Regex("^(Asia|Business|East Asia|World)$"), show_cna)],
                  GRND: [MessageHandler(filters.Regex("^(Stock Markets|Tech|Asia|North America)$"), show_gn)],
                  NHK: [MessageHandler(filters.Regex("^(経済|社会|政治|国際)$"), show_nhk)]
                  },
        fallbacks = [CommandHandler("cancel", cancel)] )
    application.add_handler(news_node_handler)

    ### expense handler ###
    expense_node_handler = ConversationHandler(
        entry_points = [CommandHandler("expense", expense_node)],
        states = {EXPMENU: [MessageHandler(filters.Regex("^/expense_add$"), expense_add_type),
                            MessageHandler(filters.Regex("^/expense_view$"), expense_view_type),
                            MessageHandler(filters.Regex("^/expense_clear$"), expense_clear)
                            ],
                  EXPADD_TYP:  [MessageHandler(filters.Regex("^(Food|Stuff)$"), expense_add_amount)],
                  EXPADD_AMT:  [MessageHandler(filters.Regex("^\\d+(\\.\\d{1,2})?(\\+\\d+(\\.\\d{1,2})?)*$"), expense_add_update)],
                  EXPGET_TYP:  [MessageHandler(filters.Regex("^(Food|Stuff)$"), expense_view_date)],
                  EXPGET_DATE: [MessageHandler(filters.Regex("^[0-9]{6}$"), expense_view_get)]
                  },
        fallbacks = [CommandHandler("cancel", cancel)] )
    application.add_handler(expense_node_handler)

    ### Handlers for standard and unknown commands ###
    application.add_handlers([CommandHandler("start", start),
                              CommandHandler("help", help),
                              CommandHandler("cancel", cancel),
                              MessageHandler(filters.TEXT & (~filters.COMMAND), echo)])

    print("\n>> main.py > hnk_pinboard bot ONLINE.")
    application.run_polling()

# -------------------------------------------------- #
# Run telegram bot                                   #
# -------------------------------------------------- #

if __name__ == '__main__':
    main(telegram_token)
    print("\n>> main.py > hnk_pinboard bot OFFLINE.")
else:
    print("\n>> main.py > Failed to start hnk_pinboard bot.")