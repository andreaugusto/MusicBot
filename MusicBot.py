import asyncio
import discord
import re
import datetime
import youtube_dl
import pafy

try:
    import creds
except:
    print("Need valid creds.py to login")
    exit()
    
option = 'butts'
isPlaying = False
firstTime = True

skipCount = 0
skipperlist = []

playlist = []

helpmessage = '`!play [youtube link]` will allow me to play a new song or add it to the queue.\n`!play playlist` will print out all links to youtube videos currently in the queue!\n`!play skip` will make it skip to the next song after 4 people vote to skip the current one!'

with open('whitelist.txt') as f:
    whitelist = f.readlines()
for i, item in enumerate(whitelist):
    whitelist[i] = item.rstrip()

client = discord.Client()

@client.async_event
def on_ready():
    print('Connected!')
    print('Username: ' + client.user.name)
    print('ID: ' + client.user.id)
    print('--Server List--')
    for server in client.servers:
        print(server.name)
        
@client.async_event
def on_message(message):
    global option
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    if '!whitelist' in message.content.lower():
            msg = message.content
            substrStart = msg.find('!whitelist') + 11
            msg = msg[substrStart: ]
            msg.strip()
            msg = re.sub('<|@|>', '', msg)
            whitelist.append(msg)
    elif '!play' in message.content.lower():
            discord.opus.load_opus('libopus-0.dll')
            global firstTime
            global skipCount
            global skipperlist
            msg = message.content
            msg2 = msg
            substrStart = msg.find('!play') + 6
            msg = msg[substrStart: ]
            msg.strip()
            sendmsg = False
            if (message.author.name == 'Weggy' or not is_long_member(message.author.joined_at)) and message.author.id not in whitelist:
                print('no')
            elif msg == 'help':
                hotsmessage = yield from client.send_message(message.channel,helpmessage)
            elif message.author.id == '77511942717046784' and firstTime is True:
                vce = yield from client.join_voice_channel(message.author.voice_channel)
                firstTime = False
                playlist.append(msg)
            elif msg == 'playlist':
                endmsg = ''
                count = 0
                for things in playlist:
                    count+=1
                    endmsg =endmsg +str(count) + ": "+ things + " \n"
                sendmsg = True
                buttmsg = discord.utils.get(client.servers[0].channels, name='general')
                hotsmessage = yield from client.send_message(buttmsg,endmsg)
            elif msg == 'skip':
                if message.author.id == '77511942717046784':
                    skipperlist = []
                    skipCount = 0
                    option = 'skip'
                elif message.author.id not in skipperlist:
                    print('skip increased by 1')
                    print(skipCount)
                    skipperlist.append(message.author.id)
                    skipCount+=1
                else:
                    print('already voted to skip')
                if skipCount > 1:
                    skipperlist = []
                    skipCount = 0
                    option = 'skip'
            else:
                playlist.append(msg)
            yield from asyncio.sleep(5)
            yield from client.delete_message(message)
            if sendmsg is True:
                sendmsg = False
                yield from asyncio.sleep(10)
                yield from client.delete_message(hotsmessage)

def is_long_member(dateJoined):
    convDT = dateJoined.date()
    today = datetime.date.today()
    margin = datetime.timedelta(days = 2)
    return today - margin > convDT

@asyncio.coroutine
def some_task():
    #print('ding')
    global isPlaying
    global option
    global firstTime
    yield from client.wait_for_ready()
    count = 0
    time = 0
    while count!= -1:
        if isPlaying is False and firstTime is False:
            if playlist:
                print('ding')
                vce = client.voice
                thing = playlist[0]
                try: 
                    player = vce.create_ytdl_player(thing)
                    player.start()
                    isPlaying = True
                    while thing in playlist: playlist.remove(thing)
                    option = 'sleep'
                    count+=1
                except:
                    genchan = discord.utils.get(client.servers[0].channels, name='general')
                    yield from client.send_message(genchan,'you crashed me')
                    while thing in playlist: playlist.remove(thing)
            else:
                thing = 'https://www.youtube.com/watch?v=vWuQVpBeqLs'
                try:
                    player = vce.create_ytdl_player(thing,)
                    player.start()
                    isPlaying = True
                    while thing in playlist: playlist.remove(thing)
                    option = 'sleep'
                    count+=1
                except:
                    genchan = discord.utils.get(client.servers[0].channels, name='general')
                    #yield from client.send_message(genchan,'you crashed me')
                    print('am ded')
                    while thing in playlist: playlist.remove(thing)
        if option == 'sleep' or option == 'skip':
            cnt = 0
            while option!='skip' and player.is_playing():
                #print('big butts')
                cnt+=1
                yield from asyncio.sleep(1)
            player.stop()
            isPlaying = False
        else:
            print('dong')
            yield from asyncio.sleep(1)

loop = asyncio.get_event_loop()
try:
    loop.create_task(some_task())
    loop.run_until_complete(client.login('creds.discordemail', creds.discordpw))
    loop.run_until_complete(client.connect())
except Exception:
    loop.run_until_complete(client.close())
finally:
    loop.close()
