

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
import glob



# class responsible for finding connected HedgeHogs
class HHG_find:
	
	def __init__(self):
		# ideally, we could detect the OS here...
		print ''
		
	def list(self):
		res = sorted(glob.glob('/dev/ttyA*'))	# most Linux distros
		return res


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
		xonxoff=0,          #enable software flow control
		rtscts=0			#enable RTS/CTS flow control
		)
		
	def disconnect(self):
		self.ser.close()
		
	def get_version(self, time_out, exp_len):
		self.ser.write("v")
		time.sleep(time_out)
		return self.ser.read(16)
		
	def set_FAT(self, time_out, exp_len):
		self.ser.write("f")
		time.sleep(time_out)
		return self.ser.read(exp_len)

	def init_HHG(self, time_out, exp_len):
		self.ser.write("i")
		time.sleep(time_out)
		return self.ser.read(exp_len)
		
	def set_HHGID(self, conf_str, time_out, exp_len):
		self.ser.write("w")
		for i in range(0,20):
			time.sleep(time_out)
			self.ser.write(conf_str[i])
		time.sleep(time_out)
		ret = self.ser.read(exp_len)
		return ret
		
	def get_HHGID(self, time_out, exp_len):
		self.ser.write("u")
		time.sleep(time_out)
		ret = self.ser.read(exp_len)
		return ret
		
	def synchronize_clock(self, time_out, exp_len):
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
		
	def set_timeout_clock(self, tdate, time_out, exp_len):
		self.ser.write("T");
		time.sleep(time_out)
		self.ser.write(chr(tdate.year-2000))
		time.sleep(time_out)
		self.ser.write(chr(tdate.month))
		time.sleep(time_out)
		self.ser.write(chr(tdate.day))
		time.sleep(time_out)
		self.ser.write(chr(tdate.hour)) 
		time.sleep(time_out)
		self.ser.write(chr(tdate.minute))
		time.sleep(time_out)
		self.ser.write(chr(tdate.second)) 
		ret = self.ser.read(exp_len)
		return ret
		
	def read_data(self, time_out, exp_len):
		self.ser.write("r")
		time.sleep(time_out)
		ret = self.ser.read(exp_len)
		return ret

	def read_log(self, time_out, exp_len):
		self.ser.write("c")
		time.sleep(time_out)
		ret = self.ser.read(exp_len)
		return ret
		
	def record_HHG(self):
		self.ser.write("s")
		self.ser.close()
		
