"""The program is intended to make gathering measurements from Ion Mobility Spectrometer via Rigol DS2072A Oscilloscope easier.
"""

import instrument, os, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *

osc=instrument.RigolScope('/dev/usbtmc1')

class LeftSide(Frame):
	"""Left side of Gui"""
	def __init__(self, master=None):
		super().__init__(master)
		self.grid(column=0, row=0, sticky=N+E+S+W)
		self.create_widgets()
		self.data=pd.DataFrame()
		self.osx=np.ndarray(0)
		osc.write(b':WAV:SOUR CHAN1')
		osc.write(b':WAV:MODE NORM')
		osc.write(b':WAV:FORM BYTE')
		osc.write(b':WAV:YINC?')
		self.datainc=float(osc.read(300))
		osc.write(b':CHAN1:SCAL?')
		self.datascal=float(osc.read(300))
	
	def create_widgets(self):
		Label(self, text=osc.name).grid(row=0, column=0)
		Button(self, text='Run', command=self.run).grid(sticky=E+W)
		Button(self, text='Stop', command=self.stop).grid(sticky=E+W)
		Button(self, text='Clear', command=self.clear).grid(sticky=E+W)
		Button(self, text='Read time', command=self.read_time).grid(sticky=E+W)
		Button(self, text='Get data', command=lambda: PopInput(['Meas name','Submit'])).grid(sticky=E+W)
		Button(self, text='Show plot', command=self.show_plot).grid(sticky=E+W)
		Button(self, text='Save data', command=lambda: NameInput(['File name', 'Submit'])).grid(sticky=E+W)
		Button(self, text='Quit', command=root.destroy).grid(sticky=E+W)

	def run(self):
		osc.write(b':RUN')
	
	def getit(self,name):
		osc.write(b':WAV:DATA?')
		self.temp=b''
		for x in range(2):
			self.temp+=osc.read(950)
		self.tempdata=pd.DataFrame(np.frombuffer(self.temp[12:], 'B'))
		self.data[name]=(self.tempdata-float(self.tempdata.mode().iloc[0]))*self.datainc
			
	def show_plot(self):
		if not self.osx.shape[0]:
			PopInfo(text=['No data','OK'], master=root)
		else:
			self.factor=np.arange(0, 2*len(self.data.iloc[:,1:].columns), 2)
			plt.plot(self.data.iloc[:,0],(self.data.iloc[:,1:]+self.factor))
			plt.show()

	def read_time(self):
		if not self.osx.shape[0]:
			osc.write(b':WAV:XINC?')
			self.xinc=float(osc.read(300))
			osc.write(b':TIM:OFFS?')
			self.xoffs=float(osc.read(300))
			osc.write(b':WAV:POIN?')
			self.point_nr=int(osc.read(300))
			osc.write(b':TIM:SCAL?')
			self.xscal=float(osc.read(300))
			self.osx=np.arange(-(7-self.xoffs/self.xscal)*self.xscal,13*self.xscal,self.xinc)
			self.osx=self.osx[0:self.point_nr]
			self.data['time']=self.osx
	
	def stop(self):
		osc.write(b':STOP')

	def clear(self):
		osc.clear_waveform()
		
	def save_data(self, name):
		self.data.to_csv(name+'.csv')

class RightSide(Frame):
	"""this side will eventually contain some plots"""
	def __init__(self, master=None):
		super().__init__(master)
		self.grid(column=1, row=0)
		self.create_widgets()

class PopInfo(Toplevel):
	def __init__(self, text, master=None,):
		super().__init__(master)
		self.create_widgets(text)
	
	def create_widgets(self,text):
		Label(self, text=text[0]).grid(column=0, row=0)
		Button(self, text=text[1], command=self.ok).grid(column=0, row=1)
		
	def ok(self):
		self.destroy()

class PopInput(Toplevel):
	def __init__(self, text, master=None):
		super().__init__(master)
		self.create_widgets(text)
	
	def create_widgets(self,text):
		Label(self, text=text[0]).grid(column=0, row=0)
		self.colname=Entry(self)
		self.colname.grid(column=1, row = 0)
		self.colname.focus_set()
		Button(self, text=text[1], command=self.submit).grid(column=0, row=1)
		Button(self, text='Cancel', command=self.canc).grid(column=1, row=1)
		
	def submit(self):
		self.word=self.colname.get()
		menu.getit(self.word)
		self.destroy()
		
	def canc(self):
		self.destroy()

class NameInput(Toplevel):
	def __init__(self, text, master=None):
		super().__init__(master)
		self.create_widgets(text)
			
	def create_widgets(self,text):
		Label(self, text=text[0]).grid(column=0, row=0)
		self.colname=Entry(self)
		self.colname.grid(column=1, row = 0)
		self.colname.focus_set()
		Button(self, text=text[1], command=self.submit).grid(column=0, row=1)
		Button(self, text='Cancel', command=self.canc).grid(column=1, row=1)
		
	def submit(self):
		self.word=self.colname.get()
		menu.save_data(name=self.word)
		self.destroy()
		
	def canc(self):
		self.destroy()

root=Tk()
root.geometry('600x600')
menu=LeftSide(master=root)

root.mainloop()
