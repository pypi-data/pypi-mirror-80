from TikTokApi import TikTokApi
import os
import youtube_dl
from internetarchive import upload
from internetarchive import get_item
import argparse
import re
import sys
import time

def downloadTikTok(username, tiktok, cwd, sort):
    api = TikTokApi()
    try:
        tiktokID = tiktok['id']
    except:
        try:
            tiktokID = tiktok['itemInfos']['id']
        except:
            tiktokID = tiktok['itemInfo']['itemStruct']['id']
    ydl_opts = {
        'writeinfojson': True,
        'writedescription': True,
        'write_all_thumbnails': True,
        'writeannotations': True,
        'allsubtitles': True,
        'ignoreerrors': True,
        'fixup': True,
        'quiet': True,
        'no_warnings': True,
        'restrictfilenames': True,
        'outtmpl': tiktokID + '.mp4',
    }
    if (sort == True):
        if (os.path.exists('tiktok-' + username) == False):
            os.mkdir('tiktok-' + username)
        os.chdir('tiktok-' + username)
    if (os.path.exists(tiktokID) == False):
        os.mkdir(tiktokID)
    os.chdir(tiktokID)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        if (ydl.download(['https://www.tiktok.com/@' + username + '/video/' + tiktokID]) == 1):
            try:
                ydl.download([tiktok['video']['downloadAddr']])
            except:
                ydl.download(['https://www.tiktok.com/@' + username + '/video/' + tiktokID])
        else:
            ydl.download(['https://www.tiktok.com/@' + username + '/video/' + tiktokID])
    i = 0
    while (os.path.exists(tiktokID + '.mp4') != True):
        if (i == 3):
            os.chdir(cwd)
            return 'Failed!'
        print ('Couldn\'t download, trying again.')
        time.sleep(2)
        ydl.download(['https://www.tiktok.com/@' + username + '/video/' + tiktokID])
        i += 1
    x = os.listdir()
    for i in x:
        if i.endswith('.unknown_video'):
            base = os.path.splitext(i)[0]
            if (os.path.exists(base + '.mp4')):
                os.remove(base + '.mp4')
            os.rename(i, base + '.mp4')
    json = open("tiktok_info.json", "w", encoding="utf-8")
    json.write(str(tiktok))
    json.close()
    os.chdir(cwd)
    print (tiktokID + " has been downloaded.")

def uploadTikTok(username, tiktok, deletionStatus, file, sort):
    regex = re.compile('[0-9]{17}')
    regexA = re.compile('[0-9]{18}')
    regexB = re.compile('[0-9]{19}')
    regexC = re.compile('[0-9]{8}')
    regexD = re.compile('[0-9]{9}')
    if (sort == True):
        os.chdir('tiktok-' + username)
    if (os.path.isdir(tiktok) and (regex.match(str(tiktok)) or (regexA.match(str(tiktok))) or (regexB.match(str(tiktok))) or (regexC.match(str(tiktok))) or (regexD.match(str(tiktok))))):
        item = get_item('tiktok-' + tiktok)
        item.upload('./' + tiktok + '/', verbose=True, checksum=True, delete=deletionStatus, metadata=dict(collection='opensource_media', subject='tiktok', creator=username, title='TikTok Video by ' + username, originalurl='https://www.tiktok.com/@' + username + '/video/' + tiktok, scanner='TikUp 2020.09.22'), retries=9001, retries_sleep=60)
        if (deletionStatus == True):
            os.rmdir(tiktok)
        print ()
        print ('Uploaded to https://archive.org/details/tiktok-' + tiktok)
        print ()
        if file != None:
            file.write(str(tiktok))
            file.write('\n')

def downloadUser(username, limit, file, sort):
    try:
        lines = file.readlines()
        for x in range(0, len(lines) - 1):
            lines[x] = lines[x].replace('\n', '')
    except:
        lines = ''
    api = TikTokApi()
    if limit != None:
        count = int(limit)
    else:
        count = 9999
    tiktoks = api.byUsername(username, count=count)
    cwd = os.getcwd()
    ids = []
    for tiktok in tiktoks:
        if (file != None):
            if (doesIdExist(lines, tiktok['id'])):
                print (tiktok['id'] + " has already been archived.")
            else:
                status = downloadTikTok(username, tiktok, cwd, sort)
                i = 0
                if (status == 'Failed!'):
                    while (status == 'Failed!'):
                        if (i != 10):
                            print ('Trying again, again')
                            status = downloadTikTok(username, tiktok, cwd, sort)
                            i += 1
                        else:
                            status = 'Skip'
                ids.append(tiktok['id'])
        else:
            status = downloadTikTok(username, tiktok, cwd, sort)
            i = 0
            if (status == 'Failed!'):
                while (status == 'Failed!'):
                    if (i != 10):
                        print ('Trying again, again')
                        status = downloadTikTok(username, tiktok, cwd, sort)
                        i += 1
                    else:
                        status = 'Skip'
            ids.append(tiktok['id'])
        
    return ids

def downloadHashtag(hashtag, limit, file, sort):
    try:
        lines = file.readlines()
        for x in range(0, len(lines) - 1):
            lines[x] = lines[x].replace('\n', '')
    except:
        lines = ''
    api = TikTokApi()
    if limit != None:
        count = int(limit)
    else:
        count = 9999
    tiktoks = api.byHashtag(hashtag, count=count)
    usernames = []
    cwd = os.getcwd()
    for tiktok in tiktoks:
        if (doesIdExist(lines, tiktok['itemInfos']['id'])):
            print (tiktok['itemInfos']['id'] + " has already been archived.")
        else:
            username = tiktok['authorInfos']['uniqueId']
            status = downloadTikTok(username, tiktok, cwd, sort)
            i = 0
            if (status == 'Failed!'):
                while (status == 'Failed!'):
                    if (i != 10):
                        print ('Trying again, again')
                        status = downloadTikTok(username, tiktok, cwd, sort)
                        i += 1
                    else:
                        status = 'Skip'
            usernames.append(username + ':' + tiktok['itemInfos']['id'])
    return usernames

def downloadLiked(name, limit, file, sort):
    try:
        lines = file.readlines()
        for x in range(0, len(lines) - 1):
            lines[x] = lines[x].replace('\n', '')
    except:
        lines = ''
    api = TikTokApi()
    if limit != None:
        count = int(limit)
    else:
        count = 9999
    tiktoks = api.userLikedbyUsername(name, count=count)
    usernames = []
    cwd = os.getcwd()
    for tiktok in tiktoks:
        if (doesIdExist(lines, tiktok['id'])):
            print (tiktok['id'] + " has already been archived.")
        else:
            username = tiktok['author']['uniqueId']
            status = downloadTikTok(username, tiktok, cwd, sort)
            i = 0
            if (status == 'Failed!'):
                while (status == 'Failed!'):
                    if (i != 10):
                        print ('Trying again, again')
                        status = downloadTikTok(username, tiktok, cwd, sort)
                        i += 1
                    else:
                        status = 'Skip'
            usernames.append(username + ':' + tiktok['id'])
    return usernames

def doesIdExist(lines, tiktok):
    for l in lines:
        if (l == tiktok):
            return True
    return False

def getUsername(tiktokId):
    api = TikTokApi()
    thing = api.getTikTokById(tiktokId)
    try:
        return thing['itemInfo']['itemStruct']['author']['uniqueId']
    except:
        print (thing)
        sys.exit()

def getTikTokObject(tiktokId):
    api = TikTokApi()
    thing = api.getTikTokById(tiktokId)
    return thing

def main():
    os.chdir(os.path.expanduser('~'))
    if (os.path.exists('./.tikup') == False):
        os.mkdir('./.tikup')
    os.chdir('./.tikup')
    parser = argparse.ArgumentParser(description='An auto downloader and uploader for TikTok videos.')
    parser.add_argument('user')
    parser.add_argument('--no-delete', action='store_false', help="don't delete files when done")
    parser.add_argument('--hashtag', action='store_true', help="download hashtag instead of username")
    parser.add_argument('--limit', help="set limit on amount of TikToks to download")
    parser.add_argument('--use-download-archive', action='store_true', help='record the video url to the download archive. This will download only videos not listed in the archive file. Record the IDs of all downloaded videos in it.')
    parser.add_argument('--id', action='store_true', help='download this video ID')
    parser.add_argument('--liked', action='store_true', help='download the user\'s liked posts')
    parser.add_argument('--sort', action='store_true', help='sort into folders based on TikTok username')
    args = parser.parse_args()
    username = args.user
    delete = args.no_delete
    limit = args.limit
    archive = args.use_download_archive
    sort = args.sort
    if (archive == True):
        try:
            file = open('archive.txt', 'r+')
        except FileNotFoundError:
            f = open('archive.txt', 'x')
            f.close()
            file = open('archive.txt', 'r+')
    else:
        file = None
    if (args.hashtag == True): ## Download hashtag
        names = downloadHashtag(username, limit, file, sort)
        print ('')
        for name in names:
            splitName = name.split(':')
            uploadTikTok(splitName[0], splitName[1], delete, file, sort)
    elif (args.id == True): ## Download ID
        if (args.use_download_archive == True):
            lines = file.readlines()
            for x in range(0, len(lines) - 1):
                lines[x] = lines[x].replace('\n', '')
            if doesIdExist(lines, username):
                print (username + " has already been archived.")
                sys.exit()
        name = getUsername(username)
        cwd = os.getcwd()
        tiktok = getTikTokObject(username)
        status = downloadTikTok(name, tiktok, cwd, sort)
        i = 0
        if (status == 'Failed!'):
            while (status == 'Failed!'):
                if (i != 10):
                    print ('Trying again, again')
                    status = downloadTikTok(name, tiktok, cwd, sort)
                    i += 1
                else:
                    status = 'Skip'
        print ('')
        uploadTikTok(name, username, delete, file, sort)
    elif (args.liked == True): ## Download liked
        names = downloadLiked(username, limit, file, sort)
        print ('')
        for name in names:
            splitName = name.split(':')
            uploadTikTok(splitName[0], splitName[1], delete, file, sort)
    else: ## Download username
        tiktoks = downloadUser(username, limit, file, sort)
        print ('')
        for tiktok in tiktoks:
            uploadTikTok(username, tiktok, delete, file, sort)
    try:
        file.close()
    except:
        pass
    print('')

if __name__ == "__main__":
    main()
