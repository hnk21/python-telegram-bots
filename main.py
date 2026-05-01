from utility.helper import *
from nodes.standard import *
from nodes.sleep_node import *
from nodes.news_node import *
from nodes.expense_node import *
from nodes.notion import *

def main(api_token):
    application = Application.builder().token(api_token).concurrent_updates(True).read_timeout(30).write_timeout(30).build()

    ### sleep handler ###
    sleep_node_handler = ConversationHandler(
        entry_points = [CommandHandler("sleep", sleep_node)],
        states = {SLEEPMENU: [CommandHandler("sleep_add", sleep_add),
                              CommandHandler("sleep_view", sleep_view),
                              CommandHandler("sleep_clear", sleep_clear)],
                  SLEEPADD:  [MessageHandler(filters.Regex("^(?:(?:[0-1][0-9]|2[0-3])[0-5][0-9])(?:;(?:[0-1][0-9]|2[0-3])[0-5][0-9])*$"), sleep_add_update)]
                  },
        fallbacks = [CommandHandler("cancel", cancel)]
    )
    application.add_handler(sleep_node_handler)

    ### news handler ###
    news_node_handler = ConversationHandler(
        entry_points = [CommandHandler("news", news_node)],
        states = {NEWSMENU: [CommandHandler("news_cna", news_cna),
                             CommandHandler("news_gn", news_gn),
                             CommandHandler("news_nhk", news_nhk)
                             ],
                  CNA: [MessageHandler(filters.Regex("^(Asia|Business|East Asia|World)$"), show_cna)],
                  GRND: [MessageHandler(filters.Regex("^(Stock Markets|Tech|Asia|North America)$"), show_gn)],
                  NHK: [MessageHandler(filters.Regex("^(経済|社会|政治|国際)$"), show_nhk)]
                  },
        fallbacks = [CommandHandler("cancel", cancel)]
    )
    application.add_handler(news_node_handler)

    ### expense handler ###
    expense_node_handler = ConversationHandler(
        entry_points = [CommandHandler("expense", expense_node)],
        states = {EXPMENU: [CommandHandler("expense_add", expense_add_type),
                            CommandHandler("expense_view", expense_view_type),
                            CommandHandler("expense_clear", expense_clear)
                            ],
                  EXPADD_TYP:  [MessageHandler(filters.Regex("^(Food|Stuff)$"), expense_add_amount)],
                  EXPADD_AMT:  [MessageHandler(filters.Regex("^\\d+(\\.\\d{1,2})?(\\+\\d+(\\.\\d{1,2})?)*$"), expense_add_update)],
                  EXPGET_TYP:  [MessageHandler(filters.Regex("^(Food|Stuff)$"), expense_view_date)],
                  EXPGET_DATE: [MessageHandler(filters.Regex("^[0-9]{6}$"), expense_view_get)]
                  },
        fallbacks = [CommandHandler("cancel", cancel)]
    )
    application.add_handler(expense_node_handler)

    ### notion handler ###
    notion_node_handler = ConversationHandler(
        entry_points = [CommandHandler("notion", notion_node)],
        states  = {NOTIONMENU: [CommandHandler("notion_jp_vocab", notion_jpvocab)
                                # MessageHandler(filters.Regex("^/notion_jp_vocab$"), notion_jpvocab)
                                # MessageHandler(filters.Regex("^/notion_$"), notion_function),
                                # MessageHandler(filters.Regex("^/notion_$"), notion_function)
                                ],
                   JP_VOCAB_GET: [MessageHandler(filters.Regex("^([1-9]|[12][0-9]|30)$"), notion_jpvocab_get)],
                   JP_VOCAB_ANS: [MessageHandler(filters.Regex("^(Start|◯|☓)$"), notion_jpvocab_ans)],
                   JP_VOCAB_UPD: [MessageHandler(filters.Regex("^(◯|☓)$"), notion_jpvocab_update)]

                #    NOTIONSTATE: [MessageHandler(filters.Regex("^/notion_$"), notion_function)],
                   },
        fallbacks = [CommandHandler("cancel", cancel)]
    )
    application.add_handler(notion_node_handler)

    ### ... handler ###

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
    print("\n>> main.py > Failed to start hnk_pinboard telegram bot.")