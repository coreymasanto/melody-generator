from collections import defaultdict
from midiutil.MidiFile import MIDIFile
import nltk
from nltk.corpus import brown
import random
import re
import sys

def main():
        # Open training file
	print("Reading corpus files...")
	notesFilePath = "corpus/MichaelJacksonNotes.txt"
	notesFile = open(notesFilePath, 'r')
	
        notes = getTokensFromFile(notesFile)
        print(notes)

        print("Creating transition matrix...")
        transitionMatrix = getTransitionMatrix(notes)

        print("Generating verse notes...")
        verseFirstNote = 61
        verseSecondNote = 61
        verseList = generateVerse(transitionMatrix, verseFirstNote, verseSecondNote, notes)

        print("Generating chorus notes...")
        chorusFirstNote = 57
        chorusSecondNote = 56
        chorusList = generateChorus(transitionMatrix, chorusFirstNote, chorusSecondNote, notes)

        print("Generating bridge notes...")
        bridgeFirstNote = 68
        bridgeSecondNote = 69
        bridgeList = generateBridge(transitionMatrix, bridgeFirstNote, bridgeSecondNote, notes)

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
                if note >= 0:
                        pitch = note
                        volume = 100
                else:  # Values of -1 (i.e., rests)
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



def getTransitionMatrix(tokens):
        transitionMatrix = {}
        for (t1, t2, t3) in nltk.trigrams(tokens):
                if (t1, t2) not in transitionMatrix:
                        transitionMatrix[(t1, t2)] = [] 
                transitionMatrix[(t1, t2)].append(t3)
        return transitionMatrix



# Generate 4 groups of 8 notes, each separated by a half-rest
def generateVerse(transitionMatrix, firstNote, secondNote, tokens):
        verse = [firstNote, secondNote]
        for line in range(4):
                for note in range(8):
                        bestNote = nextNote(transitionMatrix, firstNote, secondNote, tokens)
                        verse.append(bestNote)
                        firstNote = secondNote
                        secondNote = bestNote
                for rest in range(2):
                        verse.append(-1)
        return verse


        
# Generate 4 groups of 8 notes, each separated by a half-rest
def generateChorus(transitionMatrix, firstNote, secondNote, tokens):
        chorus = [firstNote, secondNote]
        for line in range(4):
                for note in range(8):
                        bestNote = nextNote(transitionMatrix, firstNote, secondNote, tokens)
                        chorus.append(bestNote)
                        firstNote = secondNote
                        secondNote = bestNote
                for rest in range(2):
                        chorus.append(-1)
        return chorus



def generateBridge(transitionMatrix, firstNote, secondNote, tokens):
        bridge = [firstNote, secondNote]
        for line in range(4):
                for note in range(8):
                        bestNote = nextNote(transitionMatrix, firstNote, secondNote, tokens)
                        bridge.append(bestNote)
                        firstNote = secondNote
                        secondNote = bestNote
        return bridge



def nextNote(transitionMatrix, n1, n2, notes):
        if (n1, n2) in transitionMatrix.keys():
                possibleNotes = transitionMatrix[(n1, n2)]
        else:
                possibleNotes = []
        return random.choice(possibleNotes) if len(possibleNotes) > 0 else random.choice(notes)



def getSongList(verseList, chorusList, bridgeList):
        return verseList + chorusList + verseList + chorusList + bridgeList + chorusList



main()

