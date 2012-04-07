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
PREFIX = './'
HOME = os.getenv('HOME')
MOONCLOCK='moonclock/moonclock'
MOONS_DIR =  os.path.join(PREFIX, 'share/wppd/moon')
CACHE = os.path.join(HOME, '.cache', 'wppd')
CONFIG = os.path.join(HOME, '.config', 'wppd')
CONFIG_FILE = os.path.join(CONFIG, 'config')
WALLPP_PTH = os.path.join(CACHE, 'wallpaper.png')
SHUFFLE = False
TIMEOUT = 60*3.0
MOON = True
WALLPAPERS_DIR = os.path.abspath(u'.')

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
				SHUFFLE = bool(arg)
			elif opt == 'moon':
				MOON = bool(arg)
			elif opt == 'wallpapers':
				WALLPAPERS_DIR = arg

		pass
	

def strconf():
	ret = u"timeout=%f\n" % TIMEOUT
	ret += u"shuffle=%s\n" % str(SHUFFLE)
	ret += u"moon=%s\n" % str(MOON)
	ret += "wallpapers=%s" % WALLPAPERS_DIR
	return ret

def save_config():
	with codecs.open(CONFIG_FILE, "w", 'utf-8') as f:
		f.write("timeout=%f\n" % TIMEOUT)
		f.write("shuffle=%s\n" % str(SHUFFLE) )
		f.write("moon=%s\n" % str(MOON) )
		f.write("wallpapers=%s" % WALLPAPERS_DIR )

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
		sys.exit()

	if 'next' in sys.argv:
		Next()
		sys.exit()
	if 'kill' in sys.argv:
		killwppd()
		sys.exit()

	read_config()
	gopts = ['timeout=', 'shuffle=', 'moon=', 'walldir=', 'save']
	try:
		optlist, args = getopt.getopt(sys.argv[1:], '', gopts)
	except	getopt.GetoptError, err:
		print u'error', str(err)
		sys.exit(1)



	if ('--help', '') in optlist:
		usage()
		sys.exit()

	save = False
	global TIMEOUT, SHUFFLE, MOON, WALLPAPERS_DIR
	for opt,arg in optlist:
		if opt == '--timeout':
			TIMEOUT = float(arg)
		elif opt == '--shuffle':
			SHUFFLE = True if arg=='on' else False
		elif opt == '--moon':
			MOON = True if arg=='on' else False
		elif opt == '--walldir':
			WALLPAPERS_DIR = arg
		elif opt == '--save':
			save = True
	
	print strconf()
	if save:
		save_config()


def Next():
	import dbus
	bus = dbus.SessionBus()
	remote_object = bus.get_object(dbus_path, "/Mescaline")
	rc = remote_object.Next(dbus_interface = dbus_path)

def usage():
	print ("usage: ")
	print ("       %s" % "wppd --help" )
	print ("       %s" % "wppd [--timeout=SEC] [--shuffle=on|off] [--moon=on|off] [--walldir=dir] [--save]" )
	print ("       %s" % "wppd delete|next|kill" )

parse_cmd()
