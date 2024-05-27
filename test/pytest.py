import pytest
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils.executor import start_webhook
from main import bot, dp, user_sessions, send_start, choose_language, set_language

@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def bot_instance():
    return bot

@pytest.fixture
def dispatcher():
    return dp

@pytest.fixture
def message():
    return types.Message(message_id=1, date=None, chat=None, from_user=None, sender_chat=None, forward_from=None, forward_from_chat=None, forward_from_message_id=None, forward_signature=None, forward_sender_name=None, forward_date=None, reply_to_message=None, via_bot=None, edit_date=None, media_group_id=None, author_signature=None, text="Test message", entities=None, animation=None, audio=None, document=None, photo=None, sticker=None, video=None, video_note=None, voice=None, caption=None, contact=None, dice=None, game=None, poll=None, venue=None, location=None, new_chat_members=None, left_chat_member=None, new_chat_title=None, new_chat_photo=None, delete_chat_photo=None, group_chat_created=None, supergroup_chat_created=None, channel_chat_created=None, migrate_to_chat_id=None, migrate_from_chat_id=None, pinned_message=None, invoice=None, successful_payment=None, connected_website=None, passport_data=None, proximity_alert_triggered=None, video_chat_scheduled=None, video_chat_started=None, video_chat_ended=None, video_chat_participants_invited=None, web_app_data=None)

@pytest.mark.asyncio
async def test_send_start(bot_instance, message):
    message.text = "/start"
    await send_start(message)
    assert message.text == "/start"

@pytest.mark.asyncio
async def test_choose_language(bot_instance, message):
    await choose_language(message)
    assert "HELP" in message.text

@pytest.mark.asyncio
async def test_set_language(bot_instance, message):
    callback_query = types.CallbackQuery(id="1", from_user=message.from_user, message=message, chat_instance="instance", data="en")
    await set_language(callback_query)
    assert user_sessions[callback_query.from_user.id]['language'] == "en"
