# -*- coding: utf-8 -*-

#  Text Translator Converter
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

from Components.Converter.Converter import Converter
from os import environ
from Components.Element import cached
from Tools.Directories import resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from Components.Language import language
import gettext

lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("PlatoonHD", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/PlatoonHD/locale/"))

def _(txt):
	t = gettext.dgettext("PlatoonHD", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t

class PlatoonHDTextTranslator(Converter, object):
	def __init__(self, type):
		Converter.__init__(self, type)
		self.type = type

	@cached
	def getText(self):
		if self.type == "itfollows":
			return _('it follows:')
		elif self.type == "coming":
			return _('coming:')
		elif self.type == "runsuntil":
			return _('runs until')
		elif self.type == "timeshiftactive":
			return _('timeshift active')
		elif self.type == "untillive":
			return _('until live:')
		elif self.type == "name":
			return _('Name')
		elif self.type == "birthday":
			return _('Birthday')
		elif self.type == "age":
			return _('Age')
		elif self.type == "brsettings":
			return _('Birthday Reminder Settings')
		elif self.type == "brpath":
			return _('Select a path for the birthday file')
		elif self.type == "channellist":
			return _('Channellist')
		elif self.type == "movielist":
			return _('Movielist')
		elif self.type == "secondinfobar":
			return _('Second Infobar')
		elif self.type == "screensaver":
			return _('Screensaver')
		elif self.type == "favorites":
			return _('Favorites')

	text = property(getText)
