import asyncio
from telethon import TelegramClient, events


TELEGRAM_API_ID = 20433582
TELEGRAM_API_HASH = "8e59bb9c4db5a6c5ed2eaee3bfcc12ba"
COMBINATIONS = {
    -1001935223749: [-1001965407801]
}

client = TelegramClient('session', api_id=TELEGRAM_API_ID, api_hash=TELEGRAM_API_HASH)

def remove_forward_tag(text):
    # Remove the forward tag (owner tag) from the message text
    if text.startswith('🔄'):
        return text.split('\n', 1)[1]  # Remove the first line (forward tag)
    return text

@client.on(events.NewMessage)
async def handle_new_message(event):
    sender_chat_id = event.sender_id
    if sender_chat_id in list(COMBINATIONS.keys()):
        destination_chat_ids = COMBINATIONS.get(sender_chat_id, [])
        await asyncio.gather(*[process_message(event, chat_id) for chat_id in destination_chat_ids])

async def process_message(event, chat_id):
    if event.media:
        # Handle media messages (videos, files, gifs, etc.)
        text_without_forward_tag = remove_forward_tag(event.message.text)
        if event.photo:
            # If it's a photo, use send_file instead of forward
            await client.send_file(chat_id, event.message.photo, caption=text_without_forward_tag)
        else:
            # For other media types, use send_message with text
            await client.send_message(chat_id, text_without_forward_tag, file=event.message.media)
    else:
        # Handle text messages and remove forward tag
        text_without_forward_tag = remove_forward_tag(event.raw_text)
        await client.send_message(chat_id, text_without_forward_tag)

client.start()
client.run_until_disconnected()
