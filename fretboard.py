#!/usr/bin/python

import sys
import svgwrite
from svgwrite import cm
import argparse
from argparse import RawTextHelpFormatter

class Fretboard:
	def __init__(self, filename, notes, string_spacing=1, string_names="E,A,D,G,B,E", frets=24, fret_spacing=2,  start=(1,1), fret_numbers=[1,3,5,7,9,12,15,17,19,21,24], size=(u'100%', u'100%'), scale=1):
		self.filename = filename
		if self.filename[:-4] != ".svg":
			self.filename = self.filename + ".svg"
		self.frets = frets + 1
		self.start = start
		self.string_spacing = string_spacing * scale
		self.fret_spacing = fret_spacing * scale
		sl = list(string_names.split(","))
		sl.reverse()
		self.string_names = sl
		self.strings = len(self.string_names) + 1
		self.fret_numbers = fret_numbers
		self.svg = svgwrite.Drawing(self.filename, size=size, profile='tiny')
		self.notes = list(notes.split(","))
		self.all_notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

	def drawFretboard(self):#dwg, strings, string_spacing, string_names, frets, fret_spacing, fret_numbers, start_x, start_y):
		start_text_x = self.start[0]
		start_text_y = self.start[1]
		start_x = self.start[0] + 1
		start_y = self.start[1] + 1

		hlines = self.svg.add(self.svg.g(id='vline', stroke='black'))
		for y in range(self.strings):
			if y == self.strings-1:
				continue
			hlines.add(self.svg.line(start=(start_x*cm, (start_y + y * self.string_spacing)*cm), end=((start_y + (self.frets-1)*self.fret_spacing)*cm, (start_y + y)*cm)))

		vlines = self.svg.add(self.svg.g(id='vline', stroke='black'))
		# draw the 0 fret
		vlines.add(self.svg.line(start=((start_x)*cm, start_y*cm), end=(start_x*cm, self.strings*self.string_spacing*cm)))
		vlines.add(self.svg.line(start=((start_x + 0.1)*cm, start_y*cm), end=((start_x + 0.1)*cm, self.strings*self.string_spacing*cm)))
		# draw the rest of the self.frets
		for x in range(self.frets):
			vlines.add(self.svg.line(start=((start_x + x * self.fret_spacing)*cm, start_y*cm), end=((start_x + x * self.fret_spacing)*cm, self.strings*self.string_spacing*cm)))

		# draw string names
		paragraph = self.svg.add(self.svg.g(font_size=1*cm))
		for y in range(len(self.string_names)):
			c = self.string_names[y]
			paragraph.add(self.svg.text(c, (start_text_x * cm, (start_text_y + y + 1 + 0.3) * self.string_spacing * cm)))

		# draw fret numbers
		numbers = self.svg.add(self.svg.g(font_size=1*cm))
		for x in range(self.frets):
			if x not in self.fret_numbers:
				continue
			if x < 10:
				offset = 0
			else:
				offset = -0.25
			numbers .add(self.svg.text(str(x), ((start_text_x + offset + x * self.fret_spacing ) * cm, (self.strings + 1) * self.string_spacing * cm)))

	def drawNotes(self):
		notes = self.svg.add(self.svg.g(id='shapes', fill='black'))
		note_names = self.svg.add(self.svg.g(font_size=0.25*cm))
		start_x = self.start[0] + 1
		start_y = self.start[1] + 1
		for y in range(self.strings):
			if y == self.strings-1:
				continue
			start_note = self.string_names[y]
			for x in range(self.frets):
				if (x == 0):
					offset = 0
				else:
					offset = -self.fret_spacing/2
				x_note = x + self.all_notes.index(start_note)
				while x_note >= len(self.all_notes):
					x_note = x_note - len(self.all_notes)
				x_note = self.all_notes[x_note]
				try:
					self.notes.index(x_note)
					notes.add(self.svg.circle(center=((start_x + offset + x * self.fret_spacing)*cm, (start_y + y)*cm), r='.25cm', stroke='black', stroke_width=3))
					note_names.add(self.svg.text(x_note, ((start_x + offset + (x - 0.05) * self.fret_spacing)*cm, (start_y + y+0.05)* cm), fill='white'))
				except ValueError,IndexError:
					blah = 0 # ;]


	def draw(self):
		self.drawFretboard()
		self.drawNotes()

	def save(self):
		self.svg.save()

	def render(self):
		self.draw()
		self.save()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description="fretboard.py.\n(c) Juergen Legler",
		formatter_class=RawTextHelpFormatter)

	parser.add_argument('--strings', help='set strings. "E,A,D,G,B,E" by default')
	parser.add_argument('--notes', help='set notes. "C,D,E,F,G,A,B" by default')
	parser.add_argument('--frets', help='set amount of frets. 24 by default')
	parser.add_argument('--filename', help='set filename. "C_Major" by default')
	args = parser.parse_args()
	if not len(sys.argv):
		print "generating default c major fretboard"
		fretboard = Fretboard("C_Major", "C,D,E,F,G,A,B")
	else:
		if not args.filename:
			print "You need to supply a filename"
			exit()
		kwargs = {}
		if args.strings:
			kwargs['string_names'] = args.strings
		if args.frets:
			kwargs['frets'] = args.frets
		fretboard = Fretboard(args.filename, args.notes if args.notes else "C,D,E,F,G,A,B", **kwargs)
	fretboard.render()
