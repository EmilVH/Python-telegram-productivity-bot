import logging
from telegram.ext import Updater, CommandHandler, PicklePersistence

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def greet(update, context):
    reply_text = "Hello, I am bot that helps to deal with procrastination and track your productivity"
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)


def pomodoro_finished(context):
    context.bot.send_message(chat_id=context.job.context, text='Timer finished, good job')


def start_pomodoro(update, context):
    """Starts pomodoro timer for 25 minutes"""
    context.bot.send_message(chat_id=update.effective_chat.id, text='Timer started, please work now')
    context.job_queue.run_once(pomodoro_finished, 25 * 60, context=update.effective_chat.id,
                               name=str(update.effective_chat))


def main() -> None:
    persistence = PicklePersistence(filename='bot.info')
    with open('key.info', 'r') as fl:
        api_key = fl.read()
    updater = Updater(api_key, persistence=persistence)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', greet))
    dispatcher.add_handler(CommandHandler(command='pomodoro', callback=start_pomodoro))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
