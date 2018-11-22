import instrument, os, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from mpl_toolkits.mplot3d import Axes3D
from tkinter import ttk
from scipy.signal import find_peaks



class LeftSide(Frame):
	"""Left side of Gui"""
	def __init__(self, master=None):
		super().__init__(master)
		self.grid(column=0, sticky=N+E+S+W)
		self.columnconfigure(0,weight=1)
		self.columnconfigure(1,weight=1)
		self.data=pd.DataFrame()
		osc.write(b':WAV:SOUR CHAN1')
		osc.write(b':WAV:MODE NORM')
		osc.write(b':WAV:FORM BYTE')
		osc.write(b':WAV:YINC?')
		self.datainc=float(osc.read(300))
		osc.write(b':CHAN1:SCAL?')
		self.datascal=float(osc.read(300))
		self.read_time()

		self.create_widgets()
	
	def create_widgets(self):
		Label(self, text=osc.name).grid(row=0, columnspan=2)
		""" Menu Labelframe"""
		self.menFrame=LabelFrame(self, text='Menu')
		self.menFrame.grid(column=0, row=1, sticky=N+S+E+W,pady=10)
		self.menFrame.columnconfigure(0,weight=1)
		
		#menu notebook
		self.menuNB=ttk.Notebook(self.menFrame)
		self.menuNB.grid(sticky=E+W, pady=10)
		
		#scope controls
		self.scopecontrols=ttk.Frame(self.menuNB)
		self.scopecontrols.columnconfigure(0,weight=1)
		self.menuNB.add(self.scopecontrols, text='Scope controls')
		Button(self.scopecontrols, text='Run', command=self.run).grid(sticky=E+W, padx=10)
		Button(self.scopecontrols, text='Stop', command=self.stop).grid(sticky=E+W, padx=10)
		Button(self.scopecontrols, text='Clear', command=self.clear).grid(sticky=E+W, padx=10)
		Button(self.scopecontrols, text='Set averages number', command=lambda: AvgPop(['Averages number:','OK'])).grid(sticky=E+W, padx=10)
		
		#program & data controls
		self.progdatacontrols=ttk.Frame(self.menuNB)
		self.progdatacontrols.columnconfigure(0,weight=1)
		self.menuNB.add(self.progdatacontrols, text='Program & Data controls')
		Button(self.progdatacontrols, text='New dataset', command=lambda: PopInfo(text=['Are you sure?', 'Cancel','Yes'], com=self.newdata)).grid(sticky=E+W, padx=10)
		Button(self.progdatacontrols, text='Save data', command=lambda: NameInput(['File name', 'Submit'])).grid(sticky=E+W, padx=10)
		Button(self.progdatacontrols, text='Quit', command=root.destroy).grid(sticky=E+W, padx=10)
		
		""" Measurement Labelframe """

		self.measFrame=LabelFrame(self, text='Measurements')
		self.measFrame.grid(column=0, row=2, sticky=N+S+E+W, pady=10)
		# ~ self.measFrame.columnconfigure(0,weight=1)
		
		# measurement notebook
		self.measnb=ttk.Notebook(self.measFrame)
		self.measnb.grid(sticky=E+W, pady=10)
		
		#notebook pg1 simple measurement
		self.simpleMeas=ttk.Frame(self.measnb)
		self.simpleMeas.columnconfigure(0,weight=1)
		self.simpleMeas.columnconfigure(1,weight=1)
		self.measnb.add(self.simpleMeas,text='Single')
		Label(self.simpleMeas, text='Input measurement name: ').grid(column=0,row=0, padx=10, pady=10, sticky=W)
		self.measname=Entry(self.simpleMeas)
		self.measname.grid(column=1,row=0, padx=10, pady=10, sticky=E+W)
		Button(self.simpleMeas, text='Start', command=lambda: self.chk_input(subject=self.measname,command=self.sin_meas)).grid(sticky=E+W, padx=10, pady=10, columnspan=2)
		
		#notebook pg2 periodical measurement
		self.multiMeas=ttk.Frame(self.measnb)
		self.multiMeas.columnconfigure(0,weight=1)
		self.multiMeas.columnconfigure(1,weight=1)
		self.measnb.add(self.multiMeas, text='Periodical')
		Label(self.multiMeas, text='Timegap (min): ').grid(column=0, row=0, sticky=W, padx=10, pady=10)
		self.meastimegap=Entry(self.multiMeas)
		self.meastimegap.grid(column=1,row=0, padx=10, pady=10,sticky=E+W)
		Label(self.multiMeas, text='Enter measurement name prefix: ').grid(column=0,row=1, padx=10, sticky=W)
		self.periodpref=Entry(self.multiMeas)
		self.periodpref.grid(column=1,row=1, padx=10, pady=10, sticky=E+W)
		Label(self.multiMeas, text='Enter time length (min): ').grid(column=0, row=2, padx=10, pady=10, sticky=W)
		self.timelength=Entry(self.multiMeas)
		self.timelength.grid(column=1, row=2, padx=10, pady=10, sticky=E+W)
		Button(self.multiMeas, text='Start!', command=lambda: self.chk_input(subject=[self.meastimegap, self.periodpref, self.timelength],command=self.periodical)).grid(sticky=E+W, padx=10, pady=10, columnspan=2)
		
		#notebook pg3 measure for some time
		self.longMeas=ttk.Frame(self.measnb)
		self.longMeas.columnconfigure(0,weight=1)
		self.longMeas.columnconfigure(1,weight=1)
		self.measnb.add(self.longMeas,text='Long')
		Label(self.longMeas, text='Measurement length (min)').grid(sticky=W, column=0, row=0, padx=10)
		self.measFor=Spinbox(self.longMeas,from_=0, to=20, increment=0.1)
		self.measFor.grid(sticky=E+W, column=1,row=0,padx=10, pady=10)
		Label(self.longMeas, text='Enter measurement name prefix: ').grid(column=0,row=1, padx=10, sticky=W)
		self.measpref=Entry(self.longMeas)
		self.measpref.grid(column=1,row=1, padx=10, pady=10, sticky=E+W)
		Button(self.longMeas, text='Start!', command=lambda: self.chk_input(subject=[self.measpref, self.measFor],command=self.long_meas)).grid(sticky=E+W, padx=10, pady=10, columnspan=2)
		
		"""Plots Labelframe"""
		
		self.plotsFrame=LabelFrame(self,text='Plot')
		self.plotsFrame.grid(column=1, row=1, sticky=N+S+E+W,pady=10)
		self.plotsFrame.columnconfigure(0,weight=1)
		Label(self.plotsFrame, text='Separation: ').grid(sticky=E,padx=10,pady=10,column=0,row=0)
		self.sep=Spinbox(self.plotsFrame, from_=0, to=30, increment=0.5)
		self.sep.grid(column=1,row=0, padx=10, pady=10,sticky=E+W)
		self.left_plot_border=DoubleVar()
		self.right_plot_border=DoubleVar()
		self.right_plot_border.set(1399)
		Label(self.plotsFrame, text='Adjust plot width').grid(column=0, row=1)
		Label(self.plotsFrame, text='Left border:').grid(column=0,row=2)
		Scale(self.plotsFrame, from_=0, to=1399 ,orient=HORIZONTAL,resolution=1, variable=self.left_plot_border).grid(sticky=E+W, columnspan=2, row=3)
		Label(self.plotsFrame, text='Right border:').grid(column=0,row=5)
		Scale(self.plotsFrame, from_=0, to=1399 ,orient=HORIZONTAL,resolution=1, variable=self.right_plot_border).grid(sticky=E+W,columnspan=2, row=6)
		
		Button(self.plotsFrame, text='Show 2D plot', command=lambda: self.show_plot(separator=float(self.sep.get()), leftBorder=int(self.left_plot_border.get()),
		rightBorder=int(self.right_plot_border.get()))).grid(sticky=E+W,columnspan=2, padx=10, pady=10)
		
		Button(self.plotsFrame, text='Show 3D plot', command=lambda: self.make_3dplot(separator=float(self.sep.get()), leftBorder=int(self.left_plot_border.get()),
		rightBorder=int(self.right_plot_border.get()))).grid(sticky=E+W,columnspan=2, padx=10, pady=10)
		
	def newdata(self):
		self.data=pd.DataFrame()
		self.read_time()	
	
	def run(self):
		osc.write(b':RUN')
		
	def sin_meas(self):
		name=self.measname.get()
		self.getit(name)
		self.data[name]=(self.data[name]-float(self.data[name].mode()[0]))*self.datainc
		
	def long_meas(self,timespan=5e-2):
		timelength=float(self.measFor.get())*60
		tex=self.measpref.get()
		for x in range(int(timelength/timespan)):
			start=time.time()
			self.getit(tex+str(x))
			taken=timespan-(time.time()-start)
			time.sleep(taken)
		self.data.iloc[:,1:]=(self.data.iloc[:,1:]-self.data.iloc[:,1:].mode().iloc[0,:])*self.datainc
		
	def getit(self,name):
		osc.write(b':WAV:DATA?')
		self.temp=b''
		for x in range(2):
			self.temp+=osc.read(950)
		self.data[name]=pd.DataFrame(np.frombuffer(self.temp[12:], 'B'))
		
	def periodical(self):
		length=self.timelength.get()
		timegap=self.meastimegap.get()
		prefix=self.periodpref.get()
		if not all([timegap.isnumeric(), length.isnumeric()]):
			PopInfo(text=['Timegap or length is not a number.', 'Understood.'])
		else:
			i=0
			length=float(length)*60
			timegap=float(timegap)*60
			while length>=0:
				self.getit(prefix+str(i))
				time.wait(timegap)
				length-=timegap
	
	def make_3dplot(self, separator, leftBorder, rightBorder):
		fig=plt.figure()
		ax=fig.gca(projection='3d')
		x=self.data.drop(columns='time')
		tim=self.data['time']
		if leftBorder>rightBorder:
			rightBorder,leftBorder=(leftBorder,rightBorder)
		for n in range(len(x.columns)):
			ax.plot(tim[leftBorder:rightBorder+1],x.iloc[leftBorder:rightBorder+1,n], n*separator,zdir='y')
		ax.set_xlabel('drift time (ms)')
		ax.set_zlabel('intensity')
		plt.show()
	
	def show_plot(self,separator, leftBorder, rightBorder):
		if separator:
			factor=np.arange(0, separator*len(self.data.iloc[:,1:].columns), separator)
		else:
			factor=0
		if leftBorder>rightBorder:
			rightBorder,leftBorder=(leftBorder,rightBorder)
		x=self.data['time'][leftBorder:rightBorder+1]
		y=self.data.drop('time', axis=1)+factor
		for col in y.columns:
			plt.plot(x,y.loc[leftBorder:rightBorder+1,col])
		plt.xlabel('drift time (ms)')
		plt.ylabel('intensity')
		plt.show()

	def read_time(self):
		osc.write(b':WAV:XINC?')
		self.xinc=float(osc.read(300))
		osc.write(b':TIM:OFFS?')
		self.xoffs=float(osc.read(300))
		osc.write(b':WAV:POIN?')
		self.point_nr=int(osc.read(300))
		osc.write(b':TIM:SCAL?')
		self.xscal=float(osc.read(300))
		self.data['time']=np.arange(-(7-self.xoffs/self.xscal)*self.xscal,14*self.xscal,self.xinc)[0:self.point_nr]
	
	def stop(self):
		osc.write(b':STOP')

	def clear(self):
		osc.clear_waveform()
		
	def save_data(self, name):
		self.data.to_csv(name+'.csv')
		
	def chk_input(self, subject,command=None):
		if not isinstance(subject, list):
			subject=[subject]
		chklist=[]
		for sub in subject:
			chklist+=[sub.get()]
		if not all(chklist):
			PopInfo(['Fill entry fields.','OK'])
		else:
			if command:
				command()
				
	def set_avgs(self, num):
		osc.write(b':ACQ:TYPE AVER')
		osc.write(bytearray(':ACQ:AVER '+num, encoding='utf-8'))

class RightSide(Frame):
	"""this side will eventually contain some plots"""
	def __init__(self, master=None):
		super().__init__(master)
		self.grid(column=1, row=0)
		self.create_widgets()

class PopInfo(Toplevel):
	def __init__(self, text, com=False, master=None):
		super().__init__(master)
		self.create_widgets(text, com)
	
	def create_widgets(self,text, cmd):
		Label(self, text=text[0]).grid(columnspan=2, row=0)
		if cmd:
			Button(self, text=text[2], command=cmd).grid(column=0,row=1)
		Button(self, text=text[1], command=self.ok).grid(column=1, row=1)
		
	def ok(self):
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

class AvgPop(Toplevel):
	def __init__(self, text, master=None):
		super().__init__(master)
		self.create_widgets(text)
			
	def create_widgets(self,text):
		Label(self, text=text[0]).grid(column=0, row=0)
		x=np.ones(13)*2
		self.spbox=Spinbox(self,values=tuple(str(list((x**np.arange(1,14,1)).astype(int)))[1:-1].split(',')), state='readonly')
		self.spbox.grid(row=1, columnspan=2)
		Button(self, text=text[1], command=self.submit).grid(column=0, row=2)
		Button(self, text='Cancel', command=self.canc).grid(column=1, row=2)
		
	def submit(self):
		self.avgnr=self.spbox.get().strip()
		menu.set_avgs(num=self.avgnr)
		self.destroy()
		
	def canc(self):
		self.destroy()
		
while True:
	try:
		osc=instrument.RigolScope('/dev/usbtmc1')
	except:
		print('No device connected.')
		input('Connect device and press Enter.(Or press Ctrl+C to exit)')
	else:
		break

root=Tk()
root.geometry('1000x800')
root.columnconfigure(0,weight=1)
root.columnconfigure(1,weight=1)
menu=LeftSide(master=root)
root.mainloop()
