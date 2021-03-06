# -*- coding: utf-8 -*-
#
#  PlatoonHD Plugin for teamBlue-image
#
#  Coded/Modified/Adapted by örlgrey
#  Based on teamBlue image source code
#  Thankfully inspired by MyMetrix by iMaxxx
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

from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Screens.Standby import TryQuitMainloop
from Components.ActionMap import ActionMap
from Components.AVSwitch import AVSwitch
from Components.config import config, configfile, ConfigYesNo, ConfigSubsection, getConfigListEntry, ConfigSelection, ConfigNumber, ConfigText, ConfigInteger, ConfigClock, ConfigSlider, ConfigBoolean
from Components.ConfigList import ConfigListScreen
from Components.Sources.StaticText import StaticText
from Components.Pixmap import Pixmap
from Components.Label import Label
from Components.Sources.CanvasSource import CanvasSource
from PIL import Image, ImageEnhance
from Components.Language import language
import gettext, time, os, requests
from enigma import ePicLoad, eTimer
from Tools.Directories import fileExists, resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from shutil import move, copyfile
from lxml import etree
from xml.etree.cElementTree import fromstring

lang = language.getLanguage()
os.environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("PlatoonHD", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/PlatoonHD/locale/"))

def _(txt):
	t = gettext.dgettext("PlatoonHD", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t

def translateBlock(block):
	for x in TranslationHelper:
		if block.__contains__(x[0]):
			block = block.replace(x[0], x[1])
	return block

config.plugins.PlatoonHD = ConfigSubsection()
config.plugins.PlatoonHD.WindowColor = ConfigSelection(default="00002F", choices = [
				("000000", _("black")),
				("1F1F1F", _("dark grey")),
				("2F0000", _("dark red")),
				("00002F", _("dark blue")),
				("001F00", _("dark green"))
				])

config.plugins.PlatoonHD.WindowTrans = ConfigSelection(default="17", choices = [
				("00", _("off")),
				("17", _("low")),
				("2E", _("medium")),
				("45", _("high"))
				])

config.plugins.PlatoonHD.WindowFont1 = ConfigSelection(default="FFFFFF", choices = [
				("FFFFFF", _("white")),
				("BFBFBF", _("grey")),
				("FFC000", _("yellow")),
				("FF7F00", _("orange")),
				("3FBF3F", _("green")),
				("007FFF", _("blue"))
				])

config.plugins.PlatoonHD.WindowFont2 = ConfigSelection(default="FFC000", choices = [
				("FFFFFF", _("white")),
				("BFBFBF", _("grey")),
				("FFC000", _("yellow")),
				("FF7F00", _("orange")),
				("3FBF3F", _("green")),
				("007FFF", _("blue"))
				])

config.plugins.PlatoonHD.MenuColor = ConfigSelection(default="3A3A3A", choices = [
				("3A3A3A", _("grey")),
				("86350D", _("orange")),
				("710B11", _("red")),
				("35294D", _("violet")),
				("024F02", _("green")),
				("17397D", _("blue")),
				("035468", _("petrol"))
				])

config.plugins.PlatoonHD.MenuTrans = ConfigSelection(default="11", choices = [
				("11", _("low")),
				("3F", _("high"))
				])

config.plugins.PlatoonHD.MenuFont1 = ConfigSelection(default="FFFFFF", choices = [
				("FFFFFF", _("white")),
				("BFBFBF", _("grey")),
				("FFC000", _("yellow")),
				("FF7F00", _("orange")),
				("3FBF3F", _("green")),
				("007FFF", _("blue"))
				])

config.plugins.PlatoonHD.MenuFont2 = ConfigSelection(default="FFC000", choices = [
				("FFFFFF", _("white")),
				("BFBFBF", _("grey")),
				("FFC000", _("yellow")),
				("FF7F00", _("orange")),
				("3FBF3F", _("green")),
				("007FFF", _("blue"))
				])

config.plugins.PlatoonHD.SelectionColor1 = ConfigSelection(default="86350D", choices = [
				("3A3A3A", _("grey")),
				("86350D", _("orange")),
				("930B0B", _("red")),
				("482868", _("violet")),
				("002868", _("blue")),
				("0B630B", _("green")),
				("02404A", _("petrol"))
				])

config.plugins.PlatoonHD.SelectionColor2 = ConfigText(default = "")

config.plugins.PlatoonHD.SelectionFont = ConfigSelection(default="FFFFFF", choices = [
				("FFFFFF", _("white")),
				("BFBFBF", _("grey")),
				("FFC000", _("yellow")),
				("FF7F00", _("orange")),
				("3FBF3F", _("green")),
				("007FFF", _("blue"))
				])

config.plugins.PlatoonHD.ButtonFont = ConfigSelection(default="FFFFFF", choices = [
				("FFFFFF", _("white")),
				("BFBFBF", _("grey")),
				("FFC000", _("yellow")),
				("FF7F00", _("orange")),
				("3FBF3F", _("green")),
				("007FFF", _("blue"))
				])

config.plugins.PlatoonHD.Progress = ConfigSelection(default="FF4B05", choices = [
				("FFFFFF", _("white")),
				("FFC242", _("yellow")),
				("FF4B05", _("orange")),
				("742020", _("red")),
				("207420", _("green")),
				("202074", _("blue"))
				])

config.plugins.PlatoonHD.WeatherWidget = ConfigSelection(default = "weather-off", choices = [
				("weather-off", _("off")),
				("infobar", _("Infobar")),
				("menu", _("Menu")),
				("infobar-menu", _("Infobar & Menu"))
				])

config.plugins.PlatoonHD.msn_searchby = ConfigSelection(default = "auto-ip", choices = [
				("auto-ip", _("IP")),
				("location", _("Enter location manually"))
				])

config.plugins.PlatoonHD.refreshInterval = ConfigSelection(default = "0", choices = [
				("0", _("0")),
				("120", _("120"))
				])

SearchResultList = []
config.plugins.PlatoonHD.list = ConfigSelection(default = "", choices = SearchResultList)

config.plugins.PlatoonHD.msn_cityfound = ConfigText(default = "")
config.plugins.PlatoonHD.msn_cityname = ConfigText(default = "")
config.plugins.PlatoonHD.msn_code = ConfigText(default = "")

config.plugins.PlatoonHD.msn_language = ConfigSelection(default="de-DE", choices = [
				("de-DE", _("Deutsch")),
				("en-US", _("English")),
				("ru-RU", _("Russian")),
				("it-IT", _("Italian")),
				("es-ES", _("Spanish")),
				("uk-UA", _("Ukrainian")),
				("pt-PT", _("Portuguese")),
				("ro-RO", _("Romanian")),
				("pl-PL", _("Polish")),
				("fi-FI", _("Finnish")),
				("nl-NL", _("Dutch")),
				("fr-FR", _("French")),
				("bg-BG", _("Bulgarian")),
				("sv-SE", _("Swedish")),
				("tr-TR", _("Turkish")),
				("hr-HR", _("Croatian")),
				("ca-AD", _("Catalan")),
				("sk-SK", _("Slovak"))
				])

class PlatoonHD(ConfigListScreen, Screen):
	skin = """
			<screen name="PlatoonHD" position="0,0" size="1280,720" flags="wfNoBorder" backgroundColor="transparent">
				<widget backgroundColor="PlatoonGYbg" source="Title" render="Label" font="Regular2;30" foregroundColor="PlatoonGYfg2" position="42,20" size="736,38" valign="center" transparent="1" />
				<widget backgroundColor="PlatoonGYbg" source="version" render="Label" font="Regular;24" foregroundColor="PlatoonGYfg1" position="414,24" size="800,30" halign="right" transparent="1" />
				<widget backgroundColor="PlatoonBKbg" name="config" font="Regular;22" foregroundColor="PlatoonBKfg1" itemHeight="30" selectionPixmap="/usr/share/enigma2/PlatoonHD/graphics/sel_30.png" position="42,80" size="736,450" enableWrapAround="1" scrollbarMode="showOnDemand" transparent="1" zPosition="1" />
				<widget backgroundColor="PlatoonBKbg" name="helperimage" position="846,70" size="368,207" zPosition="1" />
				<widget backgroundColor="PlatoonBKbg" source="Canvas" render="Canvas" position="846,70" size="368,207" zPosition="-1" />
				<eLabel backgroundColor="PlatoonGYfg2" position="846,68" size="368,2" zPosition="2" />
				<eLabel backgroundColor="PlatoonGYfg2" position="846,277" size="368,2" zPosition="2" />
				<eLabel backgroundColor="PlatoonGYfg2" position="844,68" size="2,211" zPosition="2" />
				<eLabel backgroundColor="PlatoonGYfg2" position="1212,68" size="2,211" zPosition="2" />
				<widget backgroundColor="PlatoonBKbg" source="description" render="Label" font="Regular2;22" foregroundColor="PlatoonBKfg2" position="42,539" size="736,81" halign="center" valign="center" transparent="1" />
				<ePixmap backgroundColor="PlatoonBKbg" pixmap="/usr/share/enigma2/PlatoonHD/logo.png" position="902,330" size="256,256" alphatest="blend" />
				<widget font="Regular;20" halign="left" valign="center" source="key_red" position="40,655" size="220,26" render="Label" backgroundColor="PlatoonGYbg" foregroundColor="PlatoonButtonfg" transparent="1" />
				<widget font="Regular;20" halign="left" valign="center" source="key_green" position="290,655" size="220,26" render="Label" backgroundColor="PlatoonGYbg" foregroundColor="PlatoonButtonfg" transparent="1" />
				<widget font="Regular;20" halign="left" valign="center" source="key_yellow" position="540,655" size="220,26" render="Label" backgroundColor="PlatoonGYbg" foregroundColor="PlatoonButtonfg" transparent="1" />
				<ePixmap alphatest="blend" pixmap="/usr/share/enigma2/PlatoonHD/buttons/key_red1.png" position="35,682" size="200,5" />
				<ePixmap alphatest="blend" pixmap="/usr/share/enigma2/PlatoonHD/buttons/key_green1.png" position="285,682" size="200,5" />
				<ePixmap alphatest="blend" pixmap="/usr/share/enigma2/PlatoonHD/buttons/key_yellow1.png" position="535,682" size="200,5" />
				<ePixmap alphatest="blend" pixmap="/usr/share/enigma2/PlatoonHD/buttons/key_blue1.png" position="785,682" size="200,5" />
				<ePixmap pixmap="/usr/share/enigma2/PlatoonHD/global-icons/key_ok.png" position="1145,660" size="43,22" alphatest="blend" />
				<ePixmap pixmap="/usr/share/enigma2/PlatoonHD/global-icons/key_exit.png" position="1195,660" size="43,22" alphatest="blend" />
				<ePixmap pixmap="/usr/share/enigma2/PlatoonHD/graphics/menu_background.png" position="0,0" size="1280,720" zPosition="-9" alphatest="blend" />
				<eLabel backgroundColor="PlatoonBKbg" position="32,70" size="756,560" zPosition="-9" />
			</screen>
			"""

	def __init__(self, session, args = None, picPath = None):
		self.skin_lines = []
		Screen.__init__(self, session)
		self.session = session
		copyfile("/usr/share/enigma2/PlatoonHD/act-skin.xml", "/usr/lib/enigma2/python/Plugins/Extensions/PlatoonHD/skin.xml")
		self.xmlfile = "/usr/lib/enigma2/python/Plugins/Extensions/PlatoonHD/skin.xml"
		self.skinfile = "/usr/share/enigma2/PlatoonHD/skin.xml"
		self.templates = "/usr/share/enigma2/PlatoonHD/templates/"
		self.graphics = "/usr/share/enigma2/PlatoonHD/graphics/"
		self.skinfile_tmp = self.skinfile + ".tmp"
		self.picPath = "/usr/lib/enigma2/python/Plugins/Extensions/PlatoonHD/images/"
		self.Scale = AVSwitch().getFramebufferScale()
		self.PicLoad = ePicLoad()
		self["helperimage"] = Pixmap()
		self["Canvas"] = CanvasSource()
		self["description"] = StaticText()
		self["version"] = StaticText("Version 1.4.1")

		list = []
		ConfigListScreen.__init__(self, list)

		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions", "ColorActions", "InputActions"],
		{
			"up": self.keyUp,
			"down": self.keyDown,
			"left": self.keyLeft,
			"right": self.keyRight,
			"red": self.exit,
			"green": self.save,
			"yellow": self.checkCode,
			"cancel": self.exit,
			"ok": self.OK,
		}, -2)

		self["key_red"] = StaticText(_("Exit"))
		self["key_green"] = StaticText(_("Save"))
		self["key_yellow"] = StaticText()
		self["Title"] = StaticText(_("MyPlatoonHD-Settings"))

		self.UpdatePicture()

		self.timer = eTimer()
		self.timer.callback.append(self.updateMylist)
		self.onLayoutFinish.append(self.updateMylist)

		self.E2DistroVersion = self.getE2DistroVersion()
		self.InternetAvailable = self.getInternetAvailable()

	def mylist(self):
		self.timer.start(100, True)

	def updateMylist(self):
		list = []
		list.append(getConfigListEntry(_("background"), config.plugins.PlatoonHD.MenuColor, _("Choose the background color.")))
		list.append(getConfigListEntry(_("    transparency"), config.plugins.PlatoonHD.MenuTrans, _("Choose the degree of background transparency.")))
		list.append(getConfigListEntry(_("    primary font color"), config.plugins.PlatoonHD.MenuFont1, _("Choose the color of the primary font.")))
		list.append(getConfigListEntry(_("    secondary font color"), config.plugins.PlatoonHD.MenuFont2, _("Choose the color of the secondary font.")))
		list.append(getConfigListEntry(_("window"), config.plugins.PlatoonHD.WindowColor, _("Choose the background color.")))
		list.append(getConfigListEntry(_("    transparency"), config.plugins.PlatoonHD.WindowTrans, _("Choose the degree of background transparency.")))
		list.append(getConfigListEntry(_("    primary font color"), config.plugins.PlatoonHD.WindowFont1, _("Choose the color of the primary font.")))
		list.append(getConfigListEntry(_("    secondary font color"), config.plugins.PlatoonHD.WindowFont2, _("Choose the color of the secondary font.")))
		list.append(getConfigListEntry(_("    selection color"), config.plugins.PlatoonHD.SelectionColor1, _("Choose the background color of selection bars.")))
		list.append(getConfigListEntry(_("    selection font color"), config.plugins.PlatoonHD.SelectionFont, _("Choose the color of the font in selection bars.")))
		list.append(getConfigListEntry(_("    progress bar color"), config.plugins.PlatoonHD.Progress, _("Choose the color of progress bars.")))
		list.append(getConfigListEntry(_("weather"), config.plugins.PlatoonHD.WeatherWidget, _("Choose from different options to display the weather informations, or deactivate the weather infos.")))
		if config.plugins.PlatoonHD.WeatherWidget.value in ("infobar", "menu", "infobar-menu"):
			list.append(getConfigListEntry(_("    Language"), config.plugins.PlatoonHD.msn_language, _("Specify the language for the weather output.")))
			list.append(getConfigListEntry(_("    Search option"), config.plugins.PlatoonHD.msn_searchby, _("Choose from different options to enter your settings.\nThen press the yellow button to search for the weather code.")))
			if config.plugins.PlatoonHD.msn_searchby.value == "location":
				list.append(getConfigListEntry(_("    Location"), config.plugins.PlatoonHD.msn_cityname, _("Enter your location. Press OK to use the virtual keyboard.\nThen press the yellow button to search for the weather code.")))

		self["config"].list = list
		self["config"].l.setList(list)
		self.updateHelp()
		self.showYellowText()
		self["helperimage"].hide()
		self.ShowPicture()

		# preview
		self.showPreview()

	def showPreview(self):
		option = self["config"].getCurrent()[1]

		if option == config.plugins.PlatoonHD.SelectionColor1:
			if option.value == "930B0B":
				self.showGradient(config.plugins.PlatoonHD.SelectionColor1.value, "2D1010")
			elif option.value == "0B630B":
				self.showGradient(config.plugins.PlatoonHD.SelectionColor1.value, "102010")
			elif option.value == "002868":
				self.showGradient(config.plugins.PlatoonHD.SelectionColor1.value, "001535")
			elif option.value == "482868":
				self.showGradient(config.plugins.PlatoonHD.SelectionColor1.value, "1F0F2F")
			elif option.value == "02404A":
				self.showGradient(config.plugins.PlatoonHD.SelectionColor1.value, "012A3A")
			elif option.value == "86350D":
				self.showGradient(config.plugins.PlatoonHD.SelectionColor1.value, "661F02")
			elif option.value == "3A3A3A":
				self.showGradient(config.plugins.PlatoonHD.SelectionColor1.value, "202020")
		elif option in (config.plugins.PlatoonHD.WindowColor, config.plugins.PlatoonHD.WindowFont1, config.plugins.PlatoonHD.WindowFont2, config.plugins.PlatoonHD.MenuColor, config.plugins.PlatoonHD.MenuFont1, config.plugins.PlatoonHD.MenuFont2, config.plugins.PlatoonHD.SelectionFont, config.plugins.PlatoonHD.Progress):
			self.showColor(self.hexRGB(option.value))
		elif option == config.plugins.PlatoonHD.WindowTrans:
			if option.value == "00":
				self.showText(30,_("no transparency"))
			elif option.value == "17":
				self.showText(30,_("low transparency"))
			elif option.value == "2E":
				self.showText(30,_("medium transparency"))
			elif option.value == "45":
				self.showText(30,_("high transparency"))
		elif option == config.plugins.PlatoonHD.MenuTrans:
			if option.value == "11":
				self.showText(30,_("low transparency"))
			elif option.value == "3F":
				self.showText(30,_("high transparency"))
		elif option == config.plugins.PlatoonHD.WeatherWidget:
			if option.value == "weather-off":
				self.showText(30,_("Weather off"))
			elif option.value == "infobar":
				self.showText(30,_("Infobar"))
			elif option.value == "menu":
				self.showText(30,_("Menu"))
			elif option.value == "infobar-menu":
				self.showText(30,_("Infobar & Menu"))
		elif option in (config.plugins.PlatoonHD.msn_searchby, config.plugins.PlatoonHD.msn_code, config.plugins.PlatoonHD.msn_cityname):
			self.showText(30, config.plugins.PlatoonHD.msn_cityfound.value + "\n" + config.plugins.PlatoonHD.msn_code.value)
		elif option == config.plugins.PlatoonHD.msn_language:
			self.showText(30,_("Language") + ":\n" + option.value)
		else:
			self["helperimage"].show()

	def updateHelp(self):
		cur = self["config"].getCurrent()
		if cur:
			self["description"].text = cur[2]

	def showYellowText(self):
		option = self["config"].getCurrent()[1]
		if option.value == "auto-ip" or option.value == "location" or option == config.plugins.PlatoonHD.msn_cityname:
			self["key_yellow"].text = _("Search Code")
		else:
			self["key_yellow"].text = ""

	def GetPicturePath(self):
		try:
			optionValue = self["config"].getCurrent()[1]
			returnValue = self["config"].getCurrent()[1].value
			if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/PlatoonHD/images/" + returnValue + ".jpg"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/PlatoonHD/images/" + returnValue + ".jpg"
			if fileExists(path):
				return path
		except:
			return "/usr/lib/enigma2/python/Plugins/Extensions/PlatoonHD/images/black.jpg"

	def UpdatePicture(self):
		self.PicLoad.PictureData.get().append(self.DecodePicture)
		self.onLayoutFinish.append(self.ShowPicture)

	def ShowPicture(self):
		self.PicLoad.setPara([self["helperimage"].instance.size().width(), self["helperimage"].instance.size().height(), self.Scale[0], self.Scale[1], 0, 1, "#00000000"])
		if self.picPath is not None:
			self.picPath = None
			self.PicLoad.startDecode(self.picPath)
		else:
			self.PicLoad.startDecode(self.GetPicturePath())

	def DecodePicture(self, PicInfo = ""):
		ptr = self.PicLoad.getData()
		self["helperimage"].instance.setPixmap(ptr)

	def keyLeft(self):
		ConfigListScreen.keyLeft(self)
		self.mylist()

	def keyRight(self):
		ConfigListScreen.keyRight(self)
		self.mylist()

	def keyDown(self):
		self["config"].instance.moveSelection(self["config"].instance.moveDown)
		self.mylist()

	def keyUp(self):
		self["config"].instance.moveSelection(self["config"].instance.moveUp)
		self.mylist()

	def getCityByIP(self):
		try:
			res_city = requests.get('http://ip-api.com/json/?lang=de&fields=status,city', timeout=1)
			data_city = res_city.json()
			if data_city['status'] == 'success':
				return str(data_city['city'])
		except:
			self.session.open(MessageBox, _("No valid location found."), MessageBox.TYPE_INFO, timeout = 10)

	def checkCode(self):
		if self.InternetAvailable and config.plugins.PlatoonHD.WeatherWidget.value in ("infobar", "menu", "infobar-menu"):
			option = self["config"].getCurrent()[1]
			if option.value == "auto-ip":
				cityip = self.getCityByIP()
				iplist = []
				try:
					res_gc = requests.get('http://weather.service.msn.com/find.aspx?src=windows&outputview=search&weasearchstr=' + str(cityip) + '&culture=' + str(config.plugins.PlatoonHD.msn_language.value), timeout=1)
					data_gc = fromstring(res_gc.text)

					for weather in data_gc.findall("./weather"):
						ipcity = weather.get('weatherlocationname').encode("utf-8", 'ignore')
						weathercode = weather.get('weatherlocationcode')
						iplist.append((ipcity, weathercode + "//" + ipcity))

					def WeatherCodeCallBack(callback):
						callback = callback and callback[1]
						if callback:
							config.plugins.PlatoonHD.msn_code.value = str(callback.split("//")[0])
							config.plugins.PlatoonHD.msn_code.save()
							config.plugins.PlatoonHD.msn_cityfound.value = str(callback.split("//")[1].split(",")[0])
							config.plugins.PlatoonHD.msn_cityfound.save()
							self.session.open(MessageBox, _("Weather-Code found:\n") + str(config.plugins.PlatoonHD.msn_code.value), MessageBox.TYPE_INFO, timeout = 10)
						self.showPreview()
					self.session.openWithCallback(WeatherCodeCallBack, ChoiceBox, title = _("Choose your location:"), list = iplist)

				except:
					self.session.open(MessageBox, _("No valid location found."), MessageBox.TYPE_INFO, timeout = 10)

			if option.value == "location" or option == config.plugins.PlatoonHD.msn_cityname:
				citylist = []
				try:
					res_gc = requests.get('http://weather.service.msn.com/find.aspx?src=windows&outputview=search&weasearchstr=' + str(config.plugins.PlatoonHD.msn_cityname.value) + '&culture=' + str(config.plugins.PlatoonHD.msn_language.value), timeout=1)
					data_gc = fromstring(res_gc.text)

					for weather in data_gc.findall("./weather"):
						city = weather.get('weatherlocationname').encode("utf-8", 'ignore')
						code = weather.get('weatherlocationcode')
						citylist.append((city, code + "//" + city))

					def LocationCallBack(callback):
						callback = callback and callback[1]
						if callback:
							config.plugins.PlatoonHD.msn_code.value = str(callback.split("//")[0])
							config.plugins.PlatoonHD.msn_code.save()
							config.plugins.PlatoonHD.msn_cityfound.value = str(callback.split("//")[1].split(",")[0])
							config.plugins.PlatoonHD.msn_cityfound.save()
							self.session.open(MessageBox, _("Weather-Code found:\n") + str(config.plugins.PlatoonHD.msn_code.value), MessageBox.TYPE_INFO, timeout = 10)
						self.showPreview()
					self.session.openWithCallback(LocationCallBack, ChoiceBox, title = _("Choose your location:"), list = citylist)

				except:
					self.session.open(MessageBox, _("No valid Weather-Code found."), MessageBox.TYPE_INFO, timeout = 10)

	def VirtualKeyBoardCallBack(self, callback):
		try:
			if callback:
				self["config"].getCurrent()[1].value = callback
			else:
				pass
		except:
			pass

	def OK(self):
		option = self["config"].getCurrent()[1]

		if option == config.plugins.PlatoonHD.msn_cityname:
			text = self["config"].getCurrent()[1].value
			title = _("Enter your location:")
			self.session.openWithCallback(self.VirtualKeyBoardCallBack, VirtualKeyBoard, title = title, text = text)
			config.plugins.PlatoonHD.msn_cityname.save()

	def reboot(self):
		restartbox = self.session.openWithCallback(self.restartGUI,MessageBox, _("Do you really want to reboot now?"), MessageBox.TYPE_YESNO)
		restartbox.setTitle(_("Restart GUI"))

	def save(self):
		for x in self["config"].list:
			if len(x) > 1:
				x[1].save()
			else:
				pass

		self.skinSearchAndReplace = []

		# backgrounds + transparency
		self.skinSearchAndReplace.append(['name="PlatoonBKbg" value="#1700002F', 'name="PlatoonBKbg" value="#' + config.plugins.PlatoonHD.WindowTrans.value + config.plugins.PlatoonHD.WindowColor.value])
		self.skinSearchAndReplace.append(['name="background" value="#1700002F', 'name="background" value="#' + config.plugins.PlatoonHD.WindowTrans.value + config.plugins.PlatoonHD.WindowColor.value])
		self.skinSearchAndReplace.append(['name="PlatoonGYbg" value="#113A3A3A', 'name="PlatoonGYbg" value="#' + config.plugins.PlatoonHD.MenuTrans.value + config.plugins.PlatoonHD.MenuColor.value])

		# fonts
		self.skinSearchAndReplace.append(['name="PlatoonBKfg1" value="#00FFFFFF', 'name="PlatoonBKfg1" value="#00' + config.plugins.PlatoonHD.WindowFont1.value])
		self.skinSearchAndReplace.append(['name="foreground" value="#00FFFFFF', 'name="foreground" value="#00' + config.plugins.PlatoonHD.WindowFont1.value])
		self.skinSearchAndReplace.append(['name="PlatoonBKfg2" value="#00FFC000', 'name="PlatoonBKfg2" value="#00' + config.plugins.PlatoonHD.WindowFont2.value])
		self.skinSearchAndReplace.append(['name="PlatoonGYfg1" value="#00FFFFFF', 'name="PlatoonGYfg1" value="#00' + config.plugins.PlatoonHD.MenuFont1.value])
		self.skinSearchAndReplace.append(['name="PlatoonButtonfg" value="#00FFFFFF', 'name="PlatoonButtonfg" value="#00' + config.plugins.PlatoonHD.MenuFont1.value])
		self.skinSearchAndReplace.append(['name="PlatoonGYfg2" value="#00FFC000', 'name="PlatoonGYfg2" value="#00' + config.plugins.PlatoonHD.MenuFont2.value])
		self.skinSearchAndReplace.append(['name="PlatoonSelfg" value="#00FFFFFF', 'name="PlatoonSelfg" value="#00' + config.plugins.PlatoonHD.SelectionFont.value])

		# progress
		self.skinSearchAndReplace.append(['name="PlatoonProgress" value="#00FF4B05', 'name="PlatoonProgress" value="#00' + config.plugins.PlatoonHD.Progress.value])
		
		# selection background
		self.skinSearchAndReplace.append(['name="PlatoonSelbg" value="#0086350D', 'name="PlatoonSelbg" value="#00' + config.plugins.PlatoonHD.SelectionColor1.value])
		if config.plugins.PlatoonHD.SelectionColor1.value == "930B0B":
			config.plugins.PlatoonHD.SelectionColor2.value = "2D1010"
			config.plugins.PlatoonHD.SelectionColor2.save()
		elif config.plugins.PlatoonHD.SelectionColor1.value == "0B630B":
			config.plugins.PlatoonHD.SelectionColor2.value = "102010"
			config.plugins.PlatoonHD.SelectionColor2.save()
		elif config.plugins.PlatoonHD.SelectionColor1.value == "482868":
			config.plugins.PlatoonHD.SelectionColor2.value = "1F0F2F"
			config.plugins.PlatoonHD.SelectionColor2.save()
		elif config.plugins.PlatoonHD.SelectionColor1.value == "02404A":
			config.plugins.PlatoonHD.SelectionColor2.value = "012A3A"
			config.plugins.PlatoonHD.SelectionColor2.save()
		elif config.plugins.PlatoonHD.SelectionColor1.value == "86350D":
			config.plugins.PlatoonHD.SelectionColor2.value = "661F02"
			config.plugins.PlatoonHD.SelectionColor2.save()
		elif config.plugins.PlatoonHD.SelectionColor1.value == "3A3A3A":
			config.plugins.PlatoonHD.SelectionColor2.value = "202020"
			config.plugins.PlatoonHD.SelectionColor2.save()
		else:
			config.plugins.PlatoonHD.SelectionColor2.value = "001535"
			config.plugins.PlatoonHD.SelectionColor2.save()

		# graphics
		if config.plugins.PlatoonHD.MenuTrans.value == "3F":
			self.changeMenuColors()
		else:
			self.copyMenuFiles()
		self.makeSelectionpng()

		# weather
		if config.plugins.PlatoonHD.WeatherWidget.value in ("infobar", "menu", "infobar-menu"):
			if self.InternetAvailable:
				if config.plugins.PlatoonHD.WeatherWidget.value == "infobar":
					self.skinSearchAndReplace.append(['<!-- infobar weather -->', '<panel name="infobar-weather"/>'])
					self.skinSearchAndReplace.append(['name="TimeshiftState" position="217,80"', 'name="TimeshiftState" position="217,126"'])
					self.skinSearchAndReplace.append(['name="TunerState" position="10,196"', 'name="TunerState" position="10,242"'])
					self.skinSearchAndReplace.append(['name="TunerState_v2" position="10,196"', 'name="TunerState_v2" position="10,242"'])
					self.skinSearchAndReplace.append(['name="ResolutionLabel" position="10,102"', 'name="ResolutionLabel" position="10,148"'])
				elif config.plugins.PlatoonHD.WeatherWidget.value == "infobar-menu":
					self.skinSearchAndReplace.append(['<!-- infobar weather -->', '<panel name="infobar-weather"/>'])
					self.skinSearchAndReplace.append(['name="TimeshiftState" position="217,80"', 'name="TimeshiftState" position="217,126"'])
					self.skinSearchAndReplace.append(['name="TunerState" position="10,196"', 'name="TunerState" position="10,242"'])
					self.skinSearchAndReplace.append(['name="TunerState_v2" position="10,196"', 'name="TunerState_v2" position="10,242"'])
					self.skinSearchAndReplace.append(['name="ResolutionLabel" position="10,102"', 'name="ResolutionLabel" position="10,148"'])
					self.skinSearchAndReplace.append(['<panel name="menu_clock"/>', '<panel name="menu_weather"/>'])
				elif config.plugins.PlatoonHD.WeatherWidget.value == "menu":
					self.skinSearchAndReplace.append(['<panel name="menu_clock"/>', '<panel name="menu_weather"/>'])
				config.plugins.PlatoonHD.refreshInterval.value = "120"
				config.plugins.PlatoonHD.refreshInterval.save()
				self.appendSkinFile(self.xmlfile)
				self.generateSkin()
			else:
				config.plugins.PlatoonHD.refreshInterval.value = "0"
				config.plugins.PlatoonHD.refreshInterval.save()
				self.session.open(MessageBox, _("Your box needs an internet connection to display the weather information.\nPlease solve the problem."), MessageBox.TYPE_INFO, timeout = 10)
				config.plugins.PlatoonHD.WeatherWidget.value = "weather-off"
				self.mylist()
		else:
			config.plugins.PlatoonHD.refreshInterval.value = "0"
			config.plugins.PlatoonHD.refreshInterval.save()
			self.appendSkinFile(self.xmlfile)
			self.generateSkin()

	def generateSkin(self):
		xFile = open(self.skinfile_tmp, "w")
		for xx in self.skin_lines:
			xFile.writelines(xx)
		xFile.close()
		move(self.skinfile_tmp, self.skinfile)
		self.restart()

	def restart(self):
		configfile.save()
		restartbox = self.session.openWithCallback(self.restartGUI,MessageBox, _("GUI needs a restart to apply the settings.\nDo you want to Restart the GUI now?"), MessageBox.TYPE_YESNO)
		restartbox.setTitle(_("Restart GUI"))

	def appendSkinFile(self, appendFileName):
		"""
		add skin file to main skin content

		appendFileName:
		 xml skin-part to add
		"""

		skFile = open(appendFileName, "r")
		file_lines = skFile.readlines()
		skFile.close()

		tmpSearchAndReplace = []
		tmpSearchAndReplace = self.skinSearchAndReplace

		for skinLine in file_lines:
			for item in tmpSearchAndReplace:
				skinLine = skinLine.replace(item[0], item[1])
			self.skin_lines.append(skinLine)

	def restartGUI(self, answer):
		if answer is True:
			configfile.save()
			self.session.open(TryQuitMainloop, 3)
		else:
			self.close()

	def exit(self):
		askExit = self.session.openWithCallback(self.doExit,MessageBox, _("Do you really want to exit without saving?"), MessageBox.TYPE_YESNO)
		askExit.setTitle(_("Exit"))

	def doExit(self, answer):
		if answer is True:
			for x in self["config"].list:
				if len(x) > 1:
						x[1].cancel()
				else:
						pass
			self.close()
		else:
			self.mylist()

	def getE2DistroVersion(self):
		try:
			from boxbranding import getImageDistro
			if getImageDistro() == "teamblue":
				return "teamblue"
			elif getImageDistro() == "openhdf":
				return "openhdf"
		except ImportError:
			return "teamblue"

	def getInternetAvailable(self):
		import ping
		r = ping.doOne("8.8.8.8", 1.5)
		if r != None and r <= 1.5:
			return True
		else:
			return False

	def showColor(self, actcolor):
		c = self["Canvas"]
		c.fill(0, 0, 368, 207, actcolor)
		c.flush()

	def showGradient(self, color1, color2):
		width = 368
		height = 207
		color1 = color1[-6:]
		r1 = int(color1[0:2], 16)
		g1 = int(color1[2:4], 16)
		b1 = int(color1[4:6], 16)
		color2 = color2[-6:]
		r2 = int(color2[0:2], 16)
		g2 = int(color2[2:4], 16)
		b2 = int(color2[4:6], 16)
		c = self["Canvas"]
		if color1 != color2:
			for pos in range(0, height):
				p = pos / float(height)
				r = r2 * p + r1 * (1 - p)
				g = g2 * p + g1 * (1 - p)
				b = b2 * p + b1 * (1 - p)
				c.fill(0, pos, width, 1, self.RGB(int(r), int(g), int(b)))
		else:
			c.fill(0, 0, width, height, self.RGB(int(r1), int(g1), int(b1)))
		c.flush()

	def showText(self, fontsize, text):
		from enigma import gFont, RT_HALIGN_CENTER, RT_VALIGN_CENTER
		c = self["Canvas"]
		c.fill(0, 0, 368, 207, self.RGB(0, 0, 0))
		c.writeText(0, 0, 368, 207, self.RGB(255, 255, 255), self.RGB(0, 0, 0), gFont("Regular", fontsize), text, RT_HALIGN_CENTER + RT_VALIGN_CENTER)
		c.flush()

	def changeMenuColors(self):
		self.changeColor("bs_b", config.plugins.PlatoonHD.MenuColor.value)
		self.changeColor("bs_bl", config.plugins.PlatoonHD.MenuColor.value)
		self.changeColor("bs_br", config.plugins.PlatoonHD.MenuColor.value)
		self.changeColor("bs_l", config.plugins.PlatoonHD.MenuColor.value)
		self.changeColor("bs_r", config.plugins.PlatoonHD.MenuColor.value)
		self.changeColor("bs_t", config.plugins.PlatoonHD.MenuColor.value)
		self.changeColor("bs_tl", config.plugins.PlatoonHD.MenuColor.value)
		self.changeColor("bs_tr", config.plugins.PlatoonHD.MenuColor.value)
		self.changeColor("dvd_background", config.plugins.PlatoonHD.MenuColor.value)
		self.changeColor("full_background", config.plugins.PlatoonHD.MenuColor.value)
		self.changeColor("infobar_background", config.plugins.PlatoonHD.MenuColor.value)
		self.changeColor("mediaplayer_background", config.plugins.PlatoonHD.MenuColor.value)
		self.changeColor("menu_background", config.plugins.PlatoonHD.MenuColor.value)
		self.changeColor("player_background", config.plugins.PlatoonHD.MenuColor.value)
		self.changeColor("pvrstate_background", config.plugins.PlatoonHD.MenuColor.value)
		self.changeColor("shift_background", config.plugins.PlatoonHD.MenuColor.value)
		self.changeColor("sib_background", config.plugins.PlatoonHD.MenuColor.value)
		self.changeColor("virtualkeyboard_background", config.plugins.PlatoonHD.MenuColor.value)
		self.changeColor("volume_background", config.plugins.PlatoonHD.MenuColor.value)
		self.changeColor("webradio_background", config.plugins.PlatoonHD.MenuColor.value)
		if self.E2DistroVersion == "openhdf":
			self.changeColor("infobarepg_background", config.plugins.PlatoonHD.MenuColor.value)
			self.changeColor("infobareventview_background", config.plugins.PlatoonHD.MenuColor.value)
			self.changeColor("virtualkeyboard_background2", config.plugins.PlatoonHD.MenuColor.value)

	def copyMenuFiles(self):
		copyfile(self.templates + config.plugins.PlatoonHD.MenuColor.value + "/bs_b.png", self.graphics + "bs_b.png")
		copyfile(self.templates + config.plugins.PlatoonHD.MenuColor.value + "/bs_bl.png", self.graphics + "bs_bl.png")
		copyfile(self.templates + config.plugins.PlatoonHD.MenuColor.value + "/bs_br.png", self.graphics + "bs_br.png")
		copyfile(self.templates + config.plugins.PlatoonHD.MenuColor.value + "/bs_l.png", self.graphics + "bs_l.png")
		copyfile(self.templates + config.plugins.PlatoonHD.MenuColor.value + "/bs_r.png", self.graphics + "bs_r.png")
		copyfile(self.templates + config.plugins.PlatoonHD.MenuColor.value + "/bs_t.png", self.graphics + "bs_t.png")
		copyfile(self.templates + config.plugins.PlatoonHD.MenuColor.value + "/bs_tl.png", self.graphics + "bs_tl.png")
		copyfile(self.templates + config.plugins.PlatoonHD.MenuColor.value + "/bs_tr.png", self.graphics + "bs_tr.png")
		copyfile(self.templates + config.plugins.PlatoonHD.MenuColor.value + "/dvd_background.png", self.graphics + "dvd_background.png")
		copyfile(self.templates + config.plugins.PlatoonHD.MenuColor.value + "/full_background.png", self.graphics + "full_background.png")
		copyfile(self.templates + config.plugins.PlatoonHD.MenuColor.value + "/infobar_background.png", self.graphics + "infobar_background.png")
		copyfile(self.templates + config.plugins.PlatoonHD.MenuColor.value + "/mediaplayer_background.png", self.graphics + "mediaplayer_background.png")
		copyfile(self.templates + config.plugins.PlatoonHD.MenuColor.value + "/menu_background.png", self.graphics + "menu_background.png")
		copyfile(self.templates + config.plugins.PlatoonHD.MenuColor.value + "/player_background.png", self.graphics + "player_background.png")
		copyfile(self.templates + config.plugins.PlatoonHD.MenuColor.value + "/pvrstate_background.png", self.graphics + "pvrstate_background.png")
		copyfile(self.templates + config.plugins.PlatoonHD.MenuColor.value + "/shift_background.png", self.graphics + "shift_background.png")
		copyfile(self.templates + config.plugins.PlatoonHD.MenuColor.value + "/sib_background.png", self.graphics + "sib_background.png")
		copyfile(self.templates + config.plugins.PlatoonHD.MenuColor.value + "/virtualkeyboard_background.png", self.graphics + "virtualkeyboard_background.png")
		copyfile(self.templates + config.plugins.PlatoonHD.MenuColor.value + "/volume_background.png", self.graphics + "volume_background.png")
		copyfile(self.templates + config.plugins.PlatoonHD.MenuColor.value + "/webradio_background.png", self.graphics + "webradio_background.png")
		if self.E2DistroVersion == "openhdf":
			copyfile(self.templates + config.plugins.PlatoonHD.MenuColor.value + "/infobarepg_background.png", self.graphics + "infobarepg_background.png")
			copyfile(self.templates + config.plugins.PlatoonHD.MenuColor.value + "/infobareventview_background.png", self.graphics + "infobareventview_background.png")
			copyfile(self.templates + config.plugins.PlatoonHD.MenuColor.value + "/virtualkeyboard_background2.png", self.graphics + "virtualkeyboard_background2.png")

	def changeColor(self, name, color):
		color = color[-6:]
		r = int(color[0:2], 16)
		g = int(color[2:4], 16)
		b = int(color[4:6], 16)

		img = Image.open(self.templates + color + '/' + name + ".png")
		mask1 = Image.new("RGBA", img.size, (r, g, b, 0))
		mask2 = Image.new("L", img.size, 213)
		im = Image.composite(img, mask1, mask2)
		im.save(self.graphics + name + ".png")

	def makeSelectionpng(self):
		self.makeGradientpng("sel_30", 1220, 30, config.plugins.PlatoonHD.SelectionColor1.value, config.plugins.PlatoonHD.SelectionColor2.value)
		self.makeGradientpng("sel_32", 1196, 32, config.plugins.PlatoonHD.SelectionColor1.value, config.plugins.PlatoonHD.SelectionColor2.value)
		self.makeGradientpng("sel_36", 1196, 36, config.plugins.PlatoonHD.SelectionColor1.value, config.plugins.PlatoonHD.SelectionColor2.value)
		self.makeGradientpng("sel_40", 870, 40, config.plugins.PlatoonHD.SelectionColor1.value, config.plugins.PlatoonHD.SelectionColor2.value)
		self.makeGradientpng("sel_45", 747, 45, config.plugins.PlatoonHD.SelectionColor1.value, config.plugins.PlatoonHD.SelectionColor2.value)
		self.makeGradientpng("sel_50", 765, 50, config.plugins.PlatoonHD.SelectionColor1.value, config.plugins.PlatoonHD.SelectionColor2.value)
		self.makeGradientpng("sel_53", 736, 54, config.plugins.PlatoonHD.SelectionColor1.value, config.plugins.PlatoonHD.SelectionColor2.value)
		self.makeGradientpng("sel_60", 747, 60, config.plugins.PlatoonHD.SelectionColor1.value, config.plugins.PlatoonHD.SelectionColor2.value)
		self.makeGradientpng("sel_70", 765, 70, config.plugins.PlatoonHD.SelectionColor1.value, config.plugins.PlatoonHD.SelectionColor2.value)
		self.makeGradientpng("sel_75", 736, 75, config.plugins.PlatoonHD.SelectionColor1.value, config.plugins.PlatoonHD.SelectionColor2.value)
		self.makeGradientpng("sel_90", 870, 90, config.plugins.PlatoonHD.SelectionColor1.value, config.plugins.PlatoonHD.SelectionColor2.value)
		self.makeGradientpng("sel_110", 736, 110, config.plugins.PlatoonHD.SelectionColor1.value, config.plugins.PlatoonHD.SelectionColor2.value)
		self.makeGradientpng("sel_135", 736, 136, config.plugins.PlatoonHD.SelectionColor1.value, config.plugins.PlatoonHD.SelectionColor2.value)

	def makeGradientpng(self, name, width, height, color1, color2):
		color1 = color1[-6:]
		r1 = int(color1[0:2], 16)
		g1 = int(color1[2:4], 16)
		b1 = int(color1[4:6], 16)
		color2 = color2[-6:]
		r2 = int(color2[0:2], 16)
		g2 = int(color2[2:4], 16)
		b2 = int(color2[4:6], 16)

		gradient = Image.new("RGBA", (1, height), (r2, g2, b2, 255))
		for pos in range(0, height):
			p = pos / float(height)
			r = r2 * p + r1 * (1 - p)
			g = g2 * p + g1 * (1 - p)
			b = b2 * p + b1 * (1 - p)
			gradient.putpixel((0, pos), (int(r), int(g), int(b), 255))
		gradient = gradient.resize((width, height))
		gradient.save(self.graphics + name + ".png")

	def hexRGB(self, color):
		color = color[-6:]
		r = int(color[0:2], 16)
		g = int(color[2:4], 16)
		b = int(color[4:6], 16)
		return (r << 16)|(g << 8) | b

	def RGB(self, r, g, b):
		return (r << 16) | (g << 8) | b
