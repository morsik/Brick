from time import sleep

_working = False


def isFree():
	global _working
	if _working:
		return False
	return True


def setWorking(isworking):
	global _working
	_working = isworking


def doTask(cmd):
	setWorking(True)

	i = 0
	import random
	slmax = random.randint(1, 10)
	while i <= slmax:
		print("Sleep %i/%i..." % (i, slmax))
		sleep(1)
		i += 1

	setWorking(False)
	return True
