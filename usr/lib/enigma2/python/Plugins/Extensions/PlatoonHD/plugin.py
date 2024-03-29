# -*- coding: utf-8 -*-
#
#  Plugin Code
#
#  Coded/Modified/Adapted by oerlgrey
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

from __future__ import absolute_import
from Plugins.Plugin import PluginDescriptor
from Components.config import config
from Components.Language import language
from os import environ
import gettext
from Tools.Directories import resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from . import PlatoonHD

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
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("PlatoonHD", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/PlatoonHD/locale/"))

def _(txt):
	t = gettext.dgettext("PlatoonHD", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t

def main(session, **kwargs):
	global python3
	try:
		if python3:
			from six.moves import reload_module
			reload_module(PlatoonHD)
			session.open(PlatoonHD.PlatoonHD)
		else:
			reload(PlatoonHD)
			session.open(PlatoonHD.PlatoonHD)
	except:
		import traceback
		traceback.print_exc()

def Plugins(**kwargs):
	try:
		from boxbranding import getImageDistro
		if getImageDistro() in ("teamblue", "openhdf"):
			if config.skin.primary_skin.value == "PlatoonHD/skin.xml":
				list = []
				list.append(PluginDescriptor(name="MyPlatoonHD", description=_("MyPlatoonHD-Settings"), where=PluginDescriptor.WHERE_PLUGINMENU, icon='plugin.png', fnc=main))
				return list
			else:
				list = []
				return list
		else:
			list = []
			return list
	except ImportError:
		list = []
		return list
