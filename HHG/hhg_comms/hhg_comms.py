

########################################################################
#
# Filename: hhg_comms.py								Author: Kristof VL
#
# Descript: Communicate with the HedgeHog module via serial 
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#       
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#       
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.
#       
   


import serial, time, datetime, os







# class responsible for finding connected HedgeHogs
class HHG_find:
	
	def __init__(self):
		# ideally, we could detect the OS here...
		print ''
		
	def list(self):
		res = os.popen('ls /dev/ttyA*', "r").read()	# most Linux distros
		if len(res) > 0:
			sRes = str(res).split('\n')
			return sRes[0:len(sRes)-1] #remove trailing empty \n-split
		else:
			return False



# communicate with a HedgeHog via rs232 serial (over USB)
class HHG_comms:
	
	def __init__(self, port):
		self.PORT = port
		
	def connect(self, time_out=0.2):
		self.ser = serial.Serial(
		self.PORT,			#number of device or a device string
		baudrate=115200,	#baudrate
		bytesize=8,			#number of databits
		parity='N',			#enable parity checking
		stopbits=1,			#number of stopbits
		timeout=time_out,	#set a timeout value, None for waiting forever
		xonxoff=0,        #enable software flow control
		rtscts=0				#enable RTS/CTS flow control
		)
		try:
			self.ser.open()
			self.ser.flushInput()
			self.ser.flushOutput()
		except serial.SerialException as msg:
			# pyserial-2.6.1 already opened the port when constructing the
			# Serial object, and throwns an exception accordingly, ignore
			# this here.
			if str(msg)=="Port is already open.":
				return
			else:
				raise
		except ValueError:
			return False
		
	def disconnect(self):
		self.ser.close()
		
	def getVersion(self, time_out, exp_len):
		self.ser.write("v")
		time.sleep(time_out)
		return self.ser.read(16)
		
	def setFat(self, time_out, exp_len):
		self.ser.write("f")
		time.sleep(time_out)
		return self.ser.read(exp_len)

	def initHHG(self, time_out, exp_len):
		self.ser.write("i")
		time.sleep(time_out)
		return self.ser.read(exp_len)
		
	def setHHGID(self, HHGid, HHGacc, time_out, exp_len):
		self.ser.write("w")
		# HedgeHog id"
		time.sleep(time_out)
		self.ser.write(HHGid[0])
		time.sleep(time_out)
		self.ser.write(HHGid[1])
		time.sleep(time_out)
		self.ser.write(HHGid[2])
		time.sleep(time_out)
		self.ser.write(HHGid[3])
		# HedgeHog make timestamp:
		time.sleep(time_out)
		self.ser.write("_")
		time.sleep(time_out)
		self.ser.write("_")
		time.sleep(time_out)
		self.ser.write("_")
		time.sleep(time_out)
		self.ser.write("_")
		# HedgeHog acc conf:
		self.ser.write("_")
		time.sleep(time_out)
		self.ser.write("_")
		time.sleep(time_out)
		self.ser.write("_")
		time.sleep(time_out)
		self.ser.write("_")
		time.sleep(time_out)
		# HedgeHog acc id:
		self.ser.write(HHGacc[0])
		time.sleep(time_out)
		self.ser.write(HHGacc[1])
		time.sleep(time_out)
		self.ser.write(HHGacc[2])
		time.sleep(time_out)
		self.ser.write(HHGacc[3])
		time.sleep(time_out)
		# HedgeHog env id:
		self.ser.write("_")
		time.sleep(time_out)
		self.ser.write("_")
		time.sleep(time_out)
		self.ser.write("_")
		time.sleep(time_out)
		self.ser.write("_")
		time.sleep(time_out)
		ret = self.ser.read(exp_len)
		return ret
		
	def getHHGID(self, time_out, exp_len):
		self.ser.write("u")
		time.sleep(time_out)
		ret = self.ser.read(exp_len)
		return ret
		
	def synchronizeClock(self, time_out, exp_len):
		mydate = datetime.datetime.now()
		self.ser.write("t"); 
		time.sleep(time_out)
		self.ser.write(chr(mydate.year-2000))
		time.sleep(time_out)
		self.ser.write(chr(mydate.month))
		time.sleep(time_out)
		self.ser.write(chr(mydate.day))
		time.sleep(time_out)
		self.ser.write(chr(mydate.hour)) 
		time.sleep(time_out)
		self.ser.write(chr(mydate.minute))
		time.sleep(time_out)
		self.ser.write(chr(mydate.second)) 
		ret = self.ser.read(exp_len)
		return ret
		
	def readData(self, time_out, exp_len):
		self.ser.write("r")
		time.sleep(time_out)
		ret = self.ser.read(exp_len)
		return ret
		
	def record_HHG(self):
		self.ser.write("s")
		self.ser.close()
		
