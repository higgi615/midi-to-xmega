#!/usr/bin/env python
"""
Open a MIDI file and print every message in every track.

Support for MIDI files is still experimental.
"""
import sys
from mido import MidiFile

class Note:
	def __init__(self, note_num, time):
		Note.time = time
		if note_num == "rest":
			Note.freq = 0
			return
		octave = note_num // 12
		n = note_num % 12
		if n == 0:
			Note.period = 1046.5
		elif n == 1:
			Note.period = 1108.73
		elif n == 2:
			Note.period = 1174.66
		elif n == 3:
			Note.period = 1244.51
		elif n == 4:
			Note.period = 1318.51
		elif n == 5:
			Note.period = 1396.91
		elif n == 6:
			Note.period = 1479.98
		elif n == 7:
			Note.period = 1567.98
		elif n == 8:
			Note.period = 1661.22
		elif n == 9:
			Note.period = 1760.00
		elif n == 10:
			Note.period = 1864.66
		elif n == 11:
			Note.period = 1975.53
		#Adjust the Freq
		while octave > 6:
			Note.period *= 2
			octave -= 1
		while octave < 6:
			Note.period /= 2
			octave += 1
		Note.freq = 1 / Note.period


if __name__ == '__main__':
	filename = sys.argv[1]

	midi_file = MidiFile(filename)
	PPQ = midi_file.ticks_per_beat
	BPM = 120

	notes = []

	for i, track in enumerate(midi_file.tracks):
		#sys.stdout.write('=== Track {}\n'.format(i))
		for message in track:
			#print(message.__dict__.keys())
			#print(message)
			note = None
			if 'note' in message.__dict__ and message.time != 0:
				# print (message)
				# print('Note: ', message.note, "\t", end="")
				#print('Time: ', message.time, end="\t")
				if message.type == 'note_on':
					note = Note("rest", message.time)
				else:
					note = Note(message.note, message.time)
				# print('Freq: ', note.freq)
				# 60000 / (BPM * PPQ)
				#notes.append(note)
			elif message.type == "control_change" and message.time != 0:
				note = Note("rest", message.time)

			if note != None:
				print('{', note.freq, ', ', (60000 / (BPM * PPQ)) * note.time, '},', sep="")

	#for note in notes:
		#print('{', note.period, ', ', note.time, '},', sep="")
