from utilities import chat_filter
from utilities import message_logger
from utilities import general_commands
import discord


async def execute_commands(message, client):
    if message.author.id != 593106374112837647:
        if message.content.startswith('$help'):
            await general_commands.support(message)
        elif message.content.startswith('$filtertypes'):
            await general_commands.filter_types(message)
        elif message.content.startswith('$log guide'):
            await general_commands.log_guide(message)

        args = message.content.split()

        if len(args) >= 3:
            if message.content.startswith('$cf')and (args[1] == 'bl' or args[1] == 'wl' or args[1] == 'rl')\
                    and args[2] == 'guide':
                await general_commands.word_filter_guide(message, args)
            elif message.content.startswith('$cf') and args[1] == 'chrlm' and args[2] == 'guide':
                await general_commands.chrlm_guide(message)
            elif message.content.startswith('$cf') and (args[1] == 'repeat' or args[1] == 'caps') \
                    and args[2] == 'guide':
                await general_commands.other_guide(message, args)

        if message.channel.type != discord.ChannelType.private:

            if message.content.startswith('$cf enable'):
                await chat_filter.command_enable_filter(message)
            elif message.content.startswith('$cf disable'):
                await chat_filter.command_disable_filter(message)
            elif message.content.startswith('$cf chrlm limit set'):
                await chat_filter.command_set_char_limit(message, args)
            elif message.content.startswith('$cf chrlm limit display'):
                await chat_filter.command_display_character_limit(message)
            elif message.content.startswith('$log enable'):
                await message_logger.command_enable_logger(message)
            elif message.content.startswith('$log disable'):
                await message_logger.command_disable_logger(message)
            elif message.content.startswith('$log channel set'):
                await message_logger.command_set_channel(message)
            elif message.content.startswith('$cf check enable'):
                await chat_filter.command_is_enable(message)

            if len(args) >= 4:
                if args[0] == '$cf' and args[2] == 'channel' and args[3] == 'display':
                    await chat_filter.command_display_channels(message, args)
                elif args[0] == '$cf' and (args[1] == 'bl' or args[1] == 'wl' or args[1] == 'rl') \
                        and args[2] == 'word' and args[3] == 'display':
                    await chat_filter.command_display_words(message, args)

            if len(args) >= 5:
                if args[0] == '$cf' and args[3] == 'add':
                    await chat_filter.command_add_to_filter(message, args)
                elif args[0] == '$cf' and args[3] == 'remove':
                    await chat_filter.command_remove_from_filter(message, args)

            message_deleted = await chat_filter.black_list_filter(message)
            if message_deleted != True:
                message_deleted = await chat_filter.white_list_filter(message)
            if message_deleted != True:
                message_deleted = await chat_filter.red_list_filter(message)
            if message_deleted != True:
                message_deleted = await chat_filter.char_limit_filter(message)
            if message_deleted != True:
                message_deleted = await chat_filter.repeat_message_filter(message)
            if message_deleted != True:
                message_deleted = await chat_filter.caps_filter(message)