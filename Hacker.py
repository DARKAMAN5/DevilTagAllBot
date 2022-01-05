import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)
spam_chats = []

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply(
    "__**'✨ 𝑰 𝑨𝑴 𝑻𝑨𝑮𝑨𝑳𝑳 𝑩𝑶𝑻**, 𝑰 𝑪𝑨𝑵 𝑴𝑬𝑵𝑻𝑰𝑶𝑵 𝑨𝑳𝑳 𝑴𝑬𝑴𝑩𝑬𝑹𝑺 𝑰𝑵 𝑮𝑹𝑶𝑼𝑷 🤑\n𝑪𝑳𝑰𝑪𝑲 **/help** 𝑭𝑶𝑹 𝑴𝑶𝑹𝑬 𝑰𝑵𝑭𝑶𝑹𝑴𝑨𝑻𝑰𝑶𝑵__\n\n 𝑱𝑶𝑰𝑵 [✨𝑹𝑶𝒀𝑨𝑳 𝑺𝑼𝑷𝑷𝑶𝑹𝑻✨](https://t.me/DARKAMANSUPPORT)",
    link_preview=False,
    buttons=(
      [
        Button.url('🇦𝐃𝐃 𝐌𝐄𝐍𝐓𝐈𝐎𝐍 𝐁𝐎𝐓', 'https://t.me/MENTIONXROBOT'),
        Button.url('🇨𝐇𝐀𝐍𝐍𝐄𝐋', 'https://t.me/DARKAMANCHANNEL'),
        Button.url('🇸𝐔𝐏𝐏𝐎𝐑𝐓', 'https://t.me/DARKAMANSUPPORT')
      ]
    )
  )

@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**𝑯𝑬𝑳𝑷 𝑴𝑬𝑵𝑼 𝑶𝑭 𝑻𝑨𝑮𝑨𝑳𝑳𝑩𝑶𝑻**\n\n𝑪𝑶𝑴𝑴𝑨𝑵𝑫𝑺 ☞︎︎︎ /all\n__You can use this command with text what you want to mention others.__\nExample: `/all Good Morning!`\n__You can you this command as a reply to any message. Bot will tag users to that replied messsage__.\n\nFollow [✨𝑹𝑶𝒀𝑨𝑳 𝑼𝑷𝑫𝑨𝑻𝑬𝑺✨](https://t.me/DARKAMANCHANNEL)"
  await event.reply(
    helptext,
    link_preview=False,
    buttons=(
      [
        Button.url('🇸𝐔𝐏𝐏𝐎𝐑𝐓', 'https://t.me/JaiHindChatting'),
        Button.url('🇨𝐇𝐀𝐍𝐍𝐄𝐋', 'https://t.me/DARKAMANCHANNEL')
      ]
    )
  )
  
@client.on(events.NewMessage(pattern="^/all ?(.*)"))
async def all(event):
  chat_id = event.chat_id
  if event.is_private:
    return await event.respond("__This command Can Be Use In Groups And Channels @JaiHindChatting !__")
  
  is_admin = False
  try:
    partici_ = await client(GetParticipantRequest(
      event.chat_id,
      event.sender_id
    ))
  except UserNotParticipantError:
    is_admin = False
  else:
    if (
      isinstance(
        partici_.participant,
        (
          ChannelParticipantAdmin,
          ChannelParticipantCreator
        )
      )
    ):
      is_admin = True
  if not is_admin:
    return await event.respond("__Only Admins Can Mention All\n\nFor More Go On @JaiHindChatting !__")
  
  if event.pattern_match.group(1) and event.is_reply:
    return await event.respond("__Give me one argument!__")
  elif event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.is_reply:
    mode = "text_on_reply"
    msg = await event.get_reply_message()
    if msg == None:
        return await event.respond("__I Can't Mention Members For Older Messages! (messages which are sent before I'm added to group)__")
  else:
    return await event.respond("__Reply To a Message Or Give Me Some Text To Mention Others\n\nMade bY @JaiHindChatting !__")
  
  spam_chats.append(chat_id)
  usrnum = 0
  usrtxt = ''
  async for usr in client.iter_participants(chat_id):
    if not chat_id in spam_chats:
      break
    usrnum += 1
    usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
    if usrnum == 5:
      if mode == "text_on_cmd":
        txt = f"{usrtxt}\n\n{msg}\n\nMade bY @JaiHindChatting ✌️🔥"
        await client.send_message(chat_id, txt)
      elif mode == "text_on_reply":
        await msg.reply(usrtxt)
      await asyncio.sleep(2)
      usrnum = 0
      usrtxt = ''
  try:
    spam_chats.remove(chat_id)
  except:
    pass

@client.on(events.NewMessage(pattern="^/cancel$"))
async def cancel_spam(event):
  if not event.chat_id in spam_chats:
    return await event.respond('__There Is No Proccess On Going @JaiHindChatting...__')
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await event.respond('__Stopped.__')

print(">> HACKER TAGALL STARTED @JaiHindChatting<<")
client.run_until_disconnected()
