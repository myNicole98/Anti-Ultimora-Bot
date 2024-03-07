from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import ForceReply, Update, MessageOriginChannel
from telegram.error import BadRequest
from comparator import *
from typing import cast
from scraper import *
import configparser
import threading
import time

# Config initialization
config = configparser.ConfigParser()
config.read('config.ini')

# Bot Token
token = config.get("Settings", "token")

# Messages from channel updater
def channel_timer(interval):
    global messages
    messages = []
    channels_str = config['Settings']['channels']
    channels_list = channels_str.split(', ')
    channel_index = 0
    while True:
        for element in channels_list:
            messages.insert(channel_index, channel_updater(channels_list[channel_index]))
            channel_index = channel_index + 1
        channel_index = 0
        time.sleep(interval)


# Start channels polling
channel_thread = threading.Thread(target = (channel_timer), args = (int(config.get("Settings", "updater")),))
channel_thread.start()

# Anti forward function
async def antiforward(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global messages

    # Get list of channels
    channels_str = config['Settings']['channels']
    channels_list = channels_str.split(', ')
    channel_index = 0

    # Get buffer
    count = int(config.get("Settings", "buffer"))

    try:
        # Get text message
        text1 = update.message.text
        if text1 == None:
            text1 = update.message.caption
        
        # Check if it's a forwarded message from origin
        if update.message.forward_origin.type == "channel":
            forward = cast(MessageOriginChannel, update.message.forward_origin)
            for channel in channels_list:
                if forward.chat.username == channel:
                    try:
                        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.id)
                        await context.bot.send_message(chat_id= update.effective_chat.id, text=f"Spam Ultimora rilevato, messaggio cancellato.")
                        pass
                    except BadRequest:
                        pass

        # Check if spamming tag or link
        for channel in channels_list:
            exclusion_elements = [f"@{channel}", f"t.me/{channel}", f"https://t.me.{channel}"]
            for element in exclusion_elements:
                if element in text1:
                    try:
                        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.id)
                        await context.bot.send_message(chat_id= update.effective_chat.id, text=f"Spam Ultimora rilevato, messaggio cancellato.")
                        pass
                    except BadRequest:
                        pass
        
        # Check if it's a forwarded message with cosine similarity
        for channel in channels_list:
            for i in range(count):
                text2 = channel_scraper(count, messages [channel_index])
                vector1 = text_to_vector(text1)
                vector2 = text_to_vector(text2)
                similarity = cosine_similarity(vector1, vector2)
                similarity_percentage = similarity * 100

                if similarity_percentage >= 70:
                    try:
                        await context.bot.delete_message(chat_id= update.effective_chat.id, message_id=update.effective_message.id)
                        await context.bot.send_message(chat_id= update.effective_chat.id, text=f"Spam Ultimora rilevato, messaggio cancellato.")
                    except BadRequest:
                        pass
                count -= 1
            channel_index += 1
            count = int(config.get("Settings", "buffer"))

        # Reset channel_index    
        channel_index = 0
    except AttributeError:
        pass
    except TypeError:
        pass
    except IndexError:
        pass

# Build Bot
application = Application.builder().token(token).build()

# Conversation handler
application.add_handler(MessageHandler(filters.ALL, antiforward))

# Start polling
application.run_polling(allowed_updates=Update.ALL_TYPES)