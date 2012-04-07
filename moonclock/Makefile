moonclock: CalcEphem.o E-MoonClock.o Moon.o
	gcc -o $@ -O2 $^ -lm

CalcEphem.o: CalcEphem.c CalcEphem.h
	gcc -o $@ -c $<

E-MoonClock.o: E-MoonClock.c CalcEphem.h
	gcc -o $@ -c $<

Moon.o: Moon.c
	gcc -o $@ -c $<

clean:
	rm -f CalcEphem.o E-MoonClock.o Moon.o
