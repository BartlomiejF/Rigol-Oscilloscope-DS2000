"""The program is going to control and obtain data ion mobility spetrometer and save it to excel files"""

import instrument, openpyxl, os
from tkinter import *

osc=instrument.RigolScope('/dev/usbtmc1') #for me it is usbtmc1

class LeftSide(Frame):
	"""Left side of Gui"""
	def __init__(self, master=None):
		super().__init__(master)
		self.grid(column=0, row=0, sticky=N+E+S+W)
		self.create_widgets()
		
	def create_widgets(self):
		Label(self, text=osc.name).grid(row=0, column=0)
		Button(self, text='Run', command=self.run).grid(sticky=E+W)
		Button(self, text='Stop', command=self.stop).grid(sticky=E+W)
		Button(self, text='Clear', command=self.clear).grid(sticky=E+W)
		Button(self, text='viev output', command=self.getit).grid(sticky=E+W)
		Button(self, text='Quit', command=root.destroy).grid(sticky=E+W)

	def run(self):
		osc.write(b':RUN')
	
	def getit(self):
		self.stop()
		osc.write(b':WAV:SOUR CHAN1')
		osc.write(b':WAV:MODE NORM')
		osc.write(b':WAV:DATA?')
		self.temp=osc.read(9000)
		print(self.temp.decode()) #this does not work properly
	
	def stop(self):
		osc.write(b':STOP')
		
	def clear(self):
		osc.clear_waveform()

class RightSide(Frame):
	"""this side will eventually contain some plots"""
	def __init__(self, master=None):
		super().__init__(master)
		self.grid(column=1, row=0)
		self.create_widgets()
		
		
root=Tk()
root.geometry('600x600')
LeftSide(master=root)





root.mainloop()
