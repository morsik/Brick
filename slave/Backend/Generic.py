import shlex
import subprocess
import time

def printts(ts_start, msg):
	ts = "[%12.2f]" % (time.time() - ts_start)
	print("%s %s" % (ts, msg.rstrip().replace('\r', '\r%s ' % ts)))

# check this:
# http://sharats.me/the-ever-useful-and-neat-subprocess-module.html#watching-both-stdout-and-stderr
def BackendExecute(cmdline):
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

		print("Total command time: %.2fs" % (time.time() - ts_start))
	except OSError as msg:
		aftertime = ""
		if ts_start:
			aftertime = " after %.2fs" % (time.time() - ts_start)

		print("\033[1;31mCommand failed%s\033[0m" % (aftertime))
		print("\033[1;37mCommand:\033[0m %s" % (cmdline))
