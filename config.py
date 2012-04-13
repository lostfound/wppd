#!/usr/bin/python
# -*- coding: utf8 -*-

#
# Copyright (C) 2010  Platon Peacel☮ve <platonny@ngs.ru>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os, sys, getopt
import codecs
from subprocess import * 

dbus_path = "mescaline.gnu.org"
pname = os.path.abspath(sys.argv[0])
if pname.startswith('/usr/local'):
	PREFIX = u'/usr/local'
	MOONCLOCK = u'/usr/local/bin/moonclock'
elif  pname.startswith('/usr/'):
	PREFIX = u'/usr/'
	MOONCLOCK='/usr/bin/moonclock'
else:
	PREFIX = './'
	MOONCLOCK='moonclock/moonclock'
HOME = os.getenv('HOME')
MOONS_DIR =  os.path.join(PREFIX, 'share/wppd/moon')
CACHE = os.path.join(HOME, '.cache', 'wppd')
CONFIG = os.path.join(HOME, '.config', 'wppd')
CONFIG_FILE = os.path.join(CONFIG, 'config')
WALLPP_PTH = os.path.join(CACHE, 'wallpaper.png')
BLANK_PTH = os.path.join(CACHE, 'blank.png')
SHUFFLE = False
TIMEOUT = 60*3.0
MOON = True
WALLPAPERS_DIR = os.path.abspath(u'.')
MOONGRAVITY = "SouthEast"
GRAVITIES = ["NorthWest", "North", "NorthEast", "West", "Center", "East", "SouthWest", "South", "SouthEast"]

def get_display_size():
	popn = Popen(["xrandr", "-q"], stdout = PIPE)
	lines = filter( lambda x: '*' in x, popn.stdout.read().split("\n") )
	popn.wait()
	ret = lines[0].strip('\t ').split()[0]
	return ret

DISPLAY_SIZE = get_display_size()


def str_to_bool(arg):
	if arg.lower() in ['on', 'true', 'yes']:
		return True
	else:
		return False

def set_moongravity(gravity):
	global MOONGRAVITY
	if gravity.lower() in map( lambda x: x.lower(), GRAVITIES):
		MOONGRAVITY = gravity
	else:
		MOONGRAVITY = GRAVITIES[0]


def read_config():
	if not os.path.exists( CACHE ):
		os.makedirs(CACHE, 0700 )

	if not os.path.exists( CONFIG ):
		os.makedirs(CONFIG, 0700 )

	try:
		with codecs.open(CONFIG_FILE, "r", 'utf-8') as f:
			lines = map(lambda x: x.rstrip(), f.readlines())
	except:
		pass
	else:
		global WALLPAPERS_DIR, MOON, SHUFFLE, TIMEOUT
		for opt,arg in  map(lambda x: x.split('=',1), lines):
			opt = opt.rstrip()
			arg = arg.lstrip()
			if opt == 'timeout':
				TIMEOUT = float(arg)
			elif opt == 'shuffle':
				SHUFFLE = str_to_bool(arg)
			elif opt == 'moon':
				MOON = str_to_bool(arg)
			elif opt == "moonpos":
				set_moongravity(arg)
			elif opt == 'wallpapers':
				WALLPAPERS_DIR = arg

		pass
	

def strconf():
	ret = u"timeout=%f\n" % TIMEOUT
	ret += u"shuffle=%s\n" % str(SHUFFLE)
	ret += u"moon=%s\n" % str(MOON)
	ret += u"moonpos=%s\n" % MOONGRAVITY
	ret += u"wallpapers=%s" % WALLPAPERS_DIR
	return ret

def save_config():
	with codecs.open(CONFIG_FILE, "w", 'utf-8') as f:
		f.write( strconf() )

def killwppd():
	rx = Popen("ps ax | grep python", shell=True, stdout=PIPE)
	rx.wait()
	l = rx.stdout.readlines()
	pids = filter(None, map(lambda x: int(x.strip().split()[0]) if x.find('wppd') != -1 else None, l))
	pids.remove(os.getpid())
	for p in pids:
		os.kill(p, 9)
		
def parse_cmd():
	if '--help' in sys.argv:
		usage()
		sys.exit()

	if 'delete' in sys.argv:
		Delete()
		sys.exit()

	if 'next' in sys.argv:
		Next()
		sys.exit()
	if 'kill' in sys.argv:
		killwppd()
		sys.exit()

	read_config()
	gopts = ['timeout=', 'shuffle=', 'moon=', 'walldir=', 'moonpos=', 'save']
	try:
		optlist, args = getopt.getopt(sys.argv[1:], '', gopts)
	except	getopt.GetoptError, err:
		print u'error', str(err)
		sys.exit(1)



	if ('--help', '') in optlist:
		usage()
		sys.exit()

	save = False
	global TIMEOUT, SHUFFLE, MOON, WALLPAPERS_DIR, MOONGRAVITY
	for opt,arg in optlist:
		if opt == '--timeout':
			TIMEOUT = float(arg)
		elif opt == '--shuffle':
			SHUFFLE = str_to_bool(arg)
		elif opt == '--moon':
			MOON = str_to_bool(arg)
		elif opt == '--moonpos':
			set_moongravity(arg)
		elif opt == '--walldir':
			WALLPAPERS_DIR = arg
		elif opt == '--save':
			save = True
	
	print ""
	if save:
		save_config()


def Delete():
	import dbus
	bus = dbus.SessionBus()
	remote_object = bus.get_object(dbus_path, "/Mescaline")
	rc = remote_object.Delete(dbus_interface = dbus_path)
def Next():
	import dbus
	bus = dbus.SessionBus()
	remote_object = bus.get_object(dbus_path, "/Mescaline")
	rc = remote_object.Next(dbus_interface = dbus_path)

def usage():
	print ("usage: ")
	print ("       %s" % "wppd --help" )
	print ("")
	print ("       %s" % "wppd [--timeout=SEC] [--shuffle=on|off] [--moon=on|off]\n" +
	       "       %s" % "     [--walldir=dir] [--moonpos=position] [--save]" )
	print ("       %s" % "position = NorthWest|North|NorthEast|West|Center|East|SouthWest|South|SouthEast")
	print ("")
	print ("       %s" % "wppd delete|next|kill" )

parse_cmd()
