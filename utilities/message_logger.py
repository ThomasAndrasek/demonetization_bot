import sqlite3
# Enable and Disable
# Set Channel

storage_path = 'databases\\logger\\logger_storage.db'


def check_for_server(server_id):
    conn = sqlite3.connect(storage_path)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS loggerStorage(serverID TEXT, enable INTEGER, channelID TEXT)')
    c.execute('SELECT serverID FROM loggerStorage WHERE serverID = ?', (server_id,))
    data = c.fetchall()
    if len(data) == 0:
        c.execute('INSERT INTO loggerStorage VALUES(?, 0, "null")', (server_id,))
    conn.commit()
    c.close()
    conn.close()


def toggle_logger(server_id, enable):
    conn = sqlite3.connect(storage_path)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS loggerStorage(serverID TEXT, enable INTEGER, channelID TEXT)')
    check_for_server(server_id)
    c.execute('UPDATE loggerStorage SET enable = ? WHERE serverID = ?', (enable, server_id,))
    conn.commit()
    c.close()
    conn.close()


def set_channel(server_id, channel_id):
    conn = sqlite3.connect(storage_path)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS loggerStorage(serverID TEXT, enable INTEGER, channelID TEXT)')
    check_for_server(server_id)
    c.execute('UPDATE loggerStorage SET channelID = ? WHERE serverID = ?', (channel_id, server_id,))
    conn.commit()
    c.close()
    conn.close()


def get_channel(server_id):
    conn = sqlite3.connect(storage_path)
    c = conn.cursor()
    c.execute('SELECT channelID FROM loggerStorage WHERE serverID = ?', (server_id,))
    data = c.fetchall()
    for thing in data:
        for item in thing:
            c.close()
            conn.close()
            return item


def is_enable(server_id):
    check_for_server(server_id)
    conn = sqlite3.connect(storage_path)
    c = conn.cursor()
    c.execute('SELECT enable FROM loggerStorage WHERE serverID = ?', (server_id,))
    data = c.fetchall()
    for thing in data:
        for item in thing:
            c.close()
            conn.close()
            return item


async def check_permissions(message):
    user_permissions = message.channel.permissions_for(message.author)
    if user_permissions.administrator or user_permissions.manage_messages:
        return True
    else:
        await message.channel.send('Sorry, you do not have the appropriate server permissions to use this command.')
        return False


async def command_enable_logger(message):
    if await check_permissions(message):
        server_id = message.guild.id
        toggle_logger(server_id, 1)
        await message.channel.send('Logger has been enabled.')


async def command_disable_logger(message):
    if await check_permissions(message):
        server_id = message.guild.id
        toggle_logger(server_id, 0)
        await message.channel.send('Logger has been disabled.')


async def command_set_channel(message):
    if await check_permissions(message):
        server_id = message.guild.id
        channel_id = message.channel.id
        set_channel(server_id, channel_id)
        await message.channel.send('I will now log deleted messages in this channel.')


async def log(message, reason):
    server_id = message.guild.id
    if is_enable(server_id) == 1:
        channel_id = get_channel(server_id)
        if channel_id != 'null':
            channel_id = int(channel_id)
            channel = message.guild.get_channel(channel_id)
            await channel.send('***************************************\n**Message Author:** {}'.format(message.author) +
                               '\n**Reason Deleted:** {}'.format(reason) +
                               '\n**Message Content:** *{}*\n***************************************'.format(message.content))