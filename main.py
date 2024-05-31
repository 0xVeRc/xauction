import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import pyTelegramBotAPI as botapi

load_dotenv()

app = Flask(__name__)

@app.route('/bot', methods=['POST'])
def handle_message():
    message = json.loads(request.data)['message']
    if not message.get('text'):
        return ''
    
    user_name = message['from']['username']
    
    # Check if the user is registered
    with open('registered_users.txt') as f:
        registered_users = set(line.strip() for line in f)
        
    if user_name not in registered_users:
        bot.send_message(chat_id=message['chat']['id'], text='Please register your account to bid!')
        return ''
    
    # Check the command
    if message.get('text').startswith('/start'):
        start_command(message)
    
    elif message.get('text').startswith('/bid '):
        bid_product(message)

def start_command(message):
    bot.send_message(chat_id=message['chat']['id'], text='Welcome to our auction market! You can see all products with the /show command.')
    # Add user to registered users list
    with open('registered_users.txt', 'a') as f:
        f.write(f'{message["from"]["username"]}\n')

def bid_product(message):
    product_id = int(message.get('text')[5:])
    
    # Check if the product exists and is still available for bidding
    products_data = {}
    with open('products.txt') as f:
        products = [line.strip().split(',') for line in f]
        
    if str(product_id) not in [product[0] for product in products]:
        bot.send_message(chat_id=message['chat']['id'], text='This product is no longer available.')
        return
    
    # Get the current bid price and update it
    current_bid = float([product[1] for product in products if str(product_id) == product[0]][0])
    
    new_bid = float(message.get('text')[6:])
    
    if new_bid > current_bid:
        with open('products.txt', 'w') as f:
            for i, line in enumerate(f):
                fields = line.strip().split(',')
                
                if str(product_id) == fields[0]:
                    f.write(f'{product_id},{new.bid}\n')
                    break
        
        bot.send_message(chat_id=message['chat']['id'], text=f'Your bid of {new_bid} has been accepted!')
    
    # Show all products that are still available for bidding
    show_all_products(message)

def show_all_products(message):
    with open('products.txt') as f:
        products = [line.strip().split(',') for line in f]
        
        bot.send_message(chat_id=message['chat']['id'], text='Current bids:')
        
        for product in products:
            if float(product[1]) > 0.0:  # Only show products that are still available
                bot.send_photo(message['chat']['id'], photo=open(f'images/{product[2]}', 'rb'))
                
                bid_message = f'{product_id} - {float(product[1]):.2f}'
            
            else:
                continue
        
        with open('registered_users.txt') as f:
            registered_usernames = set(line.strip() for line in f)
        
        bot.send_message(chat_id=message['chat']['id'], text='To place a bid, simply start typing the product ID and your desired price!')

if __name__ == '__main__':
    load_dotenv()
    
    with open('products.txt') as f:
        products = [line.strip().split(',') for line in f]
        
        registered_users = set(line.strip() for line in open('registered_users.txt'))
        
        # Initialize the bot
        TOKEN = os.environ.get("7318782651:AAHtdSnQyf0SPBD3GEPJ-vxBxOrdxUmjA44")
        bot_token = str(TOKEN)
    
    with open('bot.log', 'w') as log_file:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
        
            apihelper. set_stream_handler(log_file)
            
        my_bot = botapi.Bot(bot_token='7318782651:AAHtdSnQyf0SPBD3GEPJ-vxBxOrdxUmjA44')

    app.run(debug=True)
