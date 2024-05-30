from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

# Your bot token
BOT_TOKEN = '7318782651:AAHtdSnQyf0SPBD3GEPJ-vxBxOrdxUmjA44'

# Items for sale
items = [
    {"name": "Item 1", "price": 10.0, "description": "Description of Item 1"},
    {"name": "Item 2", "price": 20.0, "description": "Description of Item 2"},
    # Add more items here
]

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to our shop! Use /list to see items for sale.')

def list_items(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton(item["name"], callback_data=str(index))] 
        for index, item in enumerate(items)
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Here are the items for sale:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    item = items[int(query.data)]
    text = f"{item['name']}\nPrice: ${item['price']}\nDescription: {item['description']}"
    query.edit_message_text(text=text)

def main() -> None:
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("list", list_items))
    dispatcher.add_handler(CallbackQueryHandler(button))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
