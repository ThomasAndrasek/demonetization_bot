import sqlite3
import os
import discord

# Path for databases
storage_path = 'C:\\Users\\kille\\Desktop\\databases\\demonetization bot\\chat filter\\{}.db'


def get_table_name(filter_type, type_to_add):
    if filter_type == 'bl' and type_to_add == 'word':
        return 'blackListWords'
    elif filter_type == 'bl' and type_to_add == 'channel':
        return 'blackListChannels'
    elif filter_type == 'wl' and type_to_add == 'word':
        return 'whiteListWords'
    elif filter_type == 'wl' and type_to_add == 'channel':
        return 'whiteListChannels'
    elif filter_type == 'rl' and type_to_add == 'word':
        return 'redListWords'
    elif filter_type == 'rl' and type_to_add == 'channel':
        return 'redListChannels'


def check_if_channel_filtered(server_id, channel_name, filter_type):
    conn = sqlite3.connect(storage_path.format(server_id))
    c = conn.cursor()
    return_value = 0
    if filter_type == "blacklist":
        c.execute('SELECT channelID FROM blackListChannels WHERE channelID = ?', (channel_name,))
        data = c.fetchall()
        if len(data) > 0:
            return_value = 1
    elif filter_type == "whitelist":
        c.execute('SELECT channelID FROM whiteListChannels WHERE channelID = ?', (channel_name,))
        data = c.fetchall()
        if len(data) > 0:
            return_value = 1
    elif filter_type == "redlist":
        c.execute('SELECT channelID FROM redListChannels WHERE channelID = ?', (channel_name,))
        data = c.fetchall()
        if len(data) > 0:
            return_value = 1
    conn.commit()
    c.close()
    conn.close()
    return return_value



# Creates a table for the specified table type in the database
def create_table(server_id, table_name):
    conn = sqlite3.connect(storage_path.format(server_id))
    c = conn.cursor()
    if table_name == 'blackListWords':
        c.execute('CREATE TABLE IF NOT EXISTS blackListWords(blackListedWord TEXT)')
    elif table_name == 'whiteListWords':
        c.execute('CREATE TABLE IF NOT EXISTS whiteListWords(whiteListedWord TEXT)')
    elif table_name == 'redListWords':
        c.execute('CREATE TABLE IF NOT EXISTS redListWords(redListedWord TEXT)')
    elif table_name == 'blackListChannels':
        c.execute('CREATE TABLE IF NOT EXISTS blackListChannels(channelID TEXT)')
    elif table_name == 'whiteListChannels':
        c.execute('CREATE TABLE IF NOT EXISTS whiteListChannels(channelID TEXT)')
    elif table_name == 'redListChannels':
        c.execute('CREATE TABLE IF NOT EXISTS redListChannels(channelID TEXT)')
    elif table_name == 'enabled':
        c.execute('CREATE TABLE IF NOT EXISTS enableFilter(enable INTEGER)')
    conn.commit()
    c.close()
    conn.close()


# Return 1 if enabled
# Return 0 if disabled
# Return -1 if never instantiated
def check_if_enabled(server_id):
    conn = sqlite3.connect(storage_path.format(server_id))
    c = conn.cursor()
    c.execute('SELECT enable FROM enableFilter')
    data = c.fetchall()
    if len(data) == 0:
        return -1
    else:
        for item in data:
            for thing in item:
                return thing
    c.close()
    conn.close()


def enable_filter(server_id):
    create_table(server_id, 'enabled')
    enable = check_if_enabled(server_id)
    conn = sqlite3.connect(storage_path.format(server_id))
    c = conn.cursor()
    if enable == -1:
        c.execute('INSERT INTO enableFilter VALUES(1)')
    elif enable == 0:
        c.execute('UPDATE enableFilter SET enable = 1')
    conn.commit()
    c.close()
    conn.close()


def disable_filter(server_id):
    create_table(server_id, 'enabled')
    enable = check_if_enabled(server_id)
    conn = sqlite3.connect(storage_path.format(server_id))
    c = conn.cursor()
    if enable == -1:
        c.execute('INSERT INTO enableFilter VALUES(0)')
    elif enable == 1:
        c.execute('UPDATE enableFilter SET enable = 0')
    conn.commit()
    c.close()
    conn.close()


def add_to_filter(server_id, thing_to_add, table_name):
    create_table(server_id, table_name)
    return_value = -1
    conn = sqlite3.connect(storage_path.format(server_id))
    c = conn.cursor()
    if table_name == 'blackListWords':
        c.execute('SELECT blackListedWord FROM blackListWords WHERE blackListedWord = ?', (thing_to_add,))
        data = c.fetchall()
        if len(data) == 0:
            c.execute('INSERT INTO blackListWords VALUES(?)', (thing_to_add,))
            return_value = 1
        else:
            return_value = 0
    elif table_name == 'whiteListWords':
        c.execute('SELECT whiteListedWord FROM whiteListWords WHERE whiteListedWord = ?', (thing_to_add,))
        data = c.fetchall()
        if len(data) == 0:
            c.execute('INSERT INTO whiteListWords VALUES(?)', (thing_to_add,))
            return_value = 1
        else:
            return_value = 0
    elif table_name == 'redListWords':
        c.execute('SELECT redListedWord FROM redListWords WHERE redListedWord = ?', (thing_to_add,))
        data = c.fetchall()
        if len(data) == 0:
            c.execute('INSERT INTO redListWords VALUES(?)', (thing_to_add,))
            return_value = 1
        else:
            return_value = 0
    elif table_name == 'blackListChannels':
        c.execute('SELECT channelID FROM blackListChannels WHERE channelID = ?', (thing_to_add,))
        data = c.fetchall()
        if len(data) == 0:
            c.execute('INSERT INTO blackListChannels VALUES(?)', (thing_to_add,))
            return_value = 1
        else:
            return_value = 0
    elif table_name == 'whiteListChannels':
        c.execute('SELECT channelID FROM whiteListChannels WHERE channelID = ?', (thing_to_add,))
        data = c.fetchall()
        if len(data) == 0:
            c.execute('INSERT INTO whiteListChannels VALUES(?)', (thing_to_add,))
            return_value = 1
        else:
            return_value = 0
    elif table_name == 'redListChannels':
        c.execute('SELECT channelID FROM redListChannels WHERE channelID = ?', (thing_to_add,))
        data = c.fetchall()
        if len(data) == 0:
            c.execute('INSERT INTO redListChannels VALUES(?)', (thing_to_add,))
            return_value = 1
        else:
            return_value = 0
    conn.commit()
    c.close()
    conn.close()
    return return_value


def remove_from_filter(server_id, thing_to_remove, table_name):
    create_table(server_id, table_name)
    return_value = -1
    conn = sqlite3.connect(storage_path.format(server_id))
    c = conn.cursor()
    if table_name == 'blackListWords':
        c.execute('SELECT blackListedWord FROM blackListWords WHERE blackListedWord = ?', (thing_to_remove,))
        data = c.fetchall()
        if len(data) == 0:
            return_value = 0
        else:
            return_value = 1
            c.execute('DELETE FROM blackListWords WHERE blackListedWord = ?', (thing_to_remove,))
    elif table_name == 'whiteListWords':
        c.execute('SELECT whiteListedWord FROM whiteListWords WHERE whiteListedWord = ?', (thing_to_remove,))
        data = c.fetchall()
        if len(data) == 0:
            return_value = 0
        else:
            return_value = 1
            c.execute('DELETE FROM whiteListWords WHERE whiteListedWord = ?', (thing_to_remove,))
    elif table_name == 'redListWords':
        c.execute('SELECT redListedWord FROM redListWords WHERE redListedWord = ?', (thing_to_remove,))
        data = c.fetchall()
        if len(data) == 0:
            return_value = 0
        else:
            return_value = 1
            c.execute('DELETE FROM redListWords WHERE redListedWord = ?', (thing_to_remove,))
    elif table_name == 'blackListChannels':
        c.execute('SELECT channelID FROM blackListChannels WHERE channelID = ?', (thing_to_remove,))
        data = c.fetchall()
        if len(data) == 0:
            return_value = 0
        else:
            return_value = 1
            c.execute('DELETE FROM blackListChannels WHERE channelID = ?', (thing_to_remove,))
    elif table_name == 'whiteListChannels':
        c.execute('SELECT channelID FROM whiteListChannels WHERE channelID = ?', (thing_to_remove,))
        data = c.fetchall()
        if len(data) == 0:
            return_value = 0
        else:
            return_value = 1
            c.execute('DELETE FROM whiteListChannels WHERE channelID = ?', (thing_to_remove,))
    elif table_name == 'redListChannels':
        c.execute('SELECT channelID FROM redListChannels WHERE channelID = ?', (thing_to_remove,))
        data = c.fetchall()
        if len(data) == 0:
            return_value = 0
        else:
            return_value = 1
            c.execute('DELETE FROM redListChannels WHERE channelID = ?', (thing_to_remove,))
    conn.commit()
    c.close()
    conn.close()
    return return_value


# Commands Portion


# Enable Filter
async def command_enable_filter(message, client):
    server_id = message.guild.id
    enable_filter(server_id)
    await message.channel.send('The chat filter has been enabled.')


async def command_disable_filter(message, client):
    server_id = message.guild.id
    disable_filter(server_id)
    await message.channel.send('The chat filter has been disabled.')


async def command_add_to_filter(message, client, args):
    server_id = message.guild.id
    filter_type = args[1]
    type_to_add = args[2]
    thing_to_add = args[4]
    table_name = get_table_name(filter_type, type_to_add)
    return_value = add_to_filter(server_id, thing_to_add, table_name)
    if return_value == 1:
        await message.channel.send('I have added "{}" to the {} filter.'.format(thing_to_add, filter_type))
    else:
        await message.channel.send('"{}" has already been added.'.format(thing_to_add))


async def command_remove_from_filter(message, client, args):
    server_id = message.guild.id
    filter_type = args[1]
    type_to_add = args[2]
    thing_to_remove = args[4]
    table_name = get_table_name(filter_type, type_to_add)
    return_value = remove_from_filter(server_id, thing_to_remove, table_name)
    if return_value == 1:
        await message.channel.send('I have removed "{}" from the {} filter.'.format(thing_to_remove, filter_type))
    else:
        await message.channel.send('"{}" is not in the filter.'.format(thing_to_remove))


async def delete_message(message):
    try:
        await message.delete()
        return True
    except discord.Forbidden:
        await message.guild.owner.send(
            'Error on deleting message in the {} guild, I do not have the appropriate permissions.'.format(
                message.guild.name))
    except discord.HTTPException:
        await message.guild.owner.send(
            'Error on deleting message in the {} guild.'.format(message.guild.name))
    return False


async def black_list_filter(message, client):
    server_id = message.guild.id
    if check_if_enabled(server_id) == 1:
        if check_if_channel_filtered(server_id, message.channel.name, 'blacklist') == 1:
            words_to_check = message.content.split()
            conn = sqlite3.connect(storage_path.format(server_id))
            c = conn.cursor()
            c.execute('SELECT blackListedWord FROM blackListWords')
            data = c.fetchall()
            for item in data:
                for black_list_word in item:
                    for word in words_to_check:
                        if word.upper() == black_list_word.upper():
                            await message.author.send('Please refrain from using black listed words.')
                            return await delete_message(message)



async def white_list_filter(message, client):
    server_id = message.guild.id
    if check_if_enabled(server_id) == 1:
        if check_if_channel_filtered(server_id, message.channel.name, 'whitelist') == 1:
            words_to_check = message.content.split()
            conn = sqlite3.connect(storage_path.format(server_id))
            c = conn.cursor()
            c.execute('SELECT whiteListedWord FROM whiteListWords')
            data = c.fetchall()
            used_word = False
            for item in data:
                for white_list_word in item:
                    for word in words_to_check:
                        if word.upper() == white_list_word.upper():
                            used_word = True

            if used_word == False:
                await message.author.send('Please use one of the white listed words.')
                return await delete_message(message)


async def red_list_filter(message, client):
    server_id = message.guild.id
    if check_if_enabled(server_id) == 1:
        if check_if_channel_filtered(server_id, message.channel.name, 'redlist') == 1:
            words_to_check = message.content.split()
            conn = sqlite3.connect(storage_path.format(server_id))
            c = conn.cursor()
            c.execute('SELECT redListedWord FROM redListWords')
            data = c.fetchall()
            for item in data:
                for red_list_word in item:
                    if red_list_word.upper() in message.content.upper():
                        await message.author.send(
                            'Please refrain from using red list words.')
                        return await delete_message(message)
