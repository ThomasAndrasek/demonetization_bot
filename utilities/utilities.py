from utilities import chat_filter
import discord


async def execute_commands(message, client):
    if message.author.id != '593106374112837647':
        if message.channel.type != discord.ChannelType.private:
            args = message.content.split()

            if message.content.startswith('$cf enable'):
                await chat_filter.command_enable_filter(message, client)
            elif message.content.startswith('$cf disable'):
                await chat_filter.command_disable_filter(message, client)
            elif message.content.startswith('$cf chrlm limit set'):
                await chat_filter.command_set_char_limit(message, client, args)

            if len(args) >= 5:
                if args[0] == '$cf' and args[3] == 'add':
                    await chat_filter.command_add_to_filter(message, client, args)
                elif args[0] == '$cf' and args[3] == 'remove':
                    await chat_filter.command_remove_from_filter(message, client, args)

            message_deleted = await chat_filter.black_list_filter(message, client)
            if message_deleted != True:
                message_deleted = await chat_filter.white_list_filter(message, client)
                if message_deleted != True:
                    message_deleted = await chat_filter.red_list_filter(message, client)
                if message_deleted != True:
                    await chat_filter.char_limit_filter(message, client)