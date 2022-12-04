import requests as rq

from funcs import *
from queryhandlers import *

API_ID = 16514976
API_HASH = '40bd8634b3836468bb2fb7eafe39d81a'

TOKEN = '5696074673:AAFjMo1nelLLuqWtB-G5uYHT64D0ZK-V2iY'


@bot.on_message(filters.command(['start', 'help']))
def start_cmd_func(a, msg):
    user = msg.chat.id
    Name = msg.chat.first_name
    a.send_message(user, start_txt.format(name=Name),
                   disable_web_page_preview=True)


@bot.on_message(filters.command(['features']))
def feature_cmd_func(a, msg):
    user = msg.chat.id
    Name = msg.chat.first_name
    a.send_message(user, feature_txt.format(name=Name),
                   disable_web_page_preview=True)


@bot.on_message(filters.command('api'))
def add_api_cmd(a, msg):
    API = filter_api(msg)
    if API == False:
        return
    addAPI(msg, API)


@bot.on_message(filters.command('footer'))
def add_footer_cmd(_, msg):
    ftr = filter_footer(msg, bot)
    if ftr == False:
        return
    addFooter(msg, ftr)


@bot.on_message(filters.command(['unlink', 'remove_api']))
def remove_api_cmd(_, msg):
    removeAPI(msg)


@bot.on_message(filters.private & filters.media)
def media_msgs(a, m):
    chat_ID = m.chat.id

    u_api = userQuery(chat_ID)
    if u_api == False:
        m.reply_text(add_api_txt)
        return
    Footer = mycol.find_one(chat_ID)
    footer = (Footer['FOOTER'])
    if footer == None:
        footer = ''
    msg = progress_msg(m)
    msg.edit_text(f'**{progress_txt}..**')

    caption = convert_post(m.caption, u_api)
    caption = f'<b>{caption}\n{footer}</b>'

    #msg.edit_text(f'**{failed_txt}** {e}')

    if m.photo != None:
        a.send_photo(chat_ID, m.photo.file_id, caption)

    if m.video != None:
        a.send_video(chat_ID, m.video.file_id, caption)
    if m.document != None:
        a.send_document(chat_ID, m.document.file_id, caption=caption)
    if m.animation != None:
        a.send_animation(chat_ID, m.animation.file_id, caption=caption)

    msg.delete()


@bot.on_message(filters.regex(url_ptrn))
def text_msgs(a, m):
    chat_ID = m.chat.id
    u_api = userQuery(chat_ID)
    if u_api == False:
        m.reply_text(add_api_txt)
        return
    Footer = mycol.find_one(chat_ID)
    footer = (Footer['FOOTER'])
    if footer == None:
        footer = ''

    msg = progress_msg(m)
    msg.edit_text(f'**{progress_txt}..**')
    caption = convert_post(m.text, u_api)
    caption = f'{caption}\n{footer}'
    text = f'<b>{caption}</b>'

    msg.edit_text(f'{text}', disable_web_page_preview=True)


bot.run()
