# Would not have been possible without /u/sjrsimac
#    https://www.reddit.com/r/RequestABot/comments/6xhfmk/would_like_a_bot_to_monitor_the_various_free/dmvk8xp/
import praw
import zlib
import base64
import json
import time

def getModeratorIndex(r,sub,mod):
    '''
    Get Index of a specific moderator in the list, adds mod to the list if he isn't
            there already

    Paramaters
    ----------
    r : Reddit
        Reddit instance (praw) that we will be using to access the wiki
    sub : str
        Name of the subreddit to fetch the mod index from
    mod : str
        Name of the moderator who's index we are fetching

    Returns
    -------
    int
        Index of the moderator in the list
    '''
    try:
        x = PullandUnzipUsernotes(r,sub)[0]['constants']['users'].index(mod)
        return x
    except ValueError:
        all_usernotes = PullandUnzipUsernotes(r,sub)
        # If there are no mods, place the mod into the list
        all_usernotes[0]['constants']['users'][0] = mod
        # Write that to the usernote file before we do anything else in the program
        CompileandZipUsernotes(r, all_usernotes, all_usernotes[1], sub):
        # Since the mod will be the first in the list, we can return 0 instead of
        #     Calling the function again, which could create a memory leak if something went very wrong.
        return 0

def getWarningIndex(r,sub,warning):
    '''
    Get index of the specific warning in the list
    IF YOU WANT THIS TO WORK IN YOUR SUBREDDIT EDIT THE NULL VALUE APROPRIATELY

    Paramaters
    ----------
    r : Reddit
        Reddit instance (praw) that we will be using to access the wiki
    sub : str
        Name of the subreddit to fetch the mod index from
    warning : str
        warning for which to fetch the index for

    Returns
    -------
    int
        Index of the warning in the list, null if it isn't there
    '''
    # Not conditioned to deal with a warning bla bla bla ^^^
	thing_list = PullandUnzipUsernotes(r,sub)[0]['constants']['warnings']

    # Since UserNotes is meant to deal with javascript, I cannot write null as a code,
    #       Python uses None. Javascript will not recognize None as null. Python will
    #       not recognize null as None. Kind of at a loss here

    # Find the index of null in your usernotes, change this to that index
    null_code = 3

	val = thing_list.index(warning) if warning in thing_list else null_code
    return val

# Huge thanks to /u/sjrsimac for the below code

def makeNewNote(blob, redditor, notetext, moderatornumber, link, warningNumber):
    newnote = {
    'n':notetext, # The displayed note.
    't':int(time.time()), # The time the note is made.
    'm':moderatornumber, # The moderator number that made the note.
    'l':link, # The attached link, which will be blank for now.
    'w':warningNumber # The warning number.
    }
    try:
        blob[redditor]['ns'] = [newnote] + blob[redditor]['ns']
    except:
        blob[redditor] = {'ns':list()}
        blob[redditor]['ns'] = [newnote]
    return blob

def PullandUnzipUsernotes(reddit, OurSubreddit):
    # Extract the whole usernotes page and turns it into a dictionary.
    allusernotes = json.loads(reddit.subreddit(OurSubreddit).wiki['usernotes'].content_md)
    # Get the blob in the usernotes and convert the base64 number into a binary (base2) number.
    blob = base64.b64decode(allusernotes['blob'])
    # Convert the blob binary number into a string.
    blob = zlib.decompress(blob).decode()
    # Convert blob string into a dictionary.
    blob = json.loads(blob)

    # Print the blob in a user readable form.
    # print(blob)

    return [allusernotes, blob]

def CompileandZipUsernotes(reddit, allusernotes, blob, ourSubreddit):
    # This is the debugging code. Disable or delete this when you're done debugging.
    # print(allusernotes)
    # print(blob)

    blob = json.dumps(blob)
    blob = blob.encode()
    blob = zlib.compress(blob)
    rewrittenblob = base64.b64encode(blob).decode()
    allusernotes['blob'] = str(rewrittenblob)
    allusernotes = json.dumps(allusernotes)
    reddit.subreddit(ourSubreddit).wiki['usernotes'].edit(allusernotes)
