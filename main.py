from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import logging
import random

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Your bot token
BOT_TOKEN = '7318782651:AAHtdSnQyf0SPBD3GEPJ-vxBxOrdxUmjA44'

# Items for auction
auction_items = [
    {"name": "Item 1", "start_price": 10.0, "description": "Description of Item 1", "highest_bid": 10.0, "highest_bidder": None, "photo": "https://example.com/photo1.jpg"},
    {"name": "Item 2", "start_price": 20.0, "description": "Description of Item 2", "highest_bid": 20.0, "highest_bidder": None, "photo": "https://example.com/photo2.jpg"},
    # Add more items here
]

# Registered users
registered_users = {}

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to the auction! Please register with /register <name> <phone_number_with_country_code> <email> to start bidding.')

def register(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    message = update.message.text.split()
    
    if len(message) < 4:
        update.message.reply_text('Usage: /register <name> <phone_number_with_country_code> <email>')
        return

    name = message[1]
    phone_number = message[2]
    email = message[3]

    registered_users[user.id] = {
        "name": name,
        "phone_number": phone_number,
        "email": email
    }

    update.message.reply_text(f'Registration successful! Welcome, {name}.')

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
    
    media = InputMediaPhoto(media=item['photo'], caption=text)
    query.edit_message_media(media=media)

def bid(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    if user.id not in registered_users:
        update.message.reply_text('You must register first using /register <name> <phone_number_with_country_code> <email>')
        return

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
