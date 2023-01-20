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

from __future__ import absolute_import
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop
from Components.ActionMap import ActionMap
from Components.AVSwitch import AVSwitch
from Components.config import config, configfile, ConfigYesNo, ConfigSubsection, getConfigListEntry, ConfigSelection, ConfigNumber, ConfigText, ConfigInteger, ConfigClock, ConfigSlider, ConfigBoolean
from Components.ConfigList import ConfigListScreen
from Components.Sources.StaticText import StaticText
from Components.Pixmap import Pixmap
from Components.Label import Label
from Components.Sources.CanvasSource import CanvasSource
from PIL import Image
from Components.Language import language
import gettext, time, os
from enigma import ePicLoad, eTimer
from Tools.Directories import fileExists, resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from shutil import move, copyfile

python3 = False

try:
	import six
	if six.PY2:
		python3 = False
	else:
		python3 = True
except ImportError:
	python3 = False

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

ColorList = [
	("F0A30A", _("Amber")),
	("B27708", _("Amber dark")),
	("1B1775", _("Blue")),
	("00002F", _("Blue dark")),
	("7D5929", _("Brown")),
	("3F2D15", _("Brown dark")),
	("0050EF", _("Cobalt")),
	("001F59", _("Cobalt dark")),
	("1BA1E2", _("Cyan")),
	("0F5B7F", _("Cyan dark")),
	("FFC000", _("Yellow")),
	("999999", _("Grey")),
	("3F3F3F", _("Grey dark")),
	("70AD11", _("Green")),
	("213305", _("Green dark")),
	("6D8764", _("Olive")),
	("313D2D", _("Olive dark")),
	("C3461B", _("Orange")),
	("892E13", _("Orange dark")),
	("035468", _("Petrol")),
	("02404A", _("Petrol dark")),
	("F472D0", _("Pink")),
	("723562", _("Pink dark")),
	("E51400", _("Red")),
	("330400", _("Red dark")),
	("000000", _("Black")),
	("008A00", _("Emerald")),
	("647687", _("Steel")),
	("262C33", _("Steel dark")),
	("6C0AAB", _("Violet")),
	("1F0333", _("Violet dark")),
	("FFFFFF", _("White"))
	]

config.plugins.PlatoonHD = ConfigSubsection()
config.plugins.PlatoonHD.MenuColor = ConfigSelection(default = "3F3F3F", choices = ColorList)
config.plugins.PlatoonHD.MenuColor2 = ConfigText(default = "")
config.plugins.PlatoonHD.MenuFont1 = ConfigSelection(default = "FFFFFF", choices = ColorList)
config.plugins.PlatoonHD.MenuFont2 = ConfigSelection(default = "FFC000", choices = ColorList)
config.plugins.PlatoonHD.WindowColor = ConfigSelection(default = "00002F", choices = ColorList)
config.plugins.PlatoonHD.WindowFont1 = ConfigSelection(default = "FFFFFF", choices = ColorList)
config.plugins.PlatoonHD.WindowFont2 = ConfigSelection(default = "FFC000", choices = ColorList)
config.plugins.PlatoonHD.SelectionColor1 = ConfigSelection(default = "892E13", choices = ColorList)
config.plugins.PlatoonHD.SelectionColor2 = ConfigText(default = "")
config.plugins.PlatoonHD.SelectionFont = ConfigSelection(default = "FFFFFF", choices = ColorList)
config.plugins.PlatoonHD.ButtonFont = ConfigSelection(default = "FFFFFF", choices = ColorList)
config.plugins.PlatoonHD.Progress = ConfigSelection(default = "C3461B", choices = ColorList)

config.plugins.PlatoonHD.MenuTrans = ConfigSelection(default = "11", choices = [
				("11", _("low")),
				("3F", _("high"))
				])

config.plugins.PlatoonHD.WindowTrans = ConfigSelection(default = "17", choices = [
				("00", _("off")),
				("17", _("low")),
				("2E", _("medium")),
				("45", _("high"))
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
		self["version"] = StaticText("Version 2.1.5")

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
			"cancel": self.exit,
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

		self["config"].list = list
		self["config"].l.setList(list)
		self.updateHelp()
		self["helperimage"].hide()
		self.ShowPicture()

		# preview
		self.showPreview()

	def showPreview(self):
		option = self["config"].getCurrent()[1]

		if option == config.plugins.PlatoonHD.SelectionColor1:
			self.showGradient(config.plugins.PlatoonHD.SelectionColor1.value, self.calcSecondcolor(config.plugins.PlatoonHD.SelectionColor1.value))
		elif option == config.plugins.PlatoonHD.MenuColor:
			self.showGradient(config.plugins.PlatoonHD.MenuColor.value, self.calcSecondcolor(config.plugins.PlatoonHD.MenuColor.value))
		elif option in (config.plugins.PlatoonHD.WindowColor, config.plugins.PlatoonHD.WindowFont1, config.plugins.PlatoonHD.WindowFont2, config.plugins.PlatoonHD.MenuFont1, config.plugins.PlatoonHD.MenuFont2, config.plugins.PlatoonHD.SelectionFont, config.plugins.PlatoonHD.Progress):
			self.showColor(self.hexRGB(option.value))
		elif option == config.plugins.PlatoonHD.WindowTrans:
			if option.value == "00":
				self.showText(30, _("no transparency"))
			elif option.value == "17":
				self.showText(30, _("low transparency"))
			elif option.value == "2E":
				self.showText(30, _("medium transparency"))
			elif option.value == "45":
				self.showText(30, _("high transparency"))
		elif option == config.plugins.PlatoonHD.MenuTrans:
			if option.value == "11":
				self.showText(30, _("low transparency"))
			elif option.value == "3F":
				self.showText(30, _("high transparency"))
		else:
			self["helperimage"].show()

	def updateHelp(self):
		cur = self["config"].getCurrent()
		if cur:
			self["description"].text = cur[2]

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

	def reboot(self):
		restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _("Do you really want to reboot now?"), MessageBox.TYPE_YESNO)
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
		config.plugins.PlatoonHD.MenuColor2.value = self.calcSecondcolor(config.plugins.PlatoonHD.MenuColor.value)
		config.plugins.PlatoonHD.MenuColor2.save()
		self.skinSearchAndReplace.append(['name="PlatoonGYbg2" value="#113A3A3A', 'name="PlatoonGYbg2" value="#' + config.plugins.PlatoonHD.MenuTrans.value + config.plugins.PlatoonHD.MenuColor2.value])

		# fonts
		self.skinSearchAndReplace.append(['name="PlatoonBKfg1" value="#00FFFFFF', 'name="PlatoonBKfg1" value="#00' + config.plugins.PlatoonHD.WindowFont1.value])
		self.skinSearchAndReplace.append(['name="foreground" value="#00FFFFFF', 'name="foreground" value="#00' + config.plugins.PlatoonHD.WindowFont1.value])
		self.skinSearchAndReplace.append(['name="PlatoonBKfg2" value="#00FFC000', 'name="PlatoonBKfg2" value="#00' + config.plugins.PlatoonHD.WindowFont2.value])
		self.skinSearchAndReplace.append(['name="PlatoonGYfg1" value="#00FFFFFF', 'name="PlatoonGYfg1" value="#00' + config.plugins.PlatoonHD.MenuFont1.value])
		self.skinSearchAndReplace.append(['name="PlatoonButtonfg" value="#00FFFFFF', 'name="PlatoonButtonfg" value="#00' + config.plugins.PlatoonHD.MenuFont1.value])
		self.skinSearchAndReplace.append(['name="PlatoonGYfg2" value="#00FFC000', 'name="PlatoonGYfg2" value="#00' + config.plugins.PlatoonHD.MenuFont2.value])
		self.skinSearchAndReplace.append(['name="PlatoonSelfg" value="#00FFFFFF', 'name="PlatoonSelfg" value="#00' + config.plugins.PlatoonHD.SelectionFont.value])

		# progress
		self.skinSearchAndReplace.append(['name="PlatoonProgress" value="#00C3461B', 'name="PlatoonProgress" value="#00' + config.plugins.PlatoonHD.Progress.value])

		# icons
		if config.plugins.PlatoonHD.MenuColor.value in ("FFFFFF", "F0A30A", "1BA1E2", "FFC000"):
			self.skinSearchAndReplace.append(['icons-light', 'icons-dark'])
		if config.plugins.PlatoonHD.WindowColor.value in ("FFFFFF", "F0A30A", "1BA1E2", "FFC000", "999999", "70AD11", "F472D0"):
			self.skinSearchAndReplace.append(['global-icons', 'icons-dark'])
			self.skinSearchAndReplace.append(['name="PlatoonIconfg" value="#00FFFFFF', 'name="PlatoonIconfg" value="#00000000'])
			self.skinSearchAndReplace.append(['name="PlatoonLine" value="#00FFFFFF', 'name="PlatoonLine" value="#00000000'])

		# selection background
		self.skinSearchAndReplace.append(['name="PlatoonSelbg" value="#0086350D', 'name="PlatoonSelbg" value="#00' + config.plugins.PlatoonHD.SelectionColor1.value])
		config.plugins.PlatoonHD.SelectionColor2.value = self.calcSecondcolor(config.plugins.PlatoonHD.SelectionColor1.value)
		config.plugins.PlatoonHD.SelectionColor2.save()

		# graphics
		self.changeMenuColors()
		self.makeSelectionpng()

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
		restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _("GUI needs a restart to apply the settings.\nDo you want to Restart the GUI now?"), MessageBox.TYPE_YESNO)
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
		askExit = self.session.openWithCallback(self.doExit, MessageBox, _("Do you really want to exit without saving?"), MessageBox.TYPE_YESNO)
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
		from . import ping
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
		self.makeBackgroundpng("bs_b", "bs_b", config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuTrans.value)
		self.makeBackgroundpng("bs_bl", "bs_bl", config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuTrans.value)
		self.makeBackgroundpng("bs_br", "bs_br", config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuTrans.value)
		self.makeBackgroundpng("bs_l", "bs_l", config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuTrans.value)
		self.makeBackgroundpng("bs_r", "bs_r", config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuTrans.value)
		self.makeBackgroundpng("bs_t", "bs_t", config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuTrans.value)
		self.makeBackgroundpng("bs_tl", "bs_tl", config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuTrans.value)
		self.makeBackgroundpng("bs_tr", "bs_tr", config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuTrans.value)
		self.makeBackgroundpng("dvd", "dvd_background", config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuColor2.value, config.plugins.PlatoonHD.MenuTrans.value)
		self.makeBackgroundpng("full", "full_background", config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuColor2.value, config.plugins.PlatoonHD.MenuTrans.value)
		self.makeBackgroundpng("infobar", "infobar_background", config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuColor2.value, config.plugins.PlatoonHD.MenuTrans.value)
		self.makeBackgroundpng("mediaplayer", "mediaplayer_background", config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuColor2.value, config.plugins.PlatoonHD.MenuTrans.value)
		self.makeBackgroundpng("menu", "menu_background", config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuColor2.value, config.plugins.PlatoonHD.MenuTrans.value)
		self.makeBackgroundpng("player", "player_background", config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuColor2.value, config.plugins.PlatoonHD.MenuTrans.value)
		self.makeBackgroundpng("pvrstate", "pvrstate_background", config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuColor2.value, config.plugins.PlatoonHD.MenuTrans.value)
		self.makeBackgroundpng("shift", "shift_background", config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuColor2.value, config.plugins.PlatoonHD.MenuTrans.value)
		self.makeBackgroundpng("sib", "sib_background", config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuColor2.value, config.plugins.PlatoonHD.MenuTrans.value)
		self.makeBackgroundpng("webradio", "webradio_background", config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuColor2.value, config.plugins.PlatoonHD.MenuTrans.value)
		self.makeBackgroundpng("volume", "volume_background", config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuTrans.value)
		if self.E2DistroVersion == "teamblue":
			self.makeBackgroundpng("virtualkeyboard", "virtualkeyboard_background", config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuColor2.value, config.plugins.PlatoonHD.MenuTrans.value)
		elif self.E2DistroVersion == "openhdf":
			self.makeBackgroundpng("infobarepg", "infobarepg_background", config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuColor2.value, config.plugins.PlatoonHD.MenuTrans.value)
			self.makeBackgroundpng("infobareventview", "infobareventview_background", config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuColor2.value, config.plugins.PlatoonHD.MenuTrans.value)
			self.makeBackgroundpng("virtualkeyboard2", "virtualkeyboard2_background", config.plugins.PlatoonHD.MenuColor.value, config.plugins.PlatoonHD.MenuColor2.value, config.plugins.PlatoonHD.MenuTrans.value)

	def makeBackgroundpng(self, input, output, color1, color2, trans):
		color1 = color1[-6:]
		r1 = int(color1[0:2], 16)
		g1 = int(color1[2:4], 16)
		b1 = int(color1[4:6], 16)
		color2 = color2[-6:]
		r2 = int(color2[0:2], 16)
		g2 = int(color2[2:4], 16)
		b2 = int(color2[4:6], 16)
		trans = 255 - int(trans, 16)

		mask = Image.open(self.templates + input + "_mask.png").convert('L')
		border = Image.open(self.templates + input + "_border.png")
		gradient = Image.new("RGBA", (1, mask.size[1]), (r2, g2, b2, trans))
		for pos in range(0, mask.size[1]):
			p = pos / float(mask.size[1])
			r = r2 * p + r1 * (1 - p)
			g = g2 * p + g1 * (1 - p)
			b = b2 * p + b1 * (1 - p)
			gradient.putpixel((0, pos), (int(r), int(g), int(b), trans))
		gradient = gradient.resize(mask.size)
		border.paste(gradient, (0, 0), mask)
		border.save(self.graphics + output + ".png")

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

	def calcSecondcolor(self, color):
		color = color[-6:]
		r1 = int(color[0:2], 16)
		r2 = r1 - 24
		if r2 <= 0:
			r2 = 0
		g1 = int(color[2:4], 16)
		g2 = g1 - 24
		if g2 <= 0:
			g2 = 0
		b1 = int(color[4:6], 16)
		b2 = b1 - 24
		if b2 <= 0:
			b2 = 0
		secondcolor = str(hex(r2)[2:4]).zfill(2) + str(hex(g2)[2:4]).zfill(2) + str(hex(b2)[2:4]).zfill(2)
		return secondcolor

	def hex2dec(self, color):
		dec = int(color, 16)
		return str(dec)

	def hexRGB(self, color):
		color = color[-6:]
		r = int(color[0:2], 16)
		g = int(color[2:4], 16)
		b = int(color[4:6], 16)
		return (r << 16) | (g << 8) | b

	def RGB(self, r, g, b):
		return (r << 16) | (g << 8) | b
