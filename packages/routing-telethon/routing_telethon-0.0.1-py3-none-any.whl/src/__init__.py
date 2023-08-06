from .bot import Bot
# from telethon import TelegramClient
#
# from bot_framework import bot_logging
# from .events.register import register_all
# from .mapper import FunctionsMapper
#
#
# async def run_bot(api_id, api_hash, bot_token, *args, **kwargs):
# 	bot = await TelegramClient(
# 		'main_bot',
# 		api_id,
# 		api_hash
# 	).start(bot_token=bot_token)
#
# 	me = await bot.get_me()
# 	bot_logging.introduce_myself(me)
#
# 	register_all(bot, *args, **kwargs)
# 	await bot.run_until_disconnected()
