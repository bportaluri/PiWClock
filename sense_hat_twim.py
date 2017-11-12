import os
import sys
import time
import http.client
import json

from sense_hat import SenseHat

class SenseHatTwim(SenseHat):
	DIGITS34 = [0,1,0, 1,0,1, 1,0,1, 0,1,0,	 # 0
				1,1,0, 0,1,0, 0,1,0, 1,1,1,	 # 1
				1,1,1, 0,0,1, 0,1,0, 1,1,1,	 # 2
				1,1,1, 0,1,1, 0,1,1, 1,1,1,	 # 3
				1,0,0, 1,0,1, 1,1,1, 0,0,1,	 # 4
				1,1,1, 1,1,0, 0,0,1, 1,1,1,	 # 5
				1,1,1, 1,0,0, 1,1,1, 1,1,1,	 # 6
				1,1,1, 0,0,1, 0,1,0, 1,0,0,	 # 7
				1,1,1, 1,1,1, 1,0,1, 1,1,1,	 # 8
				1,1,1, 1,1,1, 0,0,1, 0,1,0,	 # 9
				0,1,0, 0,1,0, 0,1,0, 0,1,0]	 # 1 (small)

	DIGITS35 = [1,1,1, 1,0,1, 1,0,1, 1,0,1, 1,1,1,	# 0
				0,1,0, 0,1,0, 0,1,0, 0,1,0, 0,1,0,	# 1
				1,1,1, 0,0,1, 0,1,0, 1,0,0, 1,1,1,	# 2
				1,1,1, 0,0,1, 1,1,1, 0,0,1, 1,1,1,	# 3
				1,0,0, 1,0,1, 1,1,1, 0,0,1, 0,0,1,	# 4
				1,1,1, 1,0,0, 1,1,1, 0,0,1, 1,1,1,	# 5
				1,1,1, 1,0,0, 1,1,1, 1,0,1, 1,1,1,	# 6
				1,1,1, 0,0,1, 0,1,0, 1,0,0, 1,0,0,	# 7
				1,1,1, 1,0,1, 1,1,1, 1,0,1, 1,1,1,	# 8
				1,1,1, 1,0,1, 1,1,1, 0,0,1, 0,0,1]	# 9

	X = [200, 0, 0]	 # Red
	O = [0, 0, 0]  # Black
	G = [80, 80, 80]  # Gray
	Y = [120, 120, 0]  # Yellow
	T = [180, 180, 0]  # Thunder
	
	ICONS = {
	'SUN':	  [ Y,O,O,Y,O,O,O,Y,
				O,Y,O,O,O,O,Y,O,
				O,O,O,Y,Y,O,O,O,
				O,O,Y,Y,Y,Y,O,Y,
				Y,O,Y,Y,Y,Y,O,O,
				O,O,O,Y,Y,O,O,O,
				O,Y,O,O,O,O,Y,O,
				Y,O,O,O,Y,O,O,Y ],
	'CLOUD':  [ O,G,G,G,O,O,O,O,
				G,O,O,O,G,G,G,O,
				G,O,O,O,G,O,O,G,
				G,O,O,O,O,O,O,G,
				G,O,O,O,O,O,O,G,
				O,G,G,G,G,G,G,O,
				O,O,O,O,O,O,O,O,
				O,O,O,O,O,O,O,O, ],
	'SHOWERS':[ O,G,G,G,O,O,O,O,
				G,O,O,O,G,G,G,O,
				G,O,O,O,G,O,O,G,
				G,O,O,O,O,O,O,G,
				G,O,O,O,O,O,O,G,
				O,G,G,G,G,G,G,O,
				O,G,O,G,O,G,O,O,
				G,O,G,O,G,O,O,O, ],
	'RAIN':	  [ G,O,G,O,G,O,G,O,
				O,G,O,G,O,G,O,G,
				G,O,G,O,G,O,G,O,
				O,G,O,G,O,G,O,G,
				G,O,G,O,G,O,G,O,
				O,G,O,G,O,G,O,G,
				G,O,G,O,G,O,G,O,
				O,G,O,G,O,G,O,G ],
	'STORM':  [ O,G,G,G,O,O,O,O,
				G,O,O,O,G,G,G,O,
				G,O,O,O,G,O,O,G,
				G,O,O,O,O,Y,O,G,
				G,O,O,O,Y,O,O,G,
				O,G,G,Y,Y,Y,G,O,
				O,O,O,O,Y,O,O,O,
				O,O,O,Y,O,O,O,O ],
	'SNOW':	  [ G,O,G,O,O,G,O,G,
				O,G,O,O,O,O,G,O,
				G,O,G,O,O,G,O,G,
				O,O,O,G,G,O,O,O,
				O,O,O,G,G,O,O,O,
				G,O,G,O,O,G,O,G,
				O,G,O,O,O,O,G,O,
				G,O,G,O,O,G,O,G, ]
	}

	
	def __init__(self, *args, **kwargs):
		super(SenseHatTwim, self).__init__(*args, **kwargs)
		t = self.get_temperature_from_humidity()
		self.smooth_temp = [t, t, t]
		self.forecast_t = 0
		self.forecast_args = [0, 0, 0]
		self.forecast_weather = ""


	# read sensors data to detect orientation
	def get_orientation(self):
		x = round(self.get_accelerometer_raw()['x'], 0)
		y = round(self.get_accelerometer_raw()['y'], 0)

		if x == -1:
			return 1
		elif y == -1:
			return 2
		elif x == 1:
			return 3
		return 0

	# display one digit (0-9) with 3x4 fonts
	def show_digit34(self, val, x, y, col):
		offset = val * 12
		for p in range(offset, offset + 12):
			xt = p % 3
			yt = (p-offset) // 3
			self.set_pixel(xt+x, yt+y, [col[0]*self.DIGITS34[p], col[1]*self.DIGITS34[p], col[2]*self.DIGITS34[p]])
	
	# display one digit (0-9) with 3x5 fonts
	def show_digit35(self, val, x, y, col):
		offset = val * 15
		for p in range(offset, offset + 15):
			xt = p % 3
			yt = (p-offset) // 3
			self.set_pixel(xt+x, yt+y, [col[0]*self.DIGITS35[p], col[1]*self.DIGITS35[p], col[2]*self.DIGITS35[p]])

	# display two-digits numbers (0-99) with 3x4 fonts
	def show_digits34(self, val, x, y, col):
		tens = val // 10
		units = val % 10
		if (val > 9):
			self.show_digit34(tens, x, y, col)
		self.show_digit34(units, x+4, y, col)

	# display two-digits numbers (0-99) with 3x4 fonts
	def show_digits35(self, val, x, y, col):
		tens = val // 10
		units = val % 10
		if (val > 9):
			self.show_digit35(tens, x, y, col)
		self.show_digit35(units, x+4, y, col)

	# display a centered number in range 0-12
	def show_tiny_hour(self, val, y, col):
		if (val>=0 and val<10):
			self.show_digit34(val, 3, y, col)
		if (val==10):
			self.show_digit34(10, 1, y, col)
			self.show_digit34(0, 4, y, col)
		if (val==11):
			self.show_digit34(10, 2, y, col)
			self.show_digit34(10, 4, y, col)
		if (val==12):
			self.show_digit34(10, 1, y, col)
			self.show_digit34(2, 4, y, col)
		
	
	# draws a bar on the border to simulate minutes of a clock
	# val must be between 0 and 28
	def draw_circ_bar(self, val, col, col_bkg):
		if(val<0): val=0
		if(val>28): val=28
		x = round(val)
		
		for i in range(1, 29):
			c = col
			if (i>x): c=col_bkg
			if i<4:
				self.set_pixel(3+i, 0, c)
			if i>=4 and i<11:
				self.set_pixel(7, i-4, c)
			if i>=11 and i<18:
				self.set_pixel(-i+18, 7, c)
			if i>=18 and i<25:
				self.set_pixel(0, -i+25, c)
			if i>=25:
				self.set_pixel(i-25, 0, c)

	def show_icon(self, icon_name):
		self.set_pixels(self.ICONS[icon_name])
	
	# rotate the display according to the orientation
	def auto_rotate_display(self):
		self.set_rotation(self.get_orientation()*90)
	
	def scale_rgb_color(self, col, x):
		return [int(col[0]*x/100), int(col[1]*x/100), int(col[2]*x/100)]

	def get_cpu_temp(self):
		res = os.popen("vcgencmd measure_temp").readline()
		t = float(res.replace("temp=","").replace("'C\n",""))
		return(t)

	def get_corrected_temperature(self):
		"""Gets the temperature from Sense HAT sensors and compensates it from CPU heating."""
		t1 = self.get_temperature_from_humidity()
		t2 = self.get_temperature_from_pressure()
		t_cpu = self.get_cpu_temp()
		p = self.get_pressure()

		# calculates the real temperature compensating CPU heating
		t = (t1+t2)/2
		t_corr = t - ((t_cpu-t)/1.5)
		
		self.smooth_temp[2] = self.smooth_temp[1]
		self.smooth_temp[1] = self.smooth_temp[0]
		self.smooth_temp[0] = t_corr
		xs = (self.smooth_temp[0]+self.smooth_temp[1]+self.smooth_temp[2])/3
		
		return xs


	def show_openweather_forecast(self, apikey, lat, lon, day):
		"""
		Make request to openweathermap.org and display weather forecast icon.
		API documentation here: http://openweathermap.org/forecast16
		Parameters
		apikey: a valid openweathermap API key (register for a free key)
		lat, lon: latitude and longitude
		day: day to retrieve the forecsat, must be 0-4, 0 is today, 1 is tomorrow, etc.
		"""
		
		# skip API call if already called in the last 2 minutes

		#print("elapsed: ", int(time.time() - self.forecast_t))
		if int(time.time() - self.forecast_t)>120:

			self.forecast_args = [0, 0, 0]
			
			request = "/data/2.5/forecast/daily?" + \
					  "lat={0}&".format(lat) + \
					  "lon={0}&".format(lon) + \
					  "mode=json&" + \
					  "units=metric&" + \
					  "cnt=5&" + \
					  "APPID={0}".format(apikey)

			try:
				print("Getting weather http://api.openweathermap.org", request)
				conn = http.client.HTTPConnection("api.openweathermap.org")
				conn.request("GET", request)
				resp = conn.getresponse()
				data = resp.read()
				#print("Weather data: ", data.decode('utf-8'))
				print("Getting forecast for day: ", day)
				j = json.loads(data.decode('utf-8'))
				weather = j["list"][day]["weather"][0]["main"]
				print("Weather: ", weather)
			except:
				print("Unexpected error:", sys.exc_info()[0])
				self.show_letter("X", [80,0,0])
				return
			else:
				if(weather=="Clear"):
					self.forecast_weather = "SUN"
				elif(weather=="Clouds"):
					self.forecast_weather = "CLOUD"
				elif(weather=="Drizzle"):
					self.forecast_weather = "SHOWERS"
				elif(weather=="Rain"):
					self.forecast_weather = "RAIN"
				elif(weather=="Snow"):
					self.forecast_weather = "SNOW"
				else:
					self.forecast_weather = ""
				
				self.forecast_t = time.time()
			
		if self.forecast_weather == "":
			self.show_letter("?", [80,0,0])
		else:
			self.show_icon(self.forecast_weather)
