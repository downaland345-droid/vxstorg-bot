import asyncio
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, BaseFilter
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

router = Router()
ADMIN_ID = 5331036146 

class IsAdmin(BaseFilter):
    async def __call__(self, event) -> bool:
        user_id = event.from_user.id if hasattr(event, 'from_user') else event.message.from_user.id
        return user_id == ADMIN_ID

router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())

@router.message(Command("start"))
async def cmd_start(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 Купить звёзды", callback_data="buy_stars")],
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")]
    ])
    await message.answer("👋 Привет! Я VXSTORGAPP. Выбери действие:", reply_markup=kb)

@router.message(F.text.lower() == "купить звезды")
@router.message(Command("buy_stars"))
@router.callback_query(F.data == "buy_stars")
async def buy_stars_handler(event):
    msg = event.message if isinstance(event, CallbackQuery) else event
    text = "<b>Ваш канал</b>\n\nV Дешёвые звёзды V"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Купить звёзды ↗", url="https://t.me/vxstorgApp")]
    ])
    await msg.answer(text, reply_markup=kb, parse_mode=ParseMode.HTML)
    if isinstance(event, CallbackQuery):
        await event.answer()

@router.callback_query(F.data == "settings")
async def settings_handler(callback: CallbackQuery):
    await callback.answer("В разработке.", show_alert=True)

@router.message()
async def deny_access(message: Message):
    await message.answer("⛔ Доступ запрещён.")

async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)
    
    async def handle(request):
        return web.Response(text="Bot is running!")
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    
    port = int(os.getenv('PORT', 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
