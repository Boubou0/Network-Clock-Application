import pyprctl
import sys
import time

for cap in set(pyprctl.Cap):
    if cap != pyprctl.Cap.SYS_TIME:
        pyprctl.cap_effective.drop(cap)
        pyprctl.cap_permitted.drop(cap)

time.clock_settime(time.CLOCK_REALTIME, float(sys.argv[1]))
