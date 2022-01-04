# -*- coding: utf-8 -*-
#
#  PlatoonHDWeather Converter
#
#  Coded/Modified/Adapted by örlgrey
#  Based on teamBlue image source code
#
#  This code is licensed under the Creative Commons 
#  Attribution-NonCommercial-ShareAlike 3.0 Unported 
#  License. To view a copy of this license, visit
#  http://creativecommons.org/licenses/by-nc-sa/3.0/ 
#  or send a letter to Creative Commons, 559 Nathan 
#  Abbott Way, Stanford, California 94305, USA.
#
#  If you think this license infringes any rights,
#  please contact me at ochzoetna@gmail.com

from __future__ import print_function

from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.config import config
from enigma import eTimer
import requests, time
from Components.Converter.Poll import Poll
from Plugins.Extensions.PlatoonHD import ping
from lxml import etree
from xml.etree.cElementTree import fromstring

WEATHER_DATA = None
WEATHER_LOAD = True

class PlatoonHDWeather(Poll, Converter, object):
	def __init__(self, type):
		Poll.__init__(self)
		Converter.__init__(self, type)
		self.poll_interval = 60000
		self.poll_enabled = True
		self.type = type
		self.timer = eTimer()
		self.timer.callback.append(self.reset)
		self.timer.callback.append(self.get_Data)
		self.data = None
		self.get_Data()

	@cached
	def getText(self):
		global WEATHER_DATA
		self.data = WEATHER_DATA
		if self.type == "temp_cur":
			return self.getTemperature_current()
		elif self.type == "feels_like":
			return self.getTemperature_feelslike()
		elif self.type == "humidity":
			return self.getHumidity()
		elif self.type == "wind":
			return self.getWind()
		elif self.type == "city":
			return str(config.plugins.PlatoonHD.msn_cityfound.value)
		elif self.type in ("icon_cur", "icon1", "icon2", "icon3"):
			return self.getMeteoIcon()
		elif self.type in ("text_cur", "text1", "text2", "text3"):
			return self.getMeteoText()
		elif self.type in ("high0", "high1", "high2", "high3"):
			return self.getTemperature_high()
		elif self.type in ("low0", "low1", "low2", "low3"):
			return self.getTemperature_low()
		elif self.type in ("minmax0", "minmax1", "minmax2", "minmax3"):
			return self.getMinMax()
		elif self.type in ("shortday0", "shortday1", "shortday2", "shortday3"):
			return self.getShortday()
		else:
			return ""

	text = property(getText)

	def reset(self):
		global WEATHER_LOAD
		WEATHER_LOAD = True
		self.timer.stop()

	def get_Data(self):
		global WEATHER_DATA
		global WEATHER_LOAD
		if WEATHER_LOAD == True:
			try:
				r = ping.doOne("8.8.8.8", 1.5)
				if r != None and r <= 1.5:
					print ("PlatoonHDWeather: download from URL")
					res = requests.get('http://weather.service.msn.com/data.aspx?src=windows&weadegreetype=C&culture=' + str(config.plugins.PlatoonHD.msn_language.value) + '&wealocations=' + str(config.plugins.PlatoonHD.msn_code.value), timeout=1.5)
					self.data = fromstring(res.text)
					WEATHER_DATA = self.data
					WEATHER_LOAD = False
			except:
				pass
			timeout = max(15,int(config.plugins.PlatoonHD.refreshInterval.value)) * 1000.0 * 60.0
			self.timer.start(int(timeout), True)
		else:
			self.data = WEATHER_DATA

	def getTemperature_current(self):
		try:
			for childs in self.data:
				for items in childs:
					if items.tag == 'current':
						value = items.attrib.get("temperature")
						return str(value) + "°C"
		except:
			return ''

	def getTemperature_feelslike(self):
		try:
			for childs in self.data:
				for items in childs:
					if items.tag == 'current':
						cur_temp = items.attrib.get("temperature")
						feels_temp = items.attrib.get("feelslike")
						return str(cur_temp) + '°C' + ", gefühlt " + str(feels_temp) + '°C'
		except:
			return ''

	def getHumidity(self):
		try:
			for childs in self.data:
				for items in childs:
					if items.tag == 'current':
						value = items.attrib.get("humidity")
						return str(value) + '% Luftfeuchte'
		except:
			return ''

	def getWind(self):
		try:
			for childs in self.data:
				for items in childs:
					if items.tag == 'current':
						value = items.attrib.get("winddisplay")
						return str(value)
		except:
			return ''

	def getTemperature_high(self):
		try:
			if self.type == "high0":
				for items in self.data.findall(".//forecast[2]"):
					value = items.get("high")
					return str(value) + "°C"
			if self.type == "high1":
				for items in self.data.findall(".//forecast[3]"):
					value = items.get("high")
					return str(value) + "°C"
			if self.type == "high2":
				for items in self.data.findall(".//forecast[4]"):
					value = items.get("high")
					return str(value) + "°C"
			if self.type == "high3":
				for items in self.data.findall(".//forecast[5]"):
					value = items.get("high")
					return str(value) + "°C"
		except:
			return ''

	def getTemperature_low(self):
		try:
			if self.type == "low0":
				for items in self.data.findall(".//forecast[2]"):
					value = items.get("low")
					return str(value) + "°C"
			if self.type == "low1":
				for items in self.data.findall(".//forecast[3]"):
					value = items.get("low")
					return str(value) + "°C"
			if self.type == "low2":
				for items in self.data.findall(".//forecast[4]"):
					value = items.get("low")
					return str(value) + "°C"
			if self.type == "low3":
				for items in self.data.findall(".//forecast[5]"):
					value = items.get("low")
					return str(value) + "°C"
		except:
			return ''

	def getMinMax(self):
		try:
			if self.type == "minmax0":
				for items in self.data.findall(".//forecast[2]"):
					min = items.get("low")
					max = items.get("high")
					return str(min) + "° / " + str(max) + "°"
			if self.type == "minmax1":
				for items in self.data.findall(".//forecast[3]"):
					min = items.get("low")
					max = items.get("high")
					return str(min) + "° / " + str(max) + "°"
			if self.type == "minmax2":
				for items in self.data.findall(".//forecast[4]"):
					min = items.get("low")
					max = items.get("high")
					return str(min) + "° / " + str(max) + "°"
			if self.type == "minmax3":
				for items in self.data.findall(".//forecast[5]"):
					min = items.get("low")
					max = items.get("high")
					return str(min) + "° / " + str(max) + "°"
		except:
			return ''

	def getShortday(self):
		try:
			if self.type == "shortday0":
				for items in self.data.findall(".//forecast[2]"):
					value = items.get("shortday")
					return str(value)
			if self.type == "shortday1":
				for items in self.data.findall(".//forecast[3]"):
					value = items.get("shortday")
					return str(value)
			if self.type == "shortday2":
				for items in self.data.findall(".//forecast[4]"):
					value = items.get("shortday")
					return str(value)
			if self.type == "shortday3":
				for items in self.data.findall(".//forecast[5]"):
					value = items.get("shortday")
					return str(value)
		except:
			return ''

	def getMeteoIcon(self):
		try:
			if self.type == "icon_cur":
				for childs in self.data:
					for items in childs:
						if items.tag == "current":
							value = items.attrib.get("skycode")
							return str(value)
			if self.type == "icon1":
				for items in self.data.findall(".//forecast[3]"):
					value = items.get("skycodeday")
					return str(value)
			if self.type == "icon2":
				for items in self.data.findall(".//forecast[4]"):
					value = items.get("skycodeday")
					return str(value)
			if self.type == "icon3":
				for items in self.data.findall(".//forecast[5]"):
					value = items.get("skycodeday")
					return str(value)
		except:
			return "3200"

	def getMeteoText(self):
		try:
			if self.type == "text_cur":
				for childs in self.data:
					for items in childs:
						if items.tag == "current":
							value = items.attrib.get("skytext")
							return str(value)
			if self.type == "text1":
				for items in self.data.findall(".//forecast[3]"):
					value = items.get("skytextday")
					return str(value)
			if self.type == "text2":
				for items in self.data.findall(".//forecast[4]"):
					value = items.get("skytextday")
					return str(value)
			if self.type == "text3":
				for items in self.data.findall(".//forecast[5]"):
					value = items.get("skytextday")
					return str(value)
		except:
			return ''
