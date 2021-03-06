import os, time
import numpy as np


class usbtmc():
	"""Simple implementation of a USBTMC device driver"""
 

	def __init__(self, device):
		self.device = device
		self.FILE = os.open(device, os.O_RDWR)
 
	def write(self, command):
		os.write(self.FILE, command)
 
	def read(self, length = 950):
		return os.read(self.FILE, length)
		
	def close(self):
		self.FILE.close()


class RigolScope():
	"""This is Rigol Oscilloscope DS2000 series kind of API
	It implements function chosen for my project. For more info
	refer to Rigol DS2000 Programming Guide"""
	

	def __init__(self,dev):
		self.scope = usbtmc(dev)
		self.setDefaults()
		self.readTime()
		
	def setDefaults(self):
		self.sendCommand(b':WAV:SOUR CHAN1')
		self.sendCommand(b':WAV:MODE NORM')
		self.sendCommand(b':WAV:FORM BYTE') #may be changed to ASCII
		self.sendCommand(b':ACQ:TYPE AVER')
	
	def readTime(self):
		self.sendCommand(b':WAV:XINC?') #get time increment of horizontal axis
		xinc = float(self.read())
		self.sendCommand(b':TIM:OFFS?') #get the zero position of horizontal axis
		xoffs = float(self.read())
		self.sendCommand(b':WAV:POIN?') #get number of pointson horizontal axis
		point_nr = int(self.read())
		self.sendCommand(b':TIM:SCAL?') #get the horizontal scale of small square on the screen (there are 14 of them)
		xscal = float(self.read())
		#below: create numpy array of time points and crop it if there are too much points
		self.timeAxis = np.arange( - (7 - xoffs / xscal) * xscal, 14 * xscal, xinc)[0:point_nr]
		
	def readDataDefaults(self):
		"""These are needed to convert waveform data to voltage"""
		self.sendCommand(b':WAV:YREF?')
		YRef = float(self.read())
		self.sendCommand(b':CHAN1:SCAL?')
		YScale = float(self.read())
		self.sendCommand(b':CHAN1:OFFS?')
		YOffset = float(self.read())
		return YRef, YScale, YOffset
	
	def sendCommand(self, command):
		self.scope.write(command=command)
		
	def read(self):
		out = self.scope.read()
		return out
	
	def run(self):
		self.sendCommand(b':RUN')
		self.read()
		
	def clearWaveform(self):
		self.sendCommand(b':CLE')
		self.read()
		
	def stop(self):
		self.sendCommand(b':STOP')
		self.read()
		
	def readBinData(self):
		"""this simply reads data and returns it as numpy array"""
		self.sendCommand(b':WAV:DATA?')
		#it seems that regular read(x) function returns finite number of points no matter that the x is very high
		#so the data must be read in two packages:
		tempOutput = b''
		for _ in range(2):
			tempOutput += self.read()
		outputData = np.frombuffer(tempOutput[11:],'B') #first 11 bytes are some kind of header or preamble
		return outputData
		
	def readAscii(self):
		self.sendCommand(b':WAV:FORM ASC')
		self.sendCommand(b':WAV:DATA?')
		return self.read()
		
	def longMeasure(self, length, timegap):
		output = np.ndarray(self.timeAxis.shape)
		for _ in np.arange(0, length*60, timegap):
			start = time.time()
			output = np.vstack((output, self.readBinData())) #now every row will be subsequent read data
			to_wait = timegap-(time.time() - start)
			time.sleep(to_wait)
		result = self.cvtData2Voltage(output[:,1])
		columns = np.arange(0,length*60,timegap).astype('str')
		columns = list(np.core.defchararray.add(columns, np.array('s')))
		return result, columns
		
	def cvtData2Voltage(self, data):
		"""data must be numpy array or pandas dataframe
		the conversion formula was taken from scope programming guide, page 572
        http://int.rigol.com/Support/Manual/5 """
		YRef,YScale,YOffset = self.readDataDefaults()
		result = (data-YRef) * YScale - YOffset
		return result
		
	def setAvgs(self, num):
		self.sendCommand(bytearray(':ACQ:AVER ' + num, encoding='utf-8'))
		
	def finish(self):
		self.scope.close()