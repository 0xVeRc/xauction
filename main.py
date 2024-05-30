from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Define the command handler function
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! Welcome to your simple Telegram bot.')

def main():
    # Your bot's API token
    api_token = '7251892423:AAFsZdxT5iN6nHSzfQinr1VNhutxLvx8VrM'

    # Create the Updater and pass it your bot's token
    updater = Updater(api_token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register the /start command handler
    dispatcher.add_handler(CommandHandler("start", start))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
