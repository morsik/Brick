import sys
import time

_working = False


def isFree():
	global _working
	if _working:
		return False
	return True


def setWorking(isworking):
	global _working
	_working = isworking


# check this:
# http://sharats.me/the-ever-useful-and-neat-subprocess-module.html#watching-both-stdout-and-stderr
#
def doTask(cmdline):
	print("cmdline: \033[0;33m%s\033[0m" % cmdline)
	setWorking(True)

	import subprocess, shlex

	out = ""
	ts_start = None
	try:
		p = subprocess.Popen(shlex.split(str(cmdline)), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		ts_start = time.time()
		while p.poll() is None:
			ln = p.stdout.readline()
			if ln:
				printts(ts_start, ln)
			#out += ln

		print("Total command time: %.8fs" % (time.time() - ts_start))
	except OSError as msg:
		aftertime = ""
		if ts_start:
			aftertime = " after %.8fs" % (time.time() - ts_start)

		print("\033[1;31mCommand failed%s\033[0m" % (aftertime))
		print("\033[1;37mCommand:\033[0m %s" % (cmdline))

	setWorking(False)
	return True


def printts(ts_start, msg):
	print("[%12.4f] %s" % (time.time() - ts_start, msg.rstrip()))
