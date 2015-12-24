# MusicBot

## What does it do?

It plays music in a plug.dj "request" style.

## How do I set it up?

Install Python here - https://www.python.org/downloads/

Install Git here - https://git-scm.com/download/win

make sure you select this option in the Python install - https://i.gyazo.com/2c06a7ee35afda3383185916fd2a94d3.png
and this option in the Git install - https://cdn.discordapp.com/attachments/129489631539494912/129505383223001088/pic.png

It was coded in 3.5.1 but 3.5 will work fine.


Make sure you have installed the required modules by running `fixnupdate.bat`

Make sure you meet the non-code requirements of having existing accounts for
both discord.

##Options.txt set up
  
Line 1: accepts "0" or "1", determines if it checks the amount of days a user have been in the discord (0 turning this check off, 1 turning it on) 

Line 2: the number of days until a person can freely interact with the bot and not be on the whitelist

Line 3: The Owner's User ID

Line 4: The number of votes to skip for it to actually skip


## What are its commands?

`!whatismyuserid` will tell you your user ID!

`!whitelist` will whitelist people (and you if the server is new!) so they can play music

`!blacklist` will disallow a person from interacting with the bot!

`!play help` will summon a list of commands accepted by the bot!

`!play [youtube link]` will allow me to play a new song or add it to the queue.

`!play playlist` will print out all links to youtube videos currently in the queue!

`!play skip` will make it skip to the next song after 4 people vote to skip the current one!

## Sounds cool, How do I use it?
Simply download the bot, set everything up, then run `runbot.bat`!

It'll let you know if it's connected and what channels are connected.

Once started, its good to go. If you have any errors, report them here or on my discord and then restart the bot

Rhino Bot Discord - https://discord.gg/0iqN3da4zqrPzOjp

#FAQ

Q:`'pip' is not recognized as an internal or external command`

A: http://stackoverflow.com/questions/23708898/pip-is-not-recognized-as-an-internal-or-external-command

Q:`Bot prints 'no, not whitelisted and new' when I try and play something`

A: Add yourself to the whitelist!

Q:`I'm getting this error! http://puu.sh/m6hkf/40eec0910c.png`
A: The bot needs permission to delete messages. I'll be adding an options file to toggle this later though

Q: `I'm having an issue with the Discord installation / It doesn't say anything when I run it`
A: Run `fixnupdate.bat`

Q:`I'm having other errors with the bot, it has to be broken`
A: If Rhinobot is running in my discord, the bot isn't broken. I keep everything as updated as possible! 

