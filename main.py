import os
import ptbot
from pytimeparse import parse
from dotenv import load_dotenv

load_dotenv()

TG_TOKEN = os.environ['TG_TOKEN']
TG_CHAT_ID = os.environ['TG_CHAT_ID']

bot = ptbot.Bot(TG_TOKEN)


def wait(chat_id, question):
    sec_parse = parse(question)
    msg_start_id = bot.send_message(chat_id, 'Запускаю таймер!')
    bot.create_countdown(sec_parse, notif, chat_id=chat_id, 
                         msg_id=msg_start_id, sec_max=sec_parse)
    bot.create_timer(sec_parse, end_timer, chat_id=chat_id)


def notif(secs_left, chat_id, msg_id, sec_max):
    progress = render_progressbar(sec_max, sec_max-secs_left)
    bot.update_message(chat_id, msg_id, f'Осталось {secs_left}\n{progress}')


def end_timer(chat_id):
    bot.send_message(chat_id, 'Время вышло')


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def main():
    bot.reply_on_message(wait)
    bot.run_bot()


if __name__ == '__main__':
    main()
