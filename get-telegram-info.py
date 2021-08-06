from telegram.ext import (
	Updater,
	MessageHandler,
	PicklePersistence,
	CommandHandler,
	Defaults,
	Filters
)

from telegram import ParseMode
from random import randint, shuffle
from bot_token import TOKEN
import logging
import pytz
import datetime as dtm


logging.basicConfig(format="%(name)s | %(asctime)s | %(levelname)s -> %(message)s", datefmt="%d/%m/%Y %I:%M:%S %p", level=logging.INFO)
logger=logging.getLogger(__name__)


def start_callback(update, context):
	"""
	Entry point callback
	"""
	extra_text=" ".join(context.args)
	logger.info("entry point callback function involved")
	logger.info("{}".format(update.message))
 
	update.message.reply_text("Welcom to <b><i>Info</i> bot</b> 🤖.\n"
		"My purpose is to give you short info related to your telegram account.\n\n"
		"<b>'id'</b> \n<b>'username'</b> \n<b>'first name'</b> \n<b>'language'</b> \n<b>'owner state'</b>" )


def info_callback(update, context):
	user_id=update.message.from_user.id or '--404--'
	username=update.message.from_user.username or '--404--'
	first_name=update.message.from_user.first_name or '--404--'
	language_code=update.message.from_user.language_code or '--404--'
	is_bot=update.message.from_user.is_bot or '--404--'

	is_bot='Bot' if is_bot else 'Human'

	logger.info(
		"id: {}, \nusername: {}, \nfirst_name: {},"
		" \naccount lang: {}, \naccount owner: {}.".format(
			user_id, username, first_name, language_code, is_bot
		)
	)

	update.message.reply_text(
		"id: <b>{}</b> \nusername: <b>@{}</b> \nfirst_name: <b>{}</b>"
		" \nlanguage: <b>{}</b> \nowner state: <b>{}</b>".format(
			user_id, username, first_name, language_code, is_bot
		)
	)


def chat_migrate(update, context):
	m=update.message
	dp=context.dispatcher

	old_id=m.migrate_from_chat_id or m.chat_id
	new_id=m.migrate_to_chat_id or m.chat_id

	if old_id in dp.chat_data:
		dp.chat_data[new_id].update(dp.chat_data.get(old_id))
		del dp.chat_data[old_id]


def main():
	defaults=Defaults(parse_mode=ParseMode.HTML, tzinfo=pytz.timezone('Asia/Tashkent'))
	persistence=PicklePersistence(filename='get-telegram-info.txt')

	updater=Updater(token=TOKEN, persistence=persistence, use_context=True, defaults=defaults)
	dp=updater.dispatcher

	start_handler=CommandHandler('start', start_callback)
	dp.add_handler(start_handler)

	info_handler=CommandHandler('my_info', info_callback)
	dp.add_handler(info_handler)

	chat_migrate_handler=MessageHandler(Filters.status_update.migrate, chat_migrate)
	dp.add_handler(chat_migrate_handler)

	updater.start_polling()
	updater.idle()

if __name__=='__main__':
	main()


"""
// user_info

{
	'delete_chat_photo': False, 
	'channel_chat_created': False, 
	'photo': [], 
	'caption_entities': [], 
	'entities': [
		{
			'length': 6, 
			'type': 'bot_command', 
			'offset': 0
		}
	], 
	'chat': {
		'type': 'private', 
		'first_name': 'DJ', 
		'id': 1383749572, 
		'username': 'creative_silent_mind'
	}, 
	'supergroup_chat_created': False, 
	'date': 1628247833, 
	'new_chat_members': [], 
	'message_id': 2, 
	'text': '/start', 
	'new_chat_photo': [], 
	'group_chat_created': False, 
	'from': {
		'username': 'creative_silent_mind', 
		'language_code': 'en', 
		'id': 1383749572, 
		'is_bot': False, 
		'first_name': 'DJ'
	}
}


chat_info

{
	'date': 1628251654, 
	'supergroup_chat_created': False, 
	'photo': [], 
	'channel_chat_created': False, 
	'delete_chat_photo': False, 
	'text': '/my_info', 
	'entities': [
		{
			'type': 'bot_command', 
			'offset': 0, 'length': 8
		}
	], 
	'message_id': 4579, 
	'chat': {
		'title': '6-dom, 84-honadon', 
		'type': 'supergroup', 
		'id': -1001266471350
	}, 
	'group_chat_created': False, 
	'sender_chat': {
		'title': '6-dom, 84-honadon', 
		'type': 'supergroup', 
		'id': -1001266471350
	}, 
	'new_chat_members': [], 
	'caption_entities': [], 
	'new_chat_photo': [], 
	'from': {
		'is_bot': True, 
		'first_name': 'Group', 
		'username': 'GroupAnonymousBot', 
		'id': 1087968824
	}
}

"""