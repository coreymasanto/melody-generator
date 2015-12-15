from collections import defaultdict
from midiutil.MidiFile import MIDIFile
import nltk
from nltk.corpus import brown
from nltk.util import ngrams
import random
import re
import sys

def main():
        # Open training file
	print("Reading notes from corpus files...")
	notesFilePath = "corpus/MichaelJacksonNotes.txt"
	notesFile = open(notesFilePath, 'r')
        notes = getTokensFromFile(notesFile)

        print("Creating unary transition matrix...")
        unaryTransitionMatrix = getUnaryTransitionMatrix(notes)

        print("Creating binary transition matrix...")
        binaryTransitionMatrix = getBinaryTransitionMatrix(notes)

        print("Creating ternary transition matrix...")
        ternaryTransitionMatrix = getTernaryTransitionMatrix(notes)

        print("Generating verse notes...")
        vn1 = 61
        vn2 = 61
        vn3 = 61
        verseList = generateVerse(unaryTransitionMatrix, binaryTransitionMatrix, ternaryTransitionMatrix, vn1, vn2, vn3)

        print("Generating chorus notes...")
        cn1 = 61
        cn2 = 56
        cn3 = 68
        chorusList = generateChorus(unaryTransitionMatrix, binaryTransitionMatrix, ternaryTransitionMatrix, cn1, cn2, cn3)

        print("Generating bridge notes...")
        bn1 = 57
        bn2 = 69
        bn3 = 61
        bridgeList = generateBridge(unaryTransitionMatrix, binaryTransitionMatrix, ternaryTransitionMatrix, bn1, bn2, bn3)

        print("Creating MIDI file...")
        songList = getSongList(verseList, chorusList, bridgeList)
        
        # Create the MIDIFile Object with 1 track
        song = MIDIFile(1)
        
        # Tracks are numbered from zero. Times are measured in beats.
        track = 0
        time = 0

        # Add track name and tempo.
        song.addTrackName(track, time, "Generated Song")
        song.addTempo(track, time, 240)
        
        for note in songList:
                track = 0
                channel = 0
                duration = random.randint(1, 4)
                noteIsSilent = note == -1
                if not noteIsSilent:
                        pitch = note
                        volume = 100
                else:
                        pitch = 0
                        volume = 0
                song.addNote(track, channel, pitch, time, duration, volume)
                time += 1

        # Write it to disk.
        binfile = open("output.mid", 'wb')
        song.writeFile(binfile)
        binfile.close()

	print("Program complete.")		   



def getTokensFromFile(notesFile):
        text = notesFile.read()
        tokens = text.split('\n')
        notes = []
        for t in tokens:
                if len(t) > 0 and t[0] != '#':
                        notes.append(int(t))
        return notes



def getUnaryTransitionMatrix(tokens):
        unaryTransitionMatrix = {}
        for (t1, t2) in ngrams(tokens, 2):
                if t1 not in unaryTransitionMatrix:
                        unaryTransitionMatrix[t1] = [] 
                unaryTransitionMatrix[t1].append(t2)
        return unaryTransitionMatrix


def getBinaryTransitionMatrix(tokens):
        binaryTransitionMatrix = {}
        for (t1, t2, t3) in ngrams(tokens, 3):
                if (t1, t2) not in binaryTransitionMatrix:
                        binaryTransitionMatrix[(t1, t2)] = [] 
                binaryTransitionMatrix[(t1, t2)].append(t3)
        return binaryTransitionMatrix



def getTernaryTransitionMatrix(tokens):
        ternaryTransitionMatrix = {}
        for (t1, t2, t3, t4) in ngrams(tokens, 4):
                if (t1, t2, t3) not in ternaryTransitionMatrix:
                        ternaryTransitionMatrix[(t1, t2, t3)] = [] 
                ternaryTransitionMatrix[(t1, t2, t3)].append(t4)
        return ternaryTransitionMatrix



# Generate 4 groups of 8 notes, each separated by a half-rest
def generateVerse(unaryTransitionMatrix, binaryTransitionMatrix, ternaryTransitionMatrix, firstNote, secondNote, thirdNote):
        verse = [firstNote, secondNote, thirdNote]
        for line in range(4):
                for note in range(8):
                        bestNote = nextNote(unaryTransitionMatrix, binaryTransitionMatrix, ternaryTransitionMatrix, firstNote, secondNote, thirdNote)
                        verse.append(bestNote)
                        firstNote = secondNote
                        secondNote = thirdNote
                        thirdNote = bestNote
                for rest in range(2):
                        verse.append(-1)
        return verse


        
# Generate 4 groups of 8 notes, each separated by a half-rest
def generateChorus(unaryTransitionMatrix, binaryTransitionMatrix, ternaryTransitionMatrix, firstNote, secondNote, thirdNote):
        chorus = [firstNote, secondNote, thirdNote]
        for line in range(4):
                for note in range(8):
                        bestNote = nextNote(unaryTransitionMatrix, binaryTransitionMatrix, ternaryTransitionMatrix, firstNote, secondNote, thirdNote)
                        chorus.append(bestNote)
                        firstNote = secondNote
                        secondNote = thirdNote
                        thirdNote = bestNote
                for rest in range(2):
                        chorus.append(-1)
        return chorus



def generateBridge(unaryTransitionMatrix, binaryTransitionMatrix, ternaryTransitionMatrix, firstNote, secondNote, thirdNote):
        bridge = [firstNote, secondNote, thirdNote]
        for line in range(4):
                for note in range(8):
                        bestNote = nextNote(unaryTransitionMatrix, binaryTransitionMatrix, ternaryTransitionMatrix, firstNote, secondNote, thirdNote)
                        bridge.append(bestNote)
                        firstNote = secondNote
                        secondNote = thirdNote
                        thirdNote = bestNote
        return bridge



def nextNote(unaryTransitionMatrix, binaryTransitionMatrix, ternaryTransitionMatrix, n1, n2, n3):
        if (n1, n2, n3) in ternaryTransitionMatrix.keys():
                possibleNotes = ternaryTransitionMatrix[(n1, n2, n3)]
        elif (n2, n3) in binaryTransitionMatrix:
                possibleNotes = binaryTransitionMatrix[(n2, n3)]
        else:
                possibleNotes = unaryTransitionMatrix[n3]
        return random.choice(possibleNotes)



def getSongList(verseList, chorusList, bridgeList):
        return verseList + chorusList + verseList + chorusList + bridgeList + chorusList



main()

