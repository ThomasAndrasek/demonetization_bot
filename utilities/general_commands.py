async def support(message):
    await message.author.send(
        '**All Available Commands**' +
        '```' +
        '$help' +
        '\n$filtertypes >> Explains all the chat filter types.' +
        '\n$cf <filter type> guide >> Sends guide of how to set up specified filter type.' +
        '\nAll filter types for previous command >> bl, wl,rl, chrlm, repeat, caps' +
        '\n' +
        '\n$cf <filter type> word add <word> >> Adds the specified word to the specified filter.' +
        '\n$cf <filter type> word remove <word> >> Removes the specified word from the specified filter.' +
        '\nAll filter types for last two commands >> bl, wl, rl' +
        '\n' +
        '\n$cf <filter type> channel add <channel>> Adds the specified channel to the specified filter.' +
        '\n$cf <filter type> channel remove <channel> >> Removes the specified channel from the specified filter.' +
        '\nAll filter types for last two commands >> bl, wl, rl, caps, chrlm, repeat'
        '\n' +
        '\n$cf enable >> Enables the chat filter.' +
        '\n$cf disable >> Disables the chat filter.' +
        '\n' +
        '\n$cf chrlm limit set <limit> >> Sets the character limit to specified limit.' +
        '\n$cf chrlm limit display >> Sends the current character limit.'
        '\n' +
        '\n$cf <filter type> word display >> Sends user list of all filtered words for specified filter.' +
        '\n$cf <filter type> channel display >> Sends a list of all filtered channels for specified filter.' +
        '\n' +
        '\n$log enable >> Enables the message deletion log.' +
        '\n$log disable >> Disables the message deletion log.' +
        '\n$log channel set >> Sets the message deletion log to current channel.' +
        '\n$log guide >> Sends guide of setting up log.'
        '```' +
        '\n' +
        '\nThanks for using the bot.'
    )


async def filter_types(message):
    await message.author.send(
        '**Current Filter Types**' +
        '```' +
        'Black List >> bl' +
        '\nThe Black List looks for specified words in a message and will delete the message if any of them are in '
        'the message.' +
        '\n' +
        '\nWhite List >> wl' +
        '\nThe White List looks to see if a message has a specified word in it, if not the message will be deleted.' +
        '\n' +
        '\nRed List >> rl' +
        '\nLike the Black List, the Red List looks to see if a certain word is in the message. However is a lot more '
        'picky. For examble, if the word "hell" is filtered, the message "hello" would also be deleted. Useful for '
        'deleting links.' +
        '\n' +
        '\nCharacter Limit >> chrlm' +
        '\nThe Character Limit checks if the message has more characters than the set limit, if it does the message '
        'will be deleted. Example would be the the limit Twitter has on tweets.' +
        '\n' +
        '\nCaps Lock >> caps' +
        '\nThe Caps Lock Filter checks to see if a majority of the message is in all caps, if so the message will be '
        'deleted.' +
        '\n' +
        '\nSimilar Messages >> repeat' +
        '\nThe Repeat Filter will look to see if the message sent is similar to any of the previous messages sent by '
        'the user in the past minute, if so the new message will be deleted.' +
        '```'
    )


async def word_filter_guide(message, args):
    await message.author.send(
        '**1. Add Channel To Filter**' +
        '\n$cf {} channel add <channel>'.format(args[1]) +
        '\nEx: $cf {} chanel add general'.format(args[1]) +
        '\n' +
        '\n**2. Add Word To Filter**' +
        '\n$cf {} word add <word>'.format(args[1]) +
        '\nEx: $cf {} word add wumpus'.format(args[1]) +
        '\n' +
        '\n**3. Enable Filter**' +
        '\n$cf enable' +
        '\n' +
        '\nCongratulations, the filter is now set up.'
    )


async def chrlm_guide(message):
    await message.author.send(
        '**1. Add Channel To Filter**' +
        '\n$cf chrlm channel add <channel>' +
        '\nEx: $cf chrlm chanel add general' +
        '\n' +
        '\n**2. Add Word To Filter**' +
        '\n$cf chrlm word add <word>' +
        '\nEx: $cf chrlm limit set 100' +
        '\n' +
        '\n**3. Enable Filter**' +
        '\n$cf enable' +
        '\n' +
        '\nCongratulations, the filter is now set up.'
    )


async def other_guide(message, args):
    await message.author.send(
        '**1. Add Channel To Filter**' +
        '\n$cf {} channel add <channel>'.format(args[1]) +
        '\nEx: $cf {} chanel add general'.format(args[1]) +
        '\n' +
        '\n**2. Enable Filter**' +
        '\n$cf enable' +
        '\n' +
        '\nCongratulations, the filter is now set up.'
    )


async def log_guide(message):
    await message.author.send(
        '**1. Set Channel For Log**' +
        '\n$log channel set >> Use this command in channel you wish to log deleted messages.' +
        '\n' +
        '\n**2. Enable Log**' +
        '\n$log enable' +
        '\n' +
        '\nCongratulations, the log is now set up.'
    )