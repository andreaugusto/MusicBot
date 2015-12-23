import asyncio
import discord
import re
import datetime
import youtube_dl
import os
import traceback

try:
    import creds
except:
    print("Need valid creds.py to login")
    exit()
	
savedir = "playlist"
if not os.path.exists(savedir):
	os.makedirs(savedir)
    
option = 'butts'
isPlaying = False
firstTime = True

ownerID = '77511942717046784'

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
    global ownerID
    global firstTime
    global skipCount
    global skipperlist
    if message.author == client.user:
        return
    if '!whitelist' in message.content.lower() and message.author.id == ownerID:
            msg = message.content
            substrStart = msg.find('!whitelist') + 11
            msg = msg[substrStart: ]
            msg.strip()
            msg = re.sub('<|@|>', '', msg)
            whitelist.append(msg)
    elif '!play' in message.content.lower():
            discord.opus.load_opus('libopus-0.dll')
            
            msg = message.content
            msg2 = msg
            substrStart = msg.find('!play') + 6
            msg = msg[substrStart: ]
            msg.strip()
            sendmsg = False
            if (not is_long_member(message.author.joined_at)) and message.author.id not in whitelist:
                print('no')
            elif msg == 'help':
                hotsmessage = yield from client.send_message(message.channel,helpmessage)
            elif message.author.id == ownerID and firstTime is True:
                vce = yield from client.join_voice_channel(message.author.voice_channel)
                firstTime = False
                playlist.append(msg)
            elif msg == 'playlist':
                endmsg = getPlaylist()
                #for things in playlist:
                #    count+=1
                #    endmsg =endmsg +str(count) + ": "+ things + " \n"
                sendmsg = True
                hotsmessage = yield from client.send_message(message.channel,endmsg)
            elif msg == 'skip':
                if message.author.id == ownerID:
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

def getPlaylist():
    endmsg = ''
    count = 0
    for things in playlist:
        if '&' in things:
            substrStart = things.find('&')
            fixedThings = things[ :substrStart]
            fixedThings.strip()
        else:
            fixedThings = things
        options = {
                'format': 'bestaudio/best',
                'extractaudio' : True,
                'audioformat' : "mp3",
                'outtmpl': '%(id)s',
                'noplaylist' : True,}
        ydl = youtube_dl.YoutubeDL(options)
        try:
            info = ydl.extract_info(fixedThings, download=False)
            title = info['title']
        except Exception as e:
            print('cannot access information')
            title = 'ERROR: Title is actual dicks.'
        count+=1
        endmsg =endmsg +str(count) + ": "+ title + " \n"
    return endmsg

def make_savepath(title, savedir=savedir):
    return os.path.join(savedir, "%s.mp3" % (title))

def download_song(unfixedsongURL):
    if '&' in unfixedsongURL:
        substrStart = unfixedsongURL.find('&')
        songURL = unfixedsongURL[ :substrStart]
        songURL.strip()
    else:
        songURL = unfixedsongURL
    print('at start o download')
    options = {
	    'format': 'bestaudio/best',
	    'extractaudio' : True,
	    'audioformat' : "mp3",
	    'outtmpl': '%(id)s',
	    'noplaylist' : True,}
    ydl = youtube_dl.YoutubeDL(options)
    try:
        print('trying first meal')
        info = ydl.extract_info(songURL, download=False)
        savepath = make_savepath(info['title'])
    except Exception as e:
        print('cannot access information')
        return 'butts!'
    try:
        os.stat(savepath)
        print ("%s already downloaded, continuing..." % savepath)
        return savepath
    except OSError:
        try:
            result = ydl.extract_info(songURL, download=True)
            os.rename(result['id'], savepath)
            print ("Downloaded and converted %s successfully!" % savepath)
            
            return savepath
        except Exception as e:
            print ("Can't download audio! %s\n" % traceback.format_exc())
            return 'butts!'
@asyncio.coroutine
def playlist_update():
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
                    print('going into download')
                    path = download_song(thing)
                    if path!='butts!':
                        player = vce.create_ffmpeg_player(path)
                        player.start()
                        isPlaying = True
                        while thing in playlist: playlist.remove(thing)
                        option = 'sleep'
                except:
                    print('am ded')
                    while thing in playlist: playlist.remove(thing)
            else:
                thing = 'https://www.youtube.com/watch?v=vWuQVpBeqLs'
                try:
                    path = download_song(thing)
                    if path!='butts!':
                        player = vce.create_ffmpeg_player(path)
                        player.start()
                        isPlaying = True
                        while thing in playlist: playlist.remove(thing)
                        option = 'sleep'
                except:
                    print('am ded')
                    while thing in playlist: playlist.remove(thing)
        if option == 'sleep' or option == 'skip':
            cnt = 0
            while option!='skip' and player.is_playing():
                cnt+=1
                yield from asyncio.sleep(1)
            player.stop()
            isPlaying = False
        else:
            print('dong')
            yield from asyncio.sleep(1)

loop = asyncio.get_event_loop()
try:
    loop.create_task(playlist_update())
    loop.run_until_complete(client.login(creds.discordid, creds.discordpw))
    loop.run_until_complete(client.connect())
except Exception:
    loop.run_until_complete(client.close())
finally:
    loop.close()
