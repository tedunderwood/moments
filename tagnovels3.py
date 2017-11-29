#!/usr/bin/env python3

# Note that this script is not designed to be portable.
# We don't expect people to replicate the whole data-
# *generation* process. Someone willing to put that much
# work in would be better advised to write their own
# paper.

# For that reason, file paths are absolute rather than relative.
# This code *documents* what we did, but it's not code that we
# are trying to make executable for other researchers.

import csv, os, sys, random, json
from collections import Counter
import numpy as np
import pandas as pd

# import utils
currentdir = os.path.dirname(__file__)
libpath = os.path.join(currentdir, '../lib')
sys.path.append(libpath)

endstops = {'.', '!', '?', '"'}
def endstopped(word):
    global endstops

    for stop in endstops:
        if word.strip().endswith(stop):
            return True
    return False

def closest_value(alist, target):

    min_index, min_value = min(enumerate(alist), key = lambda x: abs(target - x[1]))

    return min_index, min_value


def split_text(linelist):
    '''
    The goal here is to produce a sequence of ~250-word chunks, roughly
    equal size, but dividing at sentence or preferably paragraph breaks.
    '''

    linewordctr = 0

    paragraphbreaks = []
    sentencebreaks = []
    allwords = []

    for line in linelist:
        line = line.replace('  ', ' ')
        line = line.replace('<pb>\n', '').replace(' \n', '\n').strip(' ')
        # get rid of my pagebreak tags, if they're present

        if len(line) < 1:
            continue
        words = line.split(' ')
        # Notice that we are not splitting or eliminating newline characters.
        for idx, word in enumerate(words):
            if endstopped(word):
                sentencebreaks.append(linewordctr + idx + 1)
                if idx + 1 >= len(words):
                    paragraphbreaks.append(linewordctr + idx + 1)

        linewordctr = linewordctr + len(words)
        allwords.extend(words)

    totalwords = linewordctr
    wordctr = 0
    chunks = []

    while (wordctr + 1) < len(allwords):
        target = wordctr + 250
        min_index, min_value = closest_value(paragraphbreaks, target)
        if min_value > wordctr and (min_value - target) < 100 and (min_value - target) > -75:
            chunks.append(allwords[wordctr : min_value])
            wordctr = min_value
        else:
            min_index, min_value = closest_value(sentencebreaks, target)
            if min_value > wordctr and abs(min_value - target) < 100:
                chunks.append(allwords[wordctr : min_value])
                wordctr = min_value
            else:
                next_value = wordctr + 250
                if next_value > len(allwords):
                    next_value = len(allwords)
                chunks.append(allwords[wordctr : next_value])
                wordctr = next_value

    if len(chunks[-1]) < 100:
        # if the last chunk is a little trailing thing
        runt = chunks.pop(-1)
        # pop off the runt
        chunks[-1].extend(runt)
        # and put it on the end of the new last chunk

    # That's a bit of a kludge. Side-effect of my sloppy algorithm
    # is, sometimes getting a (near-)empty last chunk.

    segments = []
    ctr = 0
    for chunk in chunks:
        segments.append(' '.join(chunk))

    return segments

def parsetime(phrase):
    ''' Returns a time in minutes. If the phrase is not a legal time
    expression, returns -1. Seconds, hours, days, weeks, and years are
    converted into minute values.
    '''

    timecodes = {'s': 0.01666, 'm': 1, 'h': 60, 'd': 1440, 'w': 10080, 'y': 525600}

    phrase = phrase.strip()

    if len(phrase) < 2:
        print('Answer must be longer.')
        return -1
    if not phrase[0].isdigit():
        print('Answer must begin with a number.')
        return -1
    if not phrase[-1] in timecodes:
        print('End with (s)econds, (m)inutes, (h)ours, (d)ays, (w)eeks, or (y)ears.')
        return -1

    multiplier = timecodes[phrase[-1]]
    numericpart = ''
    for character in phrase:
        if character.isdigit() or character == '.':
            numericpart = numericpart + character

    try:
        time = float(numericpart) * multiplier
    except:
        print('Mysterious problem with your number.')
        time = -1

    return time

def get_ellipsis():
    ellipsistime = -1
    while ellipsistime < 0:
        user = input("How much time passes in ellipsis? ")
        ellipsistime = parsetime(user)
    ellipsisphrase = input("Any phrase flagging ellipsis: ")

    return ellipsistime, ellipsisphrase

def get_subjective():
    subjectivetime = -1
    while subjectivetime < 0:
        user = input("How much time traversed by memory or anticipation? ")
        subjectivetime = parsetime(user)
    subjectivephrase = input("Any phrase flagging subjectivity: ")

    return subjectivetime, subjectivephrase

def print_as_lines(text):
    justskippedline = False
    lines = text.split('\n')
    for line in lines:
        words = line.split()
        if len(words) > 18:
            for floor in range(0, len(words), 18):
                ceiling = floor + 18
                if ceiling > len(words):
                    ceiling = len(words)
                print(' '.join(words[floor: ceiling]))
            justskippedline = False
        else:
            if not justskippedline or len(line) > 2:
                print(line)
                justskippedline = True


def query_segments(segments, chunks, maxchunk):
    ''' Iterates through segments getting information about time.
    '''
    print("Enter 'stop' at any time to stop and save work on this file.")
    print("Enter 'other:' followed by a one-word explanation if something")
    print("weird happens. E.g. 'other: dedication'.")
    stopwork = False

    for segment in segments:
        idx = segment['idx']
        print('SEGMENT ' + str(idx))

        if segment['complete']:
            print('complete')
            continue
        # If the segment has already been completed,
        # we'll print the index and move on to the next.

        print_as_lines(segment['text'])
        wordct = len(segment['text'].split())
        print(str(wordct) + ' words.')

        haveanswer = False

        while not haveanswer:
            narratedtime = 0
            ellipsistime = 0
            subjectivetime = 0
            ellipsisphrase = ''
            subjectivephrase = ''
            otherflag = ''
            ell = False
            subj = False

            user = input('Narrated time? ')
            user = user.strip()

            if 'stop' in user or 'quit' in user:
                stopwork = True
                haveanswer = True
                break

            elif 'other' in user:
                otherflag = user
                subjectivephrase = user
                haveanswer = True

            elif 'ell' in user:
                ellipsistime, ellipsisphrase = get_ellipsis()
                ell = True

            elif 'subj' in user:
                subjectivetime, subjectivephrase = get_subjective()
                subj = True

            if subj or ell:
                while not haveanswer:
                    user = input('Actual narrated time, outside of minds and ellipses? ')
                    narratedtime = parsetime(user)
                    if narratedtime > -1:
                        haveanswer = True

            if len(user) < 1:
                continue

            if user.isdigit():
                try:
                    segtoprint = int(user)
                except:
                    print("Tried and failed to interpret that as a segment number.")
                    segtoprint = -1

                if segtoprint > -1 and segtoprint < maxchunk:
                    print("Printing segment " + str(segtoprint))
                    print(chunks[segtoprint])
                    print()
                    print('Still need answer for segment ' + str(idx))

            else:
                if not haveanswer:
                    narratedtime = parsetime(user)
                    if narratedtime > -1:
                        haveanswer = True

        # Now that the question has been answered we can package it up as a json object.

        if not stopwork:
            for key in ['narratedtime', 'ellipsistime', 'subjectivetime', 'ellipsisphrase', 'subjectivephrase']:
                segment[key] = locals()[key]
                segment['complete'] = True
            print(str(narratedtime) + " minutes narrated time.")
        else:
            break

    return segments

def select_segments(chunks):
    ''' Accepts a sequence of text chunks, selects random chunks — plus
    the first two and last — and turns these selected chunks into
    "segment objects" that contain the chunk text along with other info.
    '''
    segindexes = [x for x in range(len(chunks))]
    if len(segindexes) < 16:
        segmentstocheck = segindexes
    else:
        segmentstocheck = []
        segmentstocheck.extend([0, 1])
        # add the first two chunks
        segmentstocheck.extend(segindexes[-2 : ])
        # and the last two chunks

        segmentstocheck.extend(random.sample(segindexes[2: -2], 12))
        # and twelve randomly selected chunks in-between

    # Okay, now let's construct segments.
    segmentstocheck.sort()
    segmentobjects = []

    for idx in segmentstocheck:
        segment = dict()
        segment['complete'] = False
        segment['text'] = chunks[idx]
        segment['idx'] = idx
        segmentobjects.append(segment)

    return segmentobjects

def check_files(metadatapath, filepath, jsonpath):
    files = []
    metadata = dict()
    with open(metadatapath, encoding = 'utf-8') as f:
        reader = csv.DictReader(f)
        notfound = 0
        for row in reader:
            filename = row['docid'] + '.txt'
            thispath = os.path.join(filepath, filename)
            if os.path.isfile(thispath):
                files.append(filename)
                metadata[filename] = row
            else:
                print(thispath + " not found on disk.")
                notfound += 1

    if os.path.isfile(jsonpath):
        with open(jsonpath, encoding = 'utf-8') as f:
            thestring = f.read()
        with open('backup.json', mode = 'a', encoding = 'utf-8') as f:
            f.write(thestring + '\n')

        jsonobject = json.loads(thestring)
    else:
        jsonobject = dict()

    fullytagged = []
    inprocess = []
    notstarted = []

    for filename in files:
        if filename not in jsonobject:
            notstarted.append(filename)
        else:
            filedata = jsonobject[filename]
            segments = filedata['segments']
            complete = True
            for seg in segments:
                if seg['complete'] == False:
                    complete = False

            if complete:
                fullytagged.append(filename)
            else:
                inprocess.append(filename)

    print()
    print("I matched the files in " + metadatapath)
    print(str(notfound) + " were not found in " + filepath)
    print("Of those found, " + str(len(fullytagged)) + " were completely tagged,")
    print("while " + str(len(notstarted)) + " have yet to be tagged, and")
    print(str(len(inprocess)) + " were in process.")
    print()
    if (len(inprocess) + len(notstarted)) > 0:
        print("Which do you want to work on? ")
        print("Not yet tagged:")
        i = 1
        choicedict = dict()
        for filename in notstarted:
            print(str(i) + ") " + filename)
            choicedict[i] = filename
            i += 1
        print()
        if len(inprocess) > 0:
            print("In process: ")
            for filename in inprocess:
                print(str(i) + ") " + filename)
                choicedict[i] = filename
                i += 1
        print()
        chosen = False
        while not chosen:
            user = input("Number of your choice (or 'stop' to quit): ")
            if user == 'stop' or user == 'quit':
                return
            elif not user.isdigit():
                print('Not a valid number.')
                continue

            user = int(user)
            if user < 1 or user + 1 > i:
                print("Number outside range of choices.")
                continue
            else:
                filename = choicedict[user]
                chosen = True

        print()
        print("You have decided to work on " + filename)
        print()
        # If it's a valid integer, read the selected file.
        if filename in inprocess:
            path = os.path.join(filepath, filename)
            with open(path, encoding = 'utf-8') as f:
                lines = f.readlines()
            chunks = split_text(lines)
            maxchunk = jsonobject[filename]['chunkct']
            jsonobject[filename]['segments'] = query_segments(jsonobject[filename]['segments'], chunks, maxchunk)
        elif filename in notstarted:
            path = os.path.join(filepath, filename)
            with open(path, encoding = 'utf-8') as f:
                lines = f.readlines()
            chunks = split_text(lines)
            jsonobject[filename] = dict()
            jsonobject[filename]['segments'] = select_segments(chunks)
            jsonobject[filename]['chunkct'] = len(chunks)
            jsonobject[filename]['metadata'] = metadata[filename]
            jsonobject[filename]['segments'] = query_segments(jsonobject[filename]['segments'], chunks, len(chunks))
        else:
            print("This is an error statement that should not be reached.")

        thestring = json.dumps(jsonobject)
        with open(jsonpath, mode = 'w', encoding = 'utf-8') as f:
            f.write(thestring)

    # End of this function.


# START MAIN
args = sys.argv
print(len(args))
if len(args) < 4:
    print('Tagnovels expects to be called with a command of this form:')
    print()
    print('python3 tagnovels.py metadatafile.csv textfolder jsonfile.json')
else:
    metadatafile = args[1]
    textfolder = args[2]
    jsonoutput = args[3]

    user = 'y'
    while user != 'n':
        check_files(metadatafile, textfolder, jsonoutput)
        user = input('Tag another volume? (y/n)')











