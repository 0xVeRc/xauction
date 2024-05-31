import logging
from telegram import Update, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import pandas as pd

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize auction data
auction_data = []
users_data = {}

# Constants
OWNER_USERNAME = '@ojjrr'

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.message.from_user
    if user.username not in users_data:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome! Please register by sending your name, phone number (with country code), and email.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome back! Type /products to see all auction products.")

def register(update: Update, context: CallbackContext) -> None:
    """Register a new user."""
    user = update.message.from_user
    text = update.message.text.split('\n')
    if len(text) == 3:
        users_data[user.username] = {
            'name': text[0],
            'phone': text[1],
            'email': text[2]
        }
        context.bot.send_message(chat_id=update.effective_chat.id, text="Registration successful! Type /products to see all auction products.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid format. Please send your name, phone number (with country code), and email in separate lines.")

def add_product(update: Update, context: CallbackContext) -> None:
    """Add a new product to the auction."""
    user = update.message.from_user
    if user.username == OWNER_USERNAME:
        if context.args and len(context.args) >= 2:
            product_name = context.args[0]
            starting_bid = float(context.args[1])
            photo = update.message.photo[-1] if update.message.photo else None
            auction_data.append({
                'product_name': product_name,
                'starting_bid': starting_bid,
                'current_bid': starting_bid,
                'current_bidder': None,
                'photo': photo
            })
            context.bot.send_message(chat_id=update.effective_chat.id, text="Product added successfully!")
            notify_users(context)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Usage: /add_product <product_name> <starting_bid>")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to add products.")

def notify_users(context: CallbackContext) -> None:
    """Notify all registered users about the new product."""
    for username in users_data:
        context.bot.send_message(chat_id=username, text="A new product is up for auction! Type /products to see details.")

def products(update: Update, context: CallbackContext) -> None:
    """Show all products currently on auction."""
    if auction_data:
        for product in auction_data:
            if product['photo']:
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=product['photo'].file_id, caption=f"{product['product_name']} - Current Bid: ${product['current_bid']}")
            else:
                context.bot.send_message(chat_id=update.
effective_chat.id, text=f"{product['product_name']} - Current Bid: ${product['current_bid']}")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="No products currently on auction.")

def bid(update: Update, context: CallbackContext) -> None:
    """Place a bid on a product."""
    user = update.message.from_user
    if user.username in users_data:
        if context.args and len(context.args) == 2:
            product_name = context.args[0]
            bid_amount = float(context.args[1])
            for product in auction_data:
                if product['product_name'] == product_name:
                    if bid_amount > product['current_bid']:
                        product['current_bid'] = bid_amount
                        product['current_bidder'] = user.username
                        context.bot.send_message(chat_id=update.effective_chat.id, text="Bid placed successfully!")
                        notify_users_about_bid(context, product)
                    else:
                        context.bot.send_message(chat_id=update.effective_chat.id, text="Bid amount must be higher than the current bid.")
                    return
            context.bot.send_message(chat_id=update.effective_chat.id, text="Product not found.")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Usage: /bid <product_name> <bid_amount>")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You must register first by sending your name, phone number, and email.")

def notify_users_about_bid(context: CallbackContext, product) -> None:
    """Notify all registered users about the new bid."""
    for username in users_data:
        context.bot.send_message(chat_id=username, text=f"{product['product_name']} - New Bid: ${product['current_bid']} by {product['current_bidder']}")

def main() -> None:
    """Start the bot."""
    updater = Updater("7318782651:AAHtdSnQyf0SPBD3GEPJ-vxBxOrdxUmjA44'", use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, register))
    dispatcher.add_handler(CommandHandler("add_product", add_product, Filters.user(username=OWNER_USERNAME)))
    dispatcher.add_handler(CommandHandler("products", products))
    dispatcher.add_handler(CommandHandler("bid", bid))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
