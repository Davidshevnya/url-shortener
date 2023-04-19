from aiogram import types, Bot, Dispatcher, executor
from BitlyAPI import shorten_urls
from dotenv import dotenv_values
from uuid import uuid4


bot = Bot(token=str(dotenv_values(".env").get("TOKEN")))
dp = Dispatcher(bot)


def cut_link(link: list):
    return shorten_urls(link)



@dp.message_handler(commands=["start", "help"])
async def start(message: types.Message):
    await message.answer(f"👋 Привет, {message.from_user.full_name}.\
                        \n🤖 Это тот же bit.ly, но теперь вы можете им пользоваться в телеграме!\
                        \n🔗 Для того чтобы сократить ссылку просто скиньте мне ее.\
                        \n👾 Так же, чтобы не заходить каждый раз в личные сообщения с ботом, вы можете просто написать \n@{dotenv_values('.env').get('BOT_NAME')} <Ссылка> и бот выведет вам сокращенную сылку.\
                        \n🥷 Бота разработал - @moylub")


@dp.message_handler()
async def on_message(message: types.Message):
    msg = await message.answer("Буп-буп... Сокращаю...")

    links = cut_link(link=[message.text])

    await msg.delete()

    if links[0].short_url:
        await message.answer(f"Держите вашу ссылку:\
                            {links[0].short_url}")
    else:
        await message.answer("Уупс.. Невалидная ссылка😔")



@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):

    links = cut_link(link=[query.query])

    

    if links[0].short_url:

        article = [types.InlineQueryResultArticle(
            id=str(uuid4()),
            title=str(links[0].short_url),
            input_message_content=types.InputTextMessageContent(message_text=f"{links[0].short_url}")
        )]

        await query.answer(article, cache_time=60, is_personal=True)

    else:
        article_not_found = [types.InlineQueryResultArticle(
            id=str(uuid4()),
            title="Уупс.. Невалидная ссылка",
            input_message_content=types.InputTextMessageContent(message_text="Ссылка невалидная"),
            thumb_url="https://cdn5.vectorstock.com/i/1000x1000/93/24/hyperlink-to-unsecured-website-is-invalid-vector-25729324.jpg"
        )]

        await query.answer(article_not_found, cache_time=60, is_personal=True)

if __name__ == "__main__":
    executor.start_polling(dp)