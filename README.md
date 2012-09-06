Wallpaper daemon with dbus control

DEPENDENCES:
        dbus-python
        imagemagic
        hsetroot
	xrandr

INSTALLATION:
        * make install:
            /usr/local/bin/wppd, /usr/local/bin/moonclock
            /usr/local/share/wppd/moon/E-MoonClock-??.png
        
        * PREFIX=/usr make install


COMMANDLINE:
        * wppd --help    prints usage
        * wppd [--timeout=SEC] [--shuffle=on|off] [--moon=on|off] 
               [--walldir=dir] [--moonpos=pos] [--save]
        
                --moon = on|off - draw a phase os moon.
		--moonpos = NorthWest|North|NorthEast|West
		            |Center|East|SouthWest|South|SouthEast
                --walldir = dir - Directory where wallpapers stored.
        
        * wppd delete|next|kill
                remote control

        * moonclock
                prints the moon phase, it is file in /usr/[local]/share/wppd/moon/

CONFIG FILE:
        $HOME/.config/wppd/config
        
        
