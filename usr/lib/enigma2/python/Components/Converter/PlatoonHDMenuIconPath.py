# -*- coding: utf-8 -*-

#  Menu Icon Path Converter
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
from Components.Element import cached
from Tools.Directories import fileExists
from Components.Converter.Poll import Poll

class PlatoonHDMenuIconPath(Poll, Converter, object):
	def __init__(self, type):
		Poll.__init__(self)
		Converter.__init__(self, type)
		self.poll_interval = 100
		self.poll_enabled = True
		self.type = str(type)
		self.path = "/usr/share/enigma2/PlatoonHD/menu-icons/"
		
		self.names = [
		("about_screen", "info.png"),
		("animation_setup", "setup.png"),
		("aspectratio_switch", "screen.png"),
		("audio_menu", "audio.png"),
		("audio_setup", "audio.png"),
		("auto_scan", "tuner.png"),
		("autolanguage_setup", "language.png"),
		("autores_setup", "screen.png"),
		("autoshutdown_setup", "shutdowntimer.png"),
		("autotimer_setup", "timer.png"),
		("av_setup", "movie_list.png"),
		("blindscan", "tuner.png"),
		("buttonsetup_setup", "setup.png"),
		("cablescan", "tuner.png"),
		("cam_setup", "setup.png"),
		("channelselection_setup", "setup.png"),
		("ci_assign", "setup.png"),
		("ci_setup", "setup.png"),
		("cooltvguide", "epg.png"),
		("crontimer_edit", "timer.png"),
		("deep_standby", "shutdown.png"),
		("default_lists", "paket.png"),
		("default_wizard", "paket.png"),
		("device_manager", "hdd.png"),
		("device_screen", "hdd.png"),
		("device_setup", "hdd.png"),
		("devicemanager", "hdd.png"),
		("devices_menu", "hdd.png"),
		("display_selection", "look.png"),
		("display_setup", "look.png"),
		("dns_setup", "net.png"),
		("dreamplex", "plugin.png"),
		("dvd_player", "dvd.png"),
		("dvdplayer", "dvd.png"),
		("dvdplayer_setup", "dvd.png"),
		("ecm_info", "tuner.png"),
		("epg_menu", "epg.png"),
		("epg_settings", "epg.png"),
		("epg_setup", "epg.png"),
		("epgloadsave_menu", "epg.png"),
		("epgrefresh", "epg.png"),
		("extended_selection", "setup.png"),
		("factory_reset", "reset.png"),
		("fansetup_config", "setup.png"),
		("fastscan", "tuner.png"),
		("harddisk_check", "hdd.png"),
		("harddisk_convert", "hdd.png"),
		("harddisk_init", "hdd.png"),
		("harddisk_setup", "hdd.png"),
		("hardisk_selection", "hdd.png"),
		("hardreset", "restart.png"),
		("hdmicec", "setup.png"),
		("hotkey_setup", "remote.png"),
		("inadyn_setup", "net.png"),
		("info_screen", "info.png"),
		("infopanel", "info.png"),
		("input_device_setup", "remote.png"),
		("ipbox_client_Start", "net.png"),
		("keyboard", "keyb.png"),
		("keyboard_setup", "keyb.png"),
		("language_setup", "language.png"),
		("lcd4linux", "plugin.png"),
		("lcd_setup", "setup.png"),
		("lcd_skin_setup", "setup.png"),
		("led_giga", "setup.png"),
		("ledmanager", "setup.png"),
		("loadepgcache", "setup.png"),
		("logs_setup", "setup.png"),
		("maintenance_mode", "reset.png"),
		("manual_scan", "tuner.png"),
		("media_player", "movie_list.png"),
		("mediaportal", "plugin.png"),
		("merlin_music_player", "audio.png"),
		("minidlna_setup", "net.png"),
		("movie_list", "movie_list.png"),
		("moviebrowser", "movie_list.png"),
		("multi_quick", "plugin.png"),
		("netafp_setup", "net.png"),
		("netftp_setup", "net.png"),
		("netmounts_setup", "net.png"),
		("netnfs_setup", "net.png"),
		("netrts_setup", "net.png"),
		("netsabnzbd_setup", "net.png"),
		("netsatpi_setup", "net.png"),
		("netsmba_setup", "net.png"),
		("nettelnet_setup", "net.png"),
		("netushare_setup", "net.png"),
		("netvpn_setup", "net.png"),
		("network_info_screen", "info.png"),
		("network_menu", "net.png"),
		("network_setup", "net.png"),
		("numzapext_setup", "remote.png"),
		("openstore", "net.png"),
		("openwebif", "setup.png"),
		("osd3dsetup", "screen.png"),
		("osd_position_setup", "screen.png"),
		("osd_setup", "screen.png"),
		("osdsetup", "screen.png"),
		("parental_setup", "look.png"),
		("password_setup", "net.png"),
		("picturecenterfs", "picture.png"),
		("plugin_select", "plugin.png"),
		("plugin_selection", "plugin.png"),
		("pluginhider_setup", "setup.png"),
		("positioner_setup", "tuner.png"),
		("powertimer_edit", "timer.png"),
		("primary_skin_selector", "gui.png"),
		("pvmc_mainmenu", "setup.png"),
		("rcu select", "setup.png"),
		("rec_setup", "setup.png"),
		("recording_menu", "hdd.png"),
		("recording_setup", "hdd.png"),
		("recordpaths", "hdd.png"),
		("remote_setup", "remote.png"),
		("remotecode", "remote.png"),
		("remotecontrolcode", "remote.png"),
		("rfmod_setup", "setup.png"),
		("run_kodi", "movie_list.png"),
		("sat_ip_client", "net.png"),
		("satfinder", "tuner.png"),
		("saveepgcache", "movie_list.png"),
		("scart_switch", "setup.png"),
		("select_menu", "setup.png"),
		("service_info_screen", "info.png"),
		("service_searching_selection", "tuner.png"),
		("setup_epgenhanced", "setup.png"),
		("setup_epggraphical", "setup.png"),
		("setup_epginfobar", "setup.png"),
		("setup_epginfobargraphical", "setup.png"),
		("setup_epgmulti", "setup.png"),
		("setup_selection", "setup.png"),
		("sibsetup", "setup.png"),
		("skin_setup", "setup.png"),
		("sleep", "timer.png"),
		("software_manager", "restart.png"),
		("software_update", "restart.png"),
		("specialfeatures_menu", "setup.png"),
		("standby", "power.png"),
		("standby_restart_list", "shutdowntimer.png"),
		("start_kodi", "movie_list.png"),
		("startwizzard", "paket.png"),
		("streamconvert", "net.png"),
		("streaming_clients_info_screen", "info.png"),
		("subtitle_selection", "setup.png"),
		("subtitle_setup", "setup.png"),
		("sundtek_control_enter", "setup.png"),
		("supportchannel_ytchannel", "plugin.png"),
		("system_selection", "setup.png"),
		("tempfancontrol", "setup.png"),
		("time_setup", "timer.png"),
		("timer_edit", "timer.png"),
		("timer_menu", "timer.png"),
		("timezone_setup", "setup.png"),
		("timshift_setup", "setup.png"),
		("tuner_setup", "tuner.png"),
		("ui_menu", "gui.png"),
		("undefined", "keyb.png"),
		("usage_setup", "setup.png"),
		("user_interface", "gui.png"),
		("vfd_ew", "setup.png"),
		("vfd_ini", "setup.png"),
		("video_clipping", "movie_list.png"),
		("video_finetune", "screen.png"),
		("video_menu", "screen.png"),
		("video_setup", "screen.png"),
		("videoenhancement_setup", "screen.png"),
		("vmc_init_setup", "setup.png"),
		("vmc_init_startvmc", "movie_list.png"),
		("volume_adjust", "audio.png"),
		("vps", "movie_list.png"),
		("webradiofs", "audio.png"),
		("yamp", "plugin.png"),
		("yamp_music_player", "plugin.png"),
		("youtube_tv", "plugin.png")
		]
	
	@cached
	def getText(self):
		try:
			cur = self.source.current
			if cur and len(cur) > 2:
				selection = cur[2]
				name = self.path + selection + ".png"
				if fileExists(name):
					return name
				name = ""
				for pair in self.names:
					if pair[0] == selection.lower():
						name = self.path + pair[1]
						if name != "" and fileExists(name):
							return name
		except:
			pass
		name = self.path + "setup.png"
		if fileExists(name):
			return name
	
	text = property(getText)
