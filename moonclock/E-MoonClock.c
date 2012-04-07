/*

 *      E-MoonClock v0.1 (C) 1999-2000 Michael Lea (mikelea@charm.net)
 *
 *              - Shows Moon Phase....
 *
 *      I am incredibly indebted to Mike Henderson, the original author of
 *      wmMoonClock.  He did the hard stuff, I ported it to an epplet.
 *
 *
 *      This program is free software; you can redistribute it and/or modify
 *      it under the terms of the GNU General Public License as published by
 *      the Free Software Foundation; either version 2, or (at your option)
 *      any later version.
 *
 *      This program is distributed in the hope that it will be useful,
 *      but WITHOUT ANY WARRANTY; without even the implied warranty of
 *      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *      GNU General Public License for more details.
 *
 *      You should have received a copy of the GNU General Public License
 *      along with this program (see the file COPYING); if not, write to the
 *      Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 *      Boston, MA  02111-1307, USA
 *
 */

#include <sys/time.h>
#include <sys/resource.h>
#include <stdio.h>
#include <time.h>
#include "CalcEphem.h"

char               *moon_image = "E-MoonClock-01.png";
double              interval = 1000.0;


static void print_moonclock()
{
   struct tm          *GMTTime, *LocalTime;
   int                 Year, Month, DayOfMonth;
   int                 ImageNumber;
   time_t              CurrentLocalTime, CurrentGMTTime, date;
   double              UT, LocalHour, hour24();
   double              TimeZone;
   CTrans              c;
   static char         buf[1024];

   CurrentGMTTime = time(NULL);
   GMTTime = gmtime(&CurrentGMTTime);
   UT = GMTTime->tm_hour + GMTTime->tm_min / 60.0 + GMTTime->tm_sec / 3600.0;
   Year = GMTTime->tm_year + 1900;
   Month = GMTTime->tm_mon + 1;
   DayOfMonth = GMTTime->tm_mday;
   date = Year * 10000 + Month * 100 + DayOfMonth;
   CurrentLocalTime = CurrentGMTTime;
   LocalTime = localtime(&CurrentLocalTime);
   LocalHour =
      LocalTime->tm_hour /*+ 1/*Tomsk*/ + LocalTime->tm_min / 60.0 +
      LocalTime->tm_sec / 3600.0;
   TimeZone = UT - LocalHour;

   CalcEphem(date, UT, &c);

   ImageNumber = (int)(c.MoonPhase * 60.0 + 0.5);
   if (ImageNumber > 60)
      ImageNumber = 1;

   sprintf(buf,"E-MoonClock-%02d.png", ImageNumber);
   
   printf("%s\n", buf);

}

int
main(int argc, char **argv)
{

   print_moonclock();
   return 0;
}
