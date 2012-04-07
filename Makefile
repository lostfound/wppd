ifeq ("${PREFIX}", "")
PREFIX=/usr/local
endif

all:
	make -C moonclock

install: all
	echo ${PREFIX}/lib
	install -D moonclock/moonclock $(PREFIX)/bin/moonclock
	install -D config.py $(PREFIX)/lib/wppd/config.py
	install -D wppd.py $(PREFIX)/lib/wppd/wppd.py
	mkdir -m 0755 -p $(PREFIX)/share/wppd/moon
	install -m 0644 share/wppd/moon/* $(PREFIX)/share/wppd/moon
	ln -sf $(PREFIX)/lib/wppd/wppd.py $(PREFIX)/bin/wppd

uninstall:
	rm -f $(PREFIX)/bin/moonclock $(PREFIX)/bin/wppd
	rm -rf $(PREFIX)/lib/wppd
	rm -rf  $(PREFIX)/share/wppd
