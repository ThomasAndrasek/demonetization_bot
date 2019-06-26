from utilities import chat_filter


async def execute_commands(message, client):
    args = message.content.split()

    if message.content.startswith('$cf enable'):
        await chat_filter.command_enable_filter(message, client)
    elif message.content.startswith('$cf disable'):
        await chat_filter.command_disable_filter(message, client)

    if args[0] == '$cf' and args[3] == 'add':
        await chat_filter.command_add_to_filter(message, client, args)
    elif args[0] == '$cf' and args[3] == 'remove':
        await chat_filter.command_remove_from_filter(message, client, args)

    await chat_filter.black_list_filter(message, client)
    await chat_filter.white_list_filter(message, client)
    await chat_filter.red_list_filter(message, client)