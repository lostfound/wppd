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


import os,random, time, getopt, sys
from subprocess import *
from Queue import Queue, Empty
from threading import Thread
from config import MOONS_DIR, WALLPP_PTH, SHUFFLE, TIMEOUT, MOON, WALLPAPERS_DIR, parse_cmd, MOONCLOCK, dbus_path, killwppd

q = Queue()
def daemon():
	parent = os.getpid()
	os.fork()
	if os.getpid() == parent:
		sys.exit(0)


def read_config():
	HOME = os.getenv('HOME')


def get_moon_image_path ():
	popn = Popen(MOONCLOCK, stdout = PIPE)
	imgpth = os.path.join(MOONS_DIR, popn.stdout.read().strip().rstrip())
	popn.wait()
	return imgpth

def gen_wallpaper(source, moon=None):
	if MOON:
		if moon == None:
			moon = get_moon_image_path ()
		Popen( [ 'convert', '-mosaic', source, moon, WALLPP_PTH ] ).wait()
	else:
		Popen( [ 'cp', source, WALLPP_PTH ] ).wait()

def main():
	wallpapers = map(lambda nm: os.path.join(WALLPAPERS_DIR, nm), os.listdir(WALLPAPERS_DIR))
	if not SHUFFLE:
		rowallpapers = map(lambda x: x, wallpapers)

	if not wallpapers:
		print "Error: there are no wallpapers"
		sys.exit()

	while True:
		cwp = random.choice(wallpapers)
		if not SHUFFLE:
			wallpapers.remove(cwp)
			if not wallpapers:
				wallpapers = map(lambda x: x, rowallpapers)

		gen_wallpaper(cwp)
		Popen("hsetroot -full %s" % WALLPP_PTH, shell = True).wait()
		try:
			task = q.get(timeout=TIMEOUT)
			q.task_done()
			if task == "del":
				os.remove(cwp)
				try: wallpapers.remove(cwp)
				except: pass
				try: rowallpapers.remove(cwp)
				except: pass
		except Empty:
			pass
		


if __name__ == "__main__":
	parse_cmd()
	import dbus, dbus.service, dbus.mainloop.glib
	import gobject

class DbusCtrl(dbus.service.Object):
	def __init__ (s, bus, name):
		dbus.service.Object.__init__(s, bus, name)
	@dbus.service.method(dbus_path, in_signature='', out_signature='')
	def Next(s):
		q.put( "" )
	@dbus.service.method(dbus_path, in_signature='', out_signature='')
	def Delete(s):
		q.put( "del" )
if __name__ == "__main__":
	killwppd()
	daemon()
	gobject.threads_init()

	dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
	session_bus = dbus.SessionBus()
	name = dbus.service.BusName(dbus_path, session_bus)
	object = DbusCtrl(session_bus, '/Mescaline')
	Thread(target=main).start()

	loop = gobject.MainLoop()
	loop.run()
