import asyncio
import discord
import re
import datetime
import youtube_dl
import os
import traceback

if not discord.opus.is_loaded():
    discord.opus.load_opus('libopus-0.dll')

try:
    with open('blacklist.txt') as f:
        blacklist = f.readlines()
    for i, item in enumerate(blacklist):
        whitelist[i] = item.rstrip()
    with open('whitelist.txt') as f:
        whitelist = f.readlines()
    for i, item in enumerate(whitelist):
        whitelist[i] = item.rstrip()
    with open('options.txt') as f:
        options = f.readlines()
    for i, item in enumerate(options):
        options[i] = item.rstrip()
except:
    print('one of the text files was deleted, reinstall')

	
savedir = "playlist"
if not os.path.exists(savedir):
	os.makedirs(savedir)
    
option = 'butts'
isPlaying = False
firstTime = True

ownerID = options[4]
skipsRequired = int(options[5])
skipCount = 0
skipperlist = []

playlist = []
currentlyPlaying = ''

helpmessage = '`!play [youtube link]` will allow me to play a new song or add it to the queue.\n`!play playlist` will print out all links to youtube videos currently in the queue!\n`!play skip` will make it skip to the next song after 4 people vote to skip the current one!'


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
    if message.channel.is_private:
        yield from client.send_message(message.channel, 'You cannot use this bot in private messages.')
    if '!whatismyuserid' in message.content.lower():
        print(message.author.id)
    if '!whitelist' in message.content.lower() and message.author.id == ownerID:
            msg = message.content
            substrStart = msg.find('!whitelist') + 11
            msg = msg[substrStart: ]
            msg.strip()
            msg = re.sub('<|@|>', '', msg)
            f = open('whitelist.txt', 'a')
            f.write(msg + "\r")
            f.close()
            whitelist.append(msg)
    elif '!blacklist' in message.content.lower() and message.author.id == ownerID:
            msg = message.content
            substrStart = msg.find('!blacklist') + 11
            msg = msg[substrStart: ]
            msg.strip()
            msg = re.sub('<|@|>', '', msg)
            f = open('blacklist.txt', 'a')
            f.write(msg + "\r")
            f.close()
            blacklist.append(msg)
    elif '!servers' in message.content.lower():
        count=0
        for servers in client.servers:
            count+=1
        if count > 1:
            yield from client.send_message(message.channel,'I DIDN\'T LISTEN TO DIRECTIONS AND HAVE MY BOT ON MORE THAN ONE SERVER')
        else:
            print('you good')
    elif '!play' in message.content.lower():
            msg = message.content
            msg2 = msg
            substrStart = msg.find('!play') + 6
            msg = msg[substrStart: ]
            msg.strip()
            sendmsg = False
            if message.author.id in blacklist :
                print('no, blacklisted')
            elif (options[2]=='1' and not is_long_member(message.author.joined_at)) and message.author.id not in whitelist:
                print('no, not whitelisted and new')
            elif msg.lower() == 'help':
                hotsmessage = yield from client.send_message(message.channel,helpmessage)
            elif message.author.id == ownerID and firstTime is True:
                vce = yield from client.join_voice_channel(message.author.voice_channel)
                firstTime = False
                playlist.append(msg)
            elif msg.lower() == 'move' and message.author.id == ownerID:
                yield from client.voice.disconnect()
                vce = yield from client.join_voice_channel(message.author.voice_channel)
            elif msg.lower() == 'playlist':
                endmsg = currentlyPlaying
                endmsg = endmsg + getPlaylist()
                sendmsg = True
                if(endmsg == ''):
                    hotsmessage = yield from client.send_message(message.channel,'There is currently nothing left in the playlist')
                else:
                    hotsmessage = yield from client.send_message(message.channel,endmsg)
            elif msg.lower() == 'skip':
                if message.author.id == ownerID:
                    skipperlist = []
                    skipCount = 0
                    option = 'skip'
                elif message.author.id not in skipperlist:
                    skipperlist.append(message.author.id)
                    skipCount+=1
                    print('Skip Vote by `'+message.author.name+'` to a total of `'+str(skipCount)+'/'+str(skipsRequired)+'`')
                else:
                    print('already voted to skip')
                if skipCount >= skipsRequired:
                    skipperlist = []
                    skipCount = 0
                    option = 'skip'
            else:
                playlist.append(msg)
                fixPlaylist()
            yield from asyncio.sleep(5)
            try:
                yield from client.delete_message(message)
            except:
                print('Couldn\'t delete message for some reason')
            if sendmsg is True:
                sendmsg = False
                yield from asyncio.sleep(10)
                yield from client.delete_message(hotsmessage)

def is_long_member(dateJoined):
    convDT = dateJoined.date()
    today = datetime.date.today()
    optDays = option[1]
    margin = datetime.timedelta(days = int(options[1]))
    return today - margin > convDT

def fixPlaylist():
    for things in playlist:
        if 'youtube' in things:
            if '&' in things:
                substrStart = things.find('&')
                fixedThings = things[ :substrStart]
                fixedThings.strip()
            else:
                fixedThings = things
        else:
            fixedThings = things
        options = {
                'format': 'bestaudio/best',
                'extractaudio' : True,
                'audioformat' : "mp3",
                'outtmpl': '%(id)s',
                'noplaylist' : True,
                'nocheckcertificate' : True,}
        ydl = youtube_dl.YoutubeDL(options)
        try:
            info = ydl.extract_info(fixedThings, download=False)
        except Exception as e:
            while fixedThings in playlist: playlist.remove(fixedThings)

def getPlaylist():
    endmsg = ''
    count = 0
    for things in playlist:
        if 'youtube' in things:
            if '&' in things:
                substrStart = things.find('&')
                fixedThings = things[ :substrStart]
                fixedThings.strip()
            else:
                fixedThings = things
        else:
            fixedThings = things
        options = {
                'format': 'bestaudio/best',
                'extractaudio' : True,
                'audioformat' : "mp3",
                'outtmpl': '%(id)s',
                'noplaylist' : True,
                'nocheckcertificate' : True,}
        ydl = youtube_dl.YoutubeDL(options)
        try:
            info = ydl.extract_info(fixedThings, download=False)
            title = info['title']
            
        except Exception as e:
            print("Can't access song! %s\n" % traceback.format_exc())
            title = 'ERROR: Title is actual dicks.'
        count+=1
        endmsg =endmsg +str(count) + ": "+ title + " \n"
    return endmsg

def make_savepath(title, savedir=savedir):
    return os.path.join(savedir, "%s.mp3" % (title))

def download_song(unfixedsongURL):
    global currentlyPlaying
    if 'youtube' in unfixedsongURL:
        if '&' in unfixedsongURL:
            substrStart = unfixedsongURL.find('&')
            songURL = unfixedsongURL[ :substrStart]
            songURL.strip()
        else:
            songURL = unfixedsongURL
    else:
        songURL = unfixedsongURL
    options = {
	    'format': 'bestaudio/best',
	    'extractaudio' : True,
	    'audioformat' : "mp3",
	    'outtmpl': '%(id)s',
	    'noplaylist' : True,
            'nocheckcertificate' : True,}
    ydl = youtube_dl.YoutubeDL(options)
    try:
        info = ydl.extract_info(songURL, download=False)
        title = info['title']
        currentlyPlaying = 'Now: ' + title + '\n'
        title = title.replace('/', '')
        title = title.replace('\\', '')
        savepath = make_savepath(title)
    except Exception as e:
        print("Can't access song! %s\n" % traceback.format_exc())
        return 'butts!'
    try:
        os.stat(savepath)
        return savepath
    except OSError:
        try:
            result = ydl.extract_info(songURL, download=True)
            os.rename(result['id'], savepath)
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
    global currentlyPlaying
    yield from client.wait_until_ready()
    count = 0
    time = 0
    while count!= -1:
        if isPlaying is False and firstTime is False:
            if playlist:
                vce = client.voice
                thing = playlist[0]
                try:
                    path = download_song(thing)
                    if path!='butts!':
                        player = vce.create_ffmpeg_player(path)
                        
                        player.start()
                        isPlaying = True
                        while thing in playlist: playlist.remove(thing)
                        option = 'sleep'
                    else:
                        while thing in playlist: playlist.remove(thing)
                except:
                    while thing in playlist: playlist.remove(thing)
            else:
                thing = 'https://www.youtube.com/watch?v=1VXMLuZkq1g'
                try:
                    path = download_song(thing)
                    if path!='butts!':
                        player = vce.create_ffmpeg_player(path)
                        player.start()
                        isPlaying = True
                        while thing in playlist: playlist.remove(thing)
                        option = 'sleep'
                except:
                    while thing in playlist: playlist.remove(thing)
        if option == 'sleep' or option == 'skip':
            cnt = 0
            while option!='skip' and player.is_playing():
                cnt+=1
                yield from asyncio.sleep(1)
            player.stop()
            currentlyPlaying = ''
            isPlaying = False
        else:
            yield from asyncio.sleep(1)

loop = asyncio.get_event_loop()
try:
    loop.create_task(playlist_update())
    loop.run_until_complete(client.login(options[0], options[1]))
    loop.run_until_complete(client.connect())
except Exception:
    loop.run_until_complete(client.close())
finally:
    loop.close()
