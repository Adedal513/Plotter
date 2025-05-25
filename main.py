from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ConversationHandler
from bot.handlers import start_handler, handle_csv, option_handler, column_input_handler
from config import TELEGRAM_TOKEN
from telegram.ext import PicklePersistence  # для хранения состояний, если нужно

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(MessageHandler(filters.Document.MimeType("text/csv"), handle_csv))

    conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(option_handler)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, column_input_handler)],
        },
        fallbacks=[],
    )

    app.add_handler(conv)

    app.run_polling()

if __name__ == "__main__":
    main()
