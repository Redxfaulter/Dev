#SATAN 
from keep_alive import keep_alive
keep_alive()
import asyncio
import random
from telethon import TelegramClient, events, functions, types

# --------------------
# API & Session Config
# --------------------
api_id = 25010242
api_hash = 'a176ec07a8e695393e669829ff91a659'
phone_number = '+919064830477 '
client = TelegramClient('@BFPYY', api_id, api_hash)

# --------------------
# Global Variables
# --------------------
# For auto-reply (.chudle / .soja)
auto_reply_active = False
auto_reply_target_id = None
auto_reply_index = 0
auto_reply_paragraphs = [
    "Hello! How can I help you today?",
    "Here is some useful information.",
    "Feel free to ask if you need further assistance.",
    "Thank you for reaching out.",
    "Have a great day!"
]

# For DM muting
muted_users = set()

# For pickup lines
pickup_lines = [
    "Are you a magician? Because whenever I look at you, everyone else disappears.",
    "I must be a snowflake because I've fallen for you."
]
dirty_pickup_lines = [
    "Dirty pickup line placeholder 1.",
    "Dirty pickup line placeholder 2."
]

# --------------------
# Command Handler
# --------------------
@client.on(events.NewMessage(outgoing=True, pattern=r'\..*'))
async def command_handler(event):
    global auto_reply_active, auto_reply_target_id, auto_reply_index
    text = event.raw_text.strip()
    parts = text.split()
    command = parts[0].lower()
    args = parts[1:]

    # .YourKing : Owner Introduction
    if command == '.Own':
        intro = "@BFPYY"
        await event.reply(intro)

    # .mute : Mute Anyone in DM (by replying to a message)
    elif command == '.mute':
        target = await event.get_reply_message()
        if target:
            muted_users.add(target.sender_id)
            await event.reply(f"Muted user with ID: {target.sender_id}")
        else:
            await event.reply("Please reply to a user's message to mute them.")

    # .unmute : Unmute in DM
    elif command == '.unmute':
        target = await event.get_reply_message()
        if target:
            if target.sender_id in muted_users:
                muted_users.remove(target.sender_id)
                await event.reply(f"Unmuted user with ID: {target.sender_id}")
            else:
                await event.reply("That user was not muted.")
        else:
            await event.reply("Please reply to a user's message to unmute them.")

    # .mid : YourKing Info
    elif command == '.Own':
        info = ": @BFPYY\nChannel : @TILLUMODZ"
        await event.reply(info)

    # .ban : Ban Anyone in DM (here, we use blocking)
    elif command == '.ban':
        target = await event.get_reply_message()
        if target:
            try:
                await client(functions.contacts.BlockRequest(id=target.sender_id))
                await event.reply(f"Banned (blocked) user with ID: {target.sender_id}")
            except Exception as e:
                await event.reply(f"Error banning user: {e}")
        else:
            await event.reply("Please reply to a user's message to ban them.")

    # .unban : Unban (unblock) user
    elif command == '.unban':
        target = await event.get_reply_message()
        if target:
            try:
                await client(functions.contacts.UnblockRequest(id=target.sender_id))
                await event.reply(f"Unbanned (unblocked) user with ID: {target.sender_id}")
            except Exception as e:
                await event.reply(f"Error unbanning user: {e}")
        else:
            await event.reply("Please reply to a user's message to unban them.")

    # .quiet : Make The Whole Group Quiet (requires group admin rights)
    elif command == '.quiet':
        if event.is_group:
            try:
                chat = await event.get_chat()
                await client(functions.messages.EditChatDefaultBannedRightsRequest(
                    peer=chat,
                    banned_rights=types.ChatBannedRights(
                        send_messages=True,
                        send_media=True,
                        send_stickers=True,
                        send_gifs=True,
                        send_games=True,
                        send_inline=True,
                        embed_links=True,
                        until_date=0
                    )
                ))
                await event.reply("Group has been made quiet.")
            except Exception as e:
                await event.reply(f"Error making group quiet: {e}")
        else:
            await event.reply("This command works only in groups.")

    # .relief : Let The Group Chat be Free (remove restrictions)
    elif command == '.relief':
        if event.is_group:
            try:
                chat = await event.get_chat()
                await client(functions.messages.EditChatDefaultBannedRightsRequest(
                    peer=chat,
                    banned_rights=types.ChatBannedRights()  # no restrictions
                ))
                await event.reply("Group restrictions lifted.")
            except Exception as e:
                await event.reply(f"Error lifting restrictions: {e}")
        else:
            await event.reply("This command works only in groups.")

    # .okie : Let Someone be Free When Group is Quieted
    elif command == '.okie':
        target = await event.get_reply_message()
        if event.is_group and target:
            try:
                chat = await event.get_chat()
                await client(functions.messages.EditChatParticipantRequest(
                    chat_id=chat.id,
                    user_id=target.sender_id,
                    banned_rights=types.ChatBannedRights()  # restore rights
                ))
                await event.reply("User has been allowed to speak.")
            except Exception as e:
                await event.reply(f"Error: {e}")
        else:
            await event.reply("This command requires a reply in a group.")

    # .naah : Make That Someone Quiet Again
    elif command == '.naah':
        target = await event.get_reply_message()
        if event.is_group and target:
            try:
                chat = await event.get_chat()
                await client(functions.messages.EditChatParticipantRequest(
                    chat_id=chat.id,
                    user_id=target.sender_id,
                    banned_rights=types.ChatBannedRights(
                        send_messages=True,
                        send_media=True,
                        send_stickers=True,
                        send_gifs=True,
                        send_games=True,
                        send_inline=True,
                        embed_links=True,
                        until_date=0
                    )
                ))
                await event.reply("User has been muted in the group.")
            except Exception as e:
                await event.reply(f"Error: {e}")
        else:
            await event.reply("This command requires a reply in a group.")

    # .ufff : See Who Can Speak While Quieted (stub)
    elif command == '.ufff':
        if event.is_group:
            await event.reply("Feature not implemented: Listing users with speak rights is not available yet.")
        else:
            await event.reply("This command works only in groups.")

    # .kick : Remove Any Member from Group
    elif command == '.kick':
        target = await event.get_reply_message()
        if event.is_group and target:
            try:
                chat = await event.get_chat()
                await client.kick_participant(chat, target.sender_id)
                await event.reply("User has been kicked from the group.")
            except Exception as e:
                await event.reply(f"Error kicking user: {e}")
        else:
            await event.reply("This command requires a reply in a group.")

    # .asleep : Make Your Status Asleep
    elif command == '.asleep':
        try:
            await client(functions.account.UpdateProfileRequest(about="Asleep"))
            await event.reply("Status updated to Asleep.")
        except Exception as e:
            await event.reply(f"Error updating status: {e}")

    # .awake : Be Awake
    elif command == '.awake':
        try:
            await client(functions.account.UpdateProfileRequest(about="Awake"))
            await event.reply("Status updated to Awake.")
        except Exception as e:
            await event.reply(f"Error updating status: {e}")

    # .busy : Make Your Status Busy
    elif command == '.busy':
        try:
            await client(functions.account.UpdateProfileRequest(about="Busy"))
            await event.reply("Status updated to Busy.")
        except Exception as e:
            await event.reply(f"Error updating status: {e}")

    # .free : Be Free
    elif command == '.free':
        try:
            await client(functions.account.UpdateProfileRequest(about="Free"))
            await event.reply("Status updated to Free.")
        except Exception as e:
            await event.reply(f"Error updating status: {e}")

    # .reset <@> : Reset Insta Password (stub)
    elif command == '.reset':
        if args:
            insta_id = args[0]
            await event.reply(f"Instagram password reset initiated for {insta_id} (stub).")
        else:
            await event.reply("Usage: .reset <insta_id>")

    # .del : Delete Someone's Chat (delete a replied-to message)
    elif command == '.del':
        target = await event.get_reply_message()
        if target:
            try:
                await client.delete_messages(target.chat_id, [target.id])
                await event.reply("Message deleted.")
            except Exception as e:
                await event.reply(f"Error deleting message: {e}")
        else:
            await event.reply("Reply to a message to delete it.")

    # .purge <no> : Delete the last N messages in the chat
    elif command == '.purge':
        if args and args[0].isdigit():
            count = int(args[0])
            try:
                msgs = await client.get_messages(event.chat_id, limit=count)
                await client.delete_messages(event.chat_id, [msg.id for msg in msgs])
                await event.reply(f"Purged {count} messages.")
            except Exception as e:
                await event.reply(f"Error purging messages: {e}")
        else:
            await event.reply("Usage: .purge <number_of_messages>")

    # .tinfo : Get the info of someone on Telegram
    elif command == '.tinfo':
        target = await event.get_reply_message()
        if target:
            try:
                entity = await client.get_entity(target.sender_id)
                info = (f"User Info:\nID: {entity.id}\nUsername: {entity.username}\n"
                        f"Name: {entity.first_name} {entity.last_name if entity.last_name else ''}")
                await event.reply(info)
            except Exception as e:
                await event.reply(f"Error getting user info: {e}")
        else:
            await event.reply("Reply to a user's message to get their info.")

    # .insta <@> : Get the info of any Insta ID (stub)
    elif command == '.insta':
        if args:
            insta_id = args[0]
            await event.reply(f"Fetching Instagram info for {insta_id} (not implemented).")
        else:
            await event.reply("Usage: .insta <insta_id>")

    # .pusd <digit> : Price of Dollar (stub)
    elif command == '.pusd':
        if args and args[0].isdigit():
            digit = args[0]
            await event.reply(f"Price of Dollar for {digit} (not implemented).")
        else:
            await event.reply("Usage: .pusd <digit>")

    # .trl : Translate any message (stub)
    elif command == '.trl':
        target = await event.get_reply_message()
        if target:
            original = target.message
            translated = f"Translated: {original}"  # Replace with actual translation logic
            await event.reply(translated)
        else:
            await event.reply("Reply to a message to translate it.")

    # .gana <name> : Search the lyrics of any song (stub)
    elif command == '.gana':
        if args:
            song = " ".join(args)
            await event.reply(f"Searching lyrics for '{song}' (not implemented).")
        else:
            await event.reply("Usage: .gana <song_name>")

    # .spam <no> : Spam your specific message
    elif command == '.spam':
        if args and args[0].isdigit():
            count = int(args[0])
            msg = " ".join(args[1:]) if len(args) > 1 else "Spam!"
            for _ in range(count):
                await event.respond(msg)
                await asyncio.sleep(0.5)
        else:
            await event.reply("Usage: .spam <count> <message>")

    # .gc : Create a Private Group
    elif command == '.gc':
        group_title = " ".join(args) if args else "Private Group"
        try:
            result = await client(functions.messages.CreateChatRequest(
                users=[],  # You can add a list of user IDs here
                title=group_title
            ))
            await event.reply(f"Private group '{group_title}' created.")
        except Exception as e:
            await event.reply(f"Error creating group: {e}")

    # .close <time> : Close the Group (stub)
    elif command == '.close':
        if args and args[0].isdigit():
            duration = int(args[0])
            await event.reply(f"Group will be closed (read-only) for {duration} seconds (not fully implemented).")
        else:
            await event.reply("Usage: .close <time_in_seconds>")

    # .chud <no> : (Provocative command – stub implementation)
    elif command == '.chud':
        if args and args[0].isdigit():
            num = int(args[0])
            for _ in range(num):
                await event.respond("Provocative message (placeholder).")
                await asyncio.sleep(0.5)
        else:
            await event.reply("Usage: .chud <number>")

    # .pline : Pickup Line
    elif command == '.pline':
        line = random.choice(pickup_lines) if pickup_lines else "No pickup lines available."
        await event.reply(line)

    # .dline : Dirty Pickup Line
    elif command == '.dline':
        line = random.choice(dirty_pickup_lines) if dirty_pickup_lines else "No dirty pickup lines available."
        await event.reply(line)

    # .cnt <time> : Start Countdown
    elif command == '.cnt':
        if args and args[0].isdigit():
            seconds = int(args[0])
            for i in range(seconds, 0, -1):
                await event.reply(f"Countdown: {i} seconds remaining")
                await asyncio.sleep(1)
            await event.reply("Countdown finished!")
        else:
            await event.reply("Usage: .cnt <time_in_seconds>")

    # .calc : Calculator
    elif command == '.calc':
        if args:
            expression = " ".join(args)
            try:
                # WARNING: Using eval is dangerous. Here it is used in a limited context.
                result = eval(expression, {"__builtins__": {}})
                await event.reply(f"Result: {result}")
            except Exception as e:
                await event.reply(f"Error evaluating expression: {e}")
        else:
            await event.reply("Usage: .calc <expression>")

    # .btc : Crypto Bitcoin Price (stub)
    elif command == '.btc':
        await event.reply("Bitcoin Price: Not implemented.")

    # .ltc : Crypto Litecoin Price (stub)
    elif command == '.ltc':
        await event.reply("Litecoin Price: Not implemented.")

    # .ton : Crypto Ton Price (stub)
    elif command == '.ton':
        await event.reply("Ton Price: Not implemented.")

    # .stock : Today Highest Increased Stock (stub)
    elif command == '.stock':
        await event.reply("Stock info: Not implemented.")

    # .dm <text> : Send Direct Message from Group (by replying to a message)
    elif command == '.dm':
        if args:
            dm_text = " ".join(args)
            target = await event.get_reply_message()
            if target:
                try:
                    await client.send_message(target.sender_id, dm_text)
                    await event.reply("Direct message sent.")
                except Exception as e:
                    await event.reply(f"Error sending DM: {e}")
            else:
                await event.reply("Please reply to a user's message to send a DM.")
        else:
            await event.reply("Usage: .dm <message_text>")

    # .cspam <no> : Copy & Paste Someone's Message (by replying)
    elif command == '.cspam':
        if args and args[0].isdigit():
            count = int(args[0])
            target = await event.get_reply_message()
            if target:
                for _ in range(count):
                    await event.respond(target.message)
                    await asyncio.sleep(0.5)
            else:
                await event.reply("Please reply to a message to copy it.")
        else:
            await event.reply("Usage: .cspam <number>")

    # .chudle : Start Auto-Reply (one paragraph per incoming message)
    elif command == '.chudle':
        target = await event.get_reply_message()
        if target:
            auto_reply_active = True
            auto_reply_target_id = target.sender_id
            auto_reply_index = 0
            await event.reply("Auto-reply activated for this user.")
        else:
            await event.reply("Reply to a user's message to start auto-reply.")

    # .soja : Stop Auto-Reply
    elif command == '.soja':
        auto_reply_active = False
        auto_reply_target_id = None
        await event.reply("Auto-reply deactivated.")

    # .upi : Upi id 
    elif command == '.upi':
        await event.reply("Nur10x@axl")

    # .cmds : List All Commands
    elif command == '.cmds':
        cmds = (
            "📜 Available Commands:\n"
            ".vishu : Owner Introduction\n"
            ".mute : Mute Anyone in DM\n"
            ".unmute : Unmute Them Again\n"
            ".mid : Mrityu's Info\n"
            ".ban : Ban Anyone in DM\n"
            ".unban : Unban Them Again\n"
            ".quiet : Make The Whole Group Quiet\n"
            ".relief : Let The Group Chat be Free\n"
            ".okie : Let Someone be Free When Whole Group is Quieted\n"
            ".naah : Make That Someone Quiet Again\n"
            ".ufff : See Who Can Speak While Quieted\n"
            ".kick : Remove Any Member from Group\n"
            ".asleep : Make Your Status Asleep\n"
            ".awake : Be Awake\n"
            ".busy : Make Your Status Busy\n"
            ".free : Be Free\n"
            ".reset <@> : Reset Insta Password\n"
            ".del : Delete Someone's Chat\n"
            ".purge <no> : Delete The Msgs\n"
            ".tinfo : Get The Info of Someone Telegram\n"
            ".insta <@> : Get The Info of Any Insta ID\n"
            ".pusd <digit> : Price of Dollar\n"
            ".trl : Translate Any Msg\n"
            ".gana <name> : Search The Lyrics of Any Song\n"
            ".spam <no> : Spam Your Specific Msg\n"
            ".gc : Create a Private Group\n"
            ".close <time> : Close The Group\n"
            ".chud <no> : F*ck Anyone\n"
            ".pline : Pickup Line\n"
            ".dline : Dirty Pickup Line\n"
            ".cnt <time> : Start Countdown\n"
            ".calc : Calculator\n"
            ".btc : Crypto Bitcoin Price\n"
            ".ltc : Crypto Litecoin Price\n"
            ".ton : Crypto Ton Price\n"
            ".stock : Today Highest Increased Stock\n"
            ".dm <text> : Send Direct Msg from Group\n"
            ".cspam <no> : Copy & Paste Someone's Msg\n"
            ".chudle : Start Auto-Reply\n"
            ".soja : Stop Auto-Reply\n"
            ".cmds : All Self-Bot Commands"
        )
        await event.reply(cmds)

    else:
        await event.reply("Unknown command.")

# --------------------
# Auto-Reply Handler
# --------------------
@client.on(events.NewMessage(incoming=True))
async def auto_reply_handler(event):
    global auto_reply_active, auto_reply_target_id, auto_reply_index
    # If auto-reply is active and the sender is the target
    if auto_reply_active and auto_reply_target_id and event.sender_id == auto_reply_target_id:
        paragraph = auto_reply_paragraphs[auto_reply_index]
        auto_reply_index = (auto_reply_index + 1) % len(auto_reply_paragraphs)
        await event.reply(paragraph)

# --------------------
# Mute Filter (Ignore messages from muted users in private chats)
# --------------------
@client.on(events.NewMessage(incoming=True))
async def mute_filter(event):
    if event.is_private and event.sender_id in muted_users:
        # Stop further processing for muted users
        raise events.StopPropagation

# --------------------
# Start the Client
# --------------------
client.start(phone=phone_number)
print("Selfbot is running...")
client.run_until_disconnected()
