wppd
=======

Wallpaper daemon with dbus control

## Dependences:

  * dbus-python
  * imagemagic
  * hsetroot
  * xrandr

## Installation:

Type this command as root:

    $ make install:
or

    $ PREFIX=/usr make install

## Files & Directories:

    * /usr/local/bin/wppd
    * /usr/local/bin/moonclock
    * /usr/local/lib/wppd
    * /usr/local/share/wppd/moon/E-MoonClock-??.png

## COMMANDLINE:

    * wppd --help    prints usage
    * wppd [--timeout=SEC] [--shuffle=on|off] [--moon=on|off] 
           [--walldir=dir] [--moonpos=pos] [--save]
        
           --moon = on|off - draw a phase os moon.
           --moonpos = NorthWest|North|NorthEast|West
	               |Center|East|SouthWest|South|SouthEast
           --walldir = dir - Directory where wallpapers stored.
        
    * wppd delete|next|kill
               - remote control

    * moonclock
               - prints the moon phase, it is file in /usr/[local]/share/wppd/moon/

## Config file:

    $HOME/.config/wppd/config
        
        

