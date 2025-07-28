from DjangoAPI.settings import ID, HASH
from telethon.sync import TelegramClient, events

api_id = ID
api_hash = HASH
session_name = 'auto_reply_session'
client = TelegramClient(session_name, api_id, api_hash)


@client.on(events.NewMessage(incoming=True))
async def handler(event):
    sender = await event.get_sender()
    sender_id = sender.id
    if sender_id == 7290106595:
        await event.respond('salom dostim')
        return
    if sender.bot:
        return  # Botlardan kelgan habarlarni javobsiz qoldiramiz
    # Avtojavob
    await event.reply("Salom! Men hozir bandman, sizga keyinroq javob beraman.")


with client:
    print("Bot ishga tushdi!")
    client.run_until_disconnected()
#
#
# async def main():
#     # Bu userga bot ishga tushgan zahoti habar yuboriladi
#     await client.send_message(7290106595, '✅ Bot ishga tushdi! Salom!')
#
# with client:
#     print("📡 Bot ishga tushdi!")
#     client.loop.run_until_complete(main())
