import sqlite3
import os
import discord
from datetime import timedelta
from datetime import datetime

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
    elif filter_type == 'chrlm' and type_to_add == 'limit':
        return 'charLimit'
    elif filter_type == 'chrlm' and type_to_add == 'channel':
        return 'charLimitChannels'
    elif filter_type == 'repeat' and type_to_add == 'channel':
        return 'repeatChannels'
    elif filter_type == 'caps' and type_to_add == 'channel':
        return 'capsChannels'


def check_if_channel_filtered(server_id, channel_name, filter_type):
    conn = sqlite3.connect(storage_path.format(server_id))
    c = conn.cursor()
    return_value = 0
    if filter_type == "blacklist":
        c.execute('SELECT channelID FROM blackListChannels WHERE channelID = ?', (channel_name,))
    elif filter_type == "whitelist":
        c.execute('SELECT channelID FROM whiteListChannels WHERE channelID = ?', (channel_name,))
    elif filter_type == "redlist":
        c.execute('SELECT channelID FROM redListChannels WHERE channelID = ?', (channel_name,))
    elif filter_type == "charlimit":
        c.execute('SELECT channelID FROM charLimitChannels WHERE channelID = ?', (channel_name,))
    elif filter_type == 'repeat':
        c.execute('SELECT channelID FROM repeatChannels WHERE channelID = ?', (channel_name,))
    elif filter_type == 'caps':
        c.execute('SELECT channelID FROM capsChannels WHERE channelID = ?', (channel_name,))
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
    elif table_name == 'charLimit':
        c.execute('CREATE TABLE IF NOT EXISTS charLimit(lim INTEGER)')
    elif table_name == 'blackListChannels':
        c.execute('CREATE TABLE IF NOT EXISTS blackListChannels(channelID TEXT)')
    elif table_name == 'whiteListChannels':
        c.execute('CREATE TABLE IF NOT EXISTS whiteListChannels(channelID TEXT)')
    elif table_name == 'redListChannels':
        c.execute('CREATE TABLE IF NOT EXISTS redListChannels(channelID TEXT)')
    elif table_name == 'charLimitChannels':
        c.execute('CREATE TABLE IF NOT EXISTS charLimitChannels(channelID TEXT)')
    elif table_name == 'repeatChannels':
        c.execute('CREATE TABLE IF NOT EXISTS repeatChannels(channelID TEXT)')
    elif table_name == 'capsChannels':
        c.execute('CREATE TABLE IF NOT EXISTS capsChannels(channelID TEXT)')
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
    elif table_name == 'charLimitChannels':
        c.execute('SELECT channelID FROM charLimitChannels WHERE channelID = ?', (thing_to_add,))
        data = c.fetchall()
        if len(data) == 0:
            c.execute('INSERT INTO charLimitChannels VALUES(?)', (thing_to_add,))
            return_value = 1
        else:
            return_value = 0
    elif table_name == 'repeatChannels':
        c.execute('SELECT channelID FROM repeatChannels WHERE channelID = ?', (thing_to_add,))
        data = c.fetchall()
        if len(data) == 0:
            c.execute('INSERT INTO repeatChannels VALUES(?)', (thing_to_add,))
            return_value = 1
        else:
            return_value = 0
    elif table_name == 'capsChannels':
        c.execute('SELECT channelID FROM capsChannels WHERE channelID = ?', (thing_to_add,))
        data = c.fetchall()
        if len(data) == 0:
            c.execute('INSERT INTO capsChannels VALUES(?)', (thing_to_add,))
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
    elif table_name == 'charLimitChannels':
        c.execute('SELECT channelID FROM charLimitChannels WHERE channelID = ?', (thing_to_remove,))
        data = c.fetchall()
        if len(data) == 0:
            return_value = 0
        else:
            return_value = 1
            c.execute('DELETE FROM charLimitChannels WHERE channelID = ?', (thing_to_remove,))
    elif table_name == 'repeatChannels':
        c.execute('SELECT channelID FROM repeatChannels WHERE channelID = ?', (thing_to_remove,))
        data = c.fetchall()
        if len(data) == 0:
            return_value = 0
        else:
            return_value = 1
            c.execute('DELETE FROM repeatChannels WHERE channelID = ?', (thing_to_remove,))
    elif table_name == 'capsChannels':
        c.execute('SELECT channelID FROM capsChannels WHERE channelID = ?', (thing_to_remove,))
        data = c.fetchall()
        if len(data) == 0:
            return_value = 0
        else:
            return_value = 1
            c.execute('DELETE FROM capsChannels WHERE channelID = ?', (thing_to_remove,))
    conn.commit()
    c.close()
    conn.close()
    return return_value


def set_char_limit(server_id, limit):
    create_table(server_id, 'charLimit')
    conn = sqlite3.connect(storage_path.format(server_id))
    c = conn.cursor()
    c.execute('SELECT lim FROM charLimit')
    data = c.fetchall()
    if len(data) == 0:
        c.execute('INSERT INTO charLimit VALUES(?)', (limit,))
    else:
        c.execute('UPDATE charLimit SET lim = ?', (limit,))
    conn.commit()
    c.close()
    conn.close()


async def check_permissions(message):
    user_permissions = message.channel.permissions_for(message.author)
    if user_permissions.administrator or user_permissions.manage_messages:
        return True
    else:
        await message.channel.send('Sorry, you do not have the appropriate server permissions to use this command.')
        return False
# Commands Portion


# Enable Filter
async def command_enable_filter(message):
    if await check_permissions(message):
        server_id = message.guild.id
        enable_filter(server_id)
        await message.channel.send('The chat filter has been enabled.')


async def command_disable_filter(message):
    if await check_permissions(message):
        server_id = message.guild.id
        disable_filter(server_id)
        await message.channel.send('The chat filter has been disabled.')


async def command_set_char_limit(message, args):
    if await check_permissions(message):
        server_id = message.guild.id
        limit = args[4]
        set_char_limit(server_id, limit)
        await message.channel.send('The new character limit is "{}."'.format(limit))


async def command_add_to_filter(message, args):
    if await check_permissions(message):
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


async def command_remove_from_filter(message, args):
    if await check_permissions(message):
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


async def black_list_filter(message):
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
                            c.close()
                            conn.close()
                            return await delete_message(message)



async def white_list_filter(message):
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
                c.close()
                conn.close()
                return await delete_message(message)


async def red_list_filter(message):
    server_id = message.guild.id
    if check_if_enabled(server_id) == 1:
        if check_if_channel_filtered(server_id, message.channel.name, 'redlist') == 1:
            conn = sqlite3.connect(storage_path.format(server_id))
            c = conn.cursor()
            c.execute('SELECT redListedWord FROM redListWords')
            data = c.fetchall()
            for item in data:
                for red_list_word in item:
                    if red_list_word.upper() in message.content.upper():
                        await message.author.send(
                            'Please refrain from using red list words.')
                        c.close()
                        conn.close()
                        return await delete_message(message)


async def char_limit_filter(message):
    server_id = message.guild.id
    if check_if_enabled(server_id):
        if check_if_channel_filtered(server_id, message.channel.name, 'charlimit') == 1:
            conn = sqlite3.connect(storage_path.format(server_id))
            c = conn.cursor()
            c.execute('SELECT lim FROM charLimit')
            data = c.fetchall()
            for item in data:
                for limit in item:
                    if len(message.content) > limit:
                        await message.author\
                            .send('Please refrain from going over the character limit of {}.'.format(limit))
                        c.close()
                        conn.close()
                        return await delete_message(message)


async def repeat_message_filter(message):
    server_id = message.guild.id
    if check_if_enabled(server_id):
        if check_if_channel_filtered(server_id, message.channel.name, 'repeat') == 1:
            async for old_message in message.channel.history(limit=100, after=datetime(message.created_at.year,
                                                                                       message.created_at.month,
                                                                                       message.created_at.day,
                                                                                       message.created_at.hour,
                                                                                       message.created_at.minute,
                                                                                       message.created_at.second) -
                                                                              timedelta(seconds=60)):
                if old_message.author == message.author:
                    if old_message.id != message.id:
                        '''if timedelta(
                                message.created_at.day - old_message.created_at.day,
                                message.created_at.hour - old_message.created_at.hour,
                                message.created_at.minute - old_message.created_at.minute,
                                message.created_at.second - old_message.created_at.second)\
                                .total_seconds() > 60:'''
                        total = 0
                        for x in range(len(message.content)):
                            if x < len(message.content) and x < len(old_message.content):
                                if message.content[x] == old_message.content[x]:
                                    total += 1
                        if len(message.content) < len(old_message.content):
                            if total / len(old_message.content) > 2/3:
                                await message.author\
                                    .send('Your most recent message is too similar to a recent previous message.')
                                return await delete_message(message)
                        else:
                            if total / len(message.content) > 2/3:
                                await message.author\
                                    .send('Your most recent message is too similar to a recent previous message.')
                                return await delete_message(message)


async def caps_filter(message):
    server_id = message.guild.id
    if check_if_enabled(server_id):
        if check_if_channel_filtered(server_id, message.channel.name, 'caps') == 1:
            if len(message.content) > 15:
                caps_message = message.content.upper()
                total = 0
                for x in range(len(message.content)):
                    if message.content[x] == caps_message[x]:
                        total += 1
                if total / len(message.content) > 2/3:
                    await message.author.send('Please refrain from using caps lock messages.')
                    return await delete_message(message)