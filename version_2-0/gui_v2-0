import scopeclass, os, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import MailResults
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from mpl_toolkits.mplot3d import Axes3D
from tkinter import ttk

class MainFrame(Frame):
	
	def __init__(self, parent):
		super().__init__(parent)
		# ~ self.scope=scopeclass.RigolScope(dev='/dev/scope/scope')
		self.data=pd.DataFrame()
		# ~ self.data['time']=self.scope.timeAxis
		self.parent=parent
		
		self.createWidgets()
		
	def createWidgets(self):
		ScopeControls(parent=self).grid(column=0,row=0, sticky=N+E+W+S)
		DataControls(parent=self).grid(column=0,row=1,sticky=N+E+W+S)
		MeasurementLabel(parent=self).grid(column=1,row=0,rowspan=2,sticky=N+E+W+S)
		PlotsLabel(parent=self).grid(column=2, row=0, rowspan=2, sticky=N+E+W+S)
		
	def exitProgram(self):
		# ~ self.scope.finish()
		self.parent.destroy()


class ScopeControls(LabelFrame):
	
	def __init__(self, parent):
		super().__init__(parent, text='Scope Controls')
		self.columnconfigure(0, weight=1)
		self.parent=parent
		
		self.createWidgets()
		
	def createWidgets(self):
		# ~ Button(self, text='Run', command=self.parent.scope.run).grid(sticky=E+W)
		Button(self, text='Run', command=None).grid(sticky=E+W)
		# ~ Button(self, text='Stop', command=self.parent.scope.stop).grid(sticky=E+W)
		Button(self, text='Stop', command=None).grid(sticky=E+W)
		# ~ Button(self, text='Clear', command=self.parent.scope.clearWaveform).grid(sticky=E+W)
		Button(self, text='Clear', command=None).grid(sticky=E+W)
		Button(self, text='Quit', command=self.parent.exitProgram).grid(sticky=E+W)
		
		
class DataControls(LabelFrame):
	
	def __init__(self, parent):
		super().__init__(parent, text='Data Controls')
		self.columnconfigure(0, weight=1)
		self.parent=parent
		
		self.createWidgets()
		
	def createWidgets(self):
		Button(self, text='Clear Data', command= self.newData).grid(sticky=E+W)
		Button(self, text='Save Data to .csv', command=self.saveData).grid(sticky=E+W)
		Button(self, text='Save Data to .csv and send via email', command=self.mailto).grid(sticky=E+W)
		
	def newData(self):
		if messagebox.askyesno(title='Are you sure?', message='Are you sure?', default='no'):
			self.parent.data=pd.DataFrame()
		
	def saveData(self):
		name=filedialog.asksaveasfilename(parent=self.parent.parent, filetypes=[('comma separated values','*.csv')], title='save as')
		if name:
			self.parent.data.to_csv(name)
			
	def mailto(self):
		MailPop(parent=self)
	
		
class MeasurementLabel(LabelFrame):
	
	def __init__(self, parent):
		super().__init__(parent, text='Measurements')
		self.columnconfigure(0, weight=1)
		self.parent=parent
		self.createWidgets()
		
	def createWidgets(self):
		# measurement notebook
		self.measnb=ttk.Notebook(self)
		self.measnb.grid(sticky=N+E+W+S, pady=10)
		
		#notebook pg1 simple measurement
		self.simpleMeas=ttk.Frame(self.measnb)
		self.simpleMeas.columnconfigure(0,weight=1)
		self.simpleMeas.columnconfigure(1,weight=1)
		self.measnb.add(self.simpleMeas,text='Single')
		Label(self.simpleMeas, text='Input measurement name: ').grid(column=0,row=0, padx=10, pady=10, sticky=W)
		self.measname=Entry(self.simpleMeas)
		self.measname.grid(column=1,row=0, padx=10, pady=10, sticky=E+W)
		Button(self.simpleMeas, text='Start', command=self.singleMeasure).grid(sticky=E+W, padx=10, pady=10, columnspan=2)
		
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
		Button(self.multiMeas, text='Start!', command=self.periodicalMeasure).grid(sticky=E+W, padx=10, pady=10, columnspan=2)
		
		#notebook pg3 measure for some time
		self.longMeas=ttk.Frame(self.measnb)
		self.longMeas.columnconfigure(0,weight=1)
		self.longMeas.columnconfigure(1,weight=1)
		self.measnb.add(self.longMeas,text='Chromatograph')
		Label(self.longMeas, text='Measurement length (min)').grid(sticky=W, column=0, row=0, padx=10)
		self.measFor=Spinbox(self.longMeas,from_=0, to=20, increment=0.1)
		self.measFor.grid(sticky=E+W, column=1,row=0,padx=10, pady=10)
		Button(self.longMeas, text='Start!', command=None).grid(sticky=E+W, padx=10, pady=10, columnspan=2)		
	
	def singleMeasure(self):
		name=self.measname.get()
		if name:
			self.parent.data[name]=self.parent.scope.readBinData()
		else:
			messagebox.showerror(title='No name', message='Failed to comply. Enter proper name.')
		
	def periodicalMeasure(self):
		name=self.periodpref.get()
		timegap=self.meastimegap.get()
		timelength=self.timelength.get()
		if all([name, timegap.isnumeric(), timelength.isnumeric()]):
			temp, _ =self.parent.scope.longMeasure(length=length, timegap=timegap)
			columns=[name+'{:03d}'.format(i) for i in range(temp.shape[0])]
			self.parent.data=pd.concat([self.parent.data, pd.DataFrame(temp.T, columns=columns)], axis=1)
		else:
			messagebox.showerror(title='No name', message='Failed to comply. Enter proper name.')
			
	def longMeasure(self):
		timegap=50*10**-3
		length=self.longMeas.get()
		if length.isnumeric():
			temp, columns=self.parent.scope.longMeasure(length=length, timegap=timegap)
			self.parent.data=pd.concat([self.parent.data, pd.DataFrame(temp.T,columns=columns)], axis=1)
		# ~ #in case there was some problem with indexes
			# ~ self.parent.data=pd.concat([self.parent.data.reset_index(drop=True),pd.DataFrame(temp.T,columns=columns).reset_index(drop=True)], axis=1)
		else:
			messagebox.showerror(title='Not a number', message='Failed to comply. Timelength is not a number.')


class PlotsLabel(LabelFrame):
	
	def __init__(self, parent):
		super().__init__(parent, text='Plots')
		self.columnconfigure(0,weight=1)
		
		self.createWidgets()
	
	def createWidgets(self):	
		Label(self, text='Separation: ').grid(sticky=E,padx=10,pady=10,column=0,row=0)
		self.sep=Spinbox(self, from_=0, to=30, increment=0.5)
		self.sep.grid(column=1,row=0, padx=10, pady=10,sticky=E+W)
		self.left_plot_border=DoubleVar()
		self.right_plot_border=DoubleVar()
		self.right_plot_border.set(1399)
		Label(self, text='Adjust plot width').grid(column=0, row=1)
		Label(self, text='Left border:').grid(column=0,row=2)
		Scale(self, from_=0, to=1399 ,orient=HORIZONTAL,resolution=1, variable=self.left_plot_border).grid(sticky=E+W, columnspan=2, row=3)
		Label(self, text='Right border:').grid(column=0,row=5)
		Scale(self, from_=0, to=1399 ,orient=HORIZONTAL,resolution=1, variable=self.right_plot_border).grid(sticky=E+W,columnspan=2, row=6)
		Button(self, text='Show 2D plot', command=self.show2DPlot).grid(sticky=E+W,columnspan=2, padx=10, pady=10)
		Button(self, text='Show 3D plot', command=self.show3DPlot).grid(sticky=E+W,columnspan=2, padx=10, pady=10)
		
	def show2DPlot(self):
		fig=plt.figure()
		ax=fig.gca()
		separator=float(self.sep.get())
		if separator:
			factor=np.arange(0, separator*len(self.parent.data.iloc[:,1:].columns), separator)
		else:
			factor=0
		leftBorder, rigthBorder=(int(self.left_plot_border.get()),int(self.right_plot_border.get()))
		if leftBorder>rightBorder:
			rightBorder,leftBorder=(leftBorder,rightBorder)
		x=self.data['time'][leftBorder:rightBorder+1]
		y=self.data.drop(columns='time')+factor
		for col in y.columns:
			ax.plot(x,y.loc[leftBorder:rightBorder+1,col])
		ax.set_xlabel('drift time (ms)')
		ax.set_ylabel('intensity')
		plt.show()
		
	def show3DPlot(self):
		fig=plt.figure()
		ax=fig.gca(projection='3d')
		x=self.parent.data.drop(columns='time')
		tim=self.parent.data['time']
		separator=float(self.sep.get())
		leftBorder, rigthBorder=(int(self.left_plot_border.get()),int(self.right_plot_border.get()))
		if leftBorder>rightBorder:
			rightBorder,leftBorder=(leftBorder,rightBorder)
		for n in range(len(x.columns)):
			ax.plot(tim[leftBorder:rightBorder+1],x.iloc[leftBorder:rightBorder+1,n], n*separator,zdir='y')
		ax.set_xlabel('drift time (ms)')
		ax.set_zlabel('intensity')
		plt.show()		


class MailPop(Toplevel):
	
	def __init__(self,parent):
		super().__init__(parent)
		self.parent=parent
		
		self.createWidgets()
		
	def createWidgets(self):
		self.opt=StringVar()
		Label(self,text='Choose receiver:').grid()
		OptionMenu(self,self.opt, *list(MailResults.receivers_dict.keys())).grid()
		Button(self, text='Send!', command=self.submit).grid()
		
	def submit(self):
		name=filedialog.asksaveasfilename(parent=self.parent.parent, filetypes=[('comma separated values','*.csv')], title='save as')
		if name:
			self.parent.parent.data.to_csv(name)
			MailResults.send_via_email(receiver=MailResults.receivers_dict[self.opt.get()], path=name)
		self.destroy()

def main():
	root=Tk()
	MainFrame(root).grid()
	root.mainloop()
	
	
if __name__== '__main__':
	main()
