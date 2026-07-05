import os
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
import database
import handlers
from config import BOT_TOKEN

def main():
    # Enforce safe localized asynchronous event contexts to systematically construct data architecture maps on boot running loops
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(database.init_db())

    if not BOT_TOKEN:
        print("Fatal error: Missing BOT_TOKEN structural deployment parameters variables mapping data values tracking strings.")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    generation_wizard = ConversationHandler(
        entry_points=[CallbackQueryHandler(handlers.start_convo_flow, pattern="^nav_create_place$")],
        states={
            handlers.DIMENSIONS_STAGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_dimensions_input),
                CallbackQueryHandler(handlers.handle_dimensions_input, pattern="^sz_")
            ],
            handlers.COLOR_STAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_color_input)],
            handlers.TEXT_STAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_text_and_compile)]
        },
        fallbacks=[CommandHandler("start", handlers.start)]
    )

    app.add_handler(CommandHandler("start", handlers.start))
    app.add_handler(CallbackQueryHandler(handlers.menu_navigation_routing, pattern="^nav_"))
    app.add_handler(generation_wizard)

    print("PlaceGen Core Production Workers Activated & Polling live loop records...")
    app.run_polling()

if __name__ == '__main__':
    main()

