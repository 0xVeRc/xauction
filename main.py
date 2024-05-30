from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Your bot token
BOT_TOKEN = '7318782651:AAHtdSnQyf0SPBD3GEPJ-vxBxOrdxUmjA44'

# Items for auction
auction_items = [
    {"name": "Item 1", "start_price": 10.0, "description": "Description of Item 1", "highest_bid": 10.0, "highest_bidder": None},
    {"name": "Item 2", "start_price": 20.0, "description": "Description of Item 2", "highest_bid": 20.0, "highest_bidder": None},
    # Add more items here
]

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to the auction! Use /list to see items for auction.')

def list_items(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton(item["name"], callback_data=str(index))] 
        for index, item in enumerate(auction_items)
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Here are the items for auction:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    item = auction_items[int(query.data)]
    text = (f"{item['name']}\n"
            f"Starting Price: ${item['start_price']}\n"
            f"Description: {item['description']}\n"
            f"Highest Bid: ${item['highest_bid']}\n"
            f"Highest Bidder: {item['highest_bidder'] if item['highest_bidder'] else 'None'}")
    query.edit_message_text(text=text)

def bid(update: Update, context: CallbackContext) -> None:
    message = update.message.text.split()
    if len(message) < 3:
        update.message.reply_text('Usage: /bid <item_number> <amount>')
        return
    
    try:
        item_number = int(message[1])
        bid_amount = float(message[2])
    except ValueError:
        update.message.reply_text('Invalid item number or bid amount.')
        return
    
    if item_number < 0 or item_number >= len(auction_items):
        update.message.reply_text('Invalid item number.')
        return
    
    item = auction_items[item_number]
    if bid_amount <= item['highest_bid']:
        update.message.reply_text(f'Your bid must be higher than the current highest bid of ${item["highest_bid"]}.')
        return
    
    item['highest_bid'] = bid_amount
    item['highest_bidder'] = update.message.from_user.username
    update.message.reply_text(f'Your bid of ${bid_amount} for {item["name"]} has been placed.')

def main() -> None:
    """Start the bot."""
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    # Handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("list", list_items))
    dispatcher.add_handler(CommandHandler("bid", bid))
    dispatcher.add_handler(CallbackQueryHandler(button))
    
    # Start polling for updates from Telegram
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
