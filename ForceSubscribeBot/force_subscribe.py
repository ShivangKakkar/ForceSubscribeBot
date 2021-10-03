from pyrogram import Client, filters
from pyrogram.types import Message
from ForceSubscribeBot.admin_check import admin_check
from pyrogram.errors import UsernameInvalid, PeerIdInvalid, UserNotParticipant
from ForceSubscribeBot.database.chats_sql import get_force_chat, change_force_chat, get_only_owner


@Client.on_message(filters.text & filters.incoming & filters.command(["fsub", "forcesubscribe"]))
async def fsub(bot, msg: Message):
    chat_id = msg.chat.id
    bot_id = (await bot.get_me()).id
    success = await admin_check(bot, msg)
    if not success:
        return
    if len(msg.command) == 1:
        force_chat = await get_force_chat(chat_id)
        if force_chat:
            chat = await bot.get_chat(force_chat)
            mention = '@' + chat.username if chat.username else f"{chat.title} ({chat.id})"
            await msg.reply(f"**Current Force Subscribe Chat** is : {mention} \n\nCould be changed using `/forcesubscribe new_chat_id`")
        else:
            await msg.reply("No force subscribe chat set ! \n\nCould be set using `/forcesubscribe chat_id`")
    else:
        creator = True if (await bot.get_chat_member(chat_id, msg.from_user.id)).status == "creator" else False
        only_owner = await get_only_owner(chat_id)
        if only_owner and not creator:
            await msg.reply("Only owner can change Force Subscribe chat in this chat.")
            return
        to_be_chat = msg.command[1]
        try:
            bot_chat_member = await bot.get_chat_member(to_be_chat, bot_id)
        except (UsernameInvalid, PeerIdInvalid):
            await msg.reply(
                "Unsuccessful :( \n\nPossible reasons could be: \n\n"
                "1) I haven't been added there. \n"
                "2) The provided chat_id/username is invalid. \n"
                "3) I have been demoted there. \n"
                "4) You have provided link instead of username/chat_id. \n\n"
                "Please re-check all three and try again! "
                "If the problem persists, try demoting and promoting again."
            )
            return
        except ValueError as e:
            await msg.reply(f"Seriously? \n\n{str(e)}")
            return
        except UserNotParticipant:
            await msg.reply(f"I haven't been added there.")
            return
        if bot_chat_member.status == "administrator":
            to_be_chat_id = (await bot.get_chat(to_be_chat)).id
            await change_force_chat(chat_id, to_be_chat_id)
            await msg.reply("Successful. Now I'll mute people who haven't joined that chat. \n\nUse /settings to change settings.")
        else:
            await msg.reply("Please make me admin there and then try again !")
