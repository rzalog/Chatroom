import os
import subprocess

def clear_screen():
	if os.name in ('nt','dos'):
		subprocess.call("cls")
	elif os.name in ('linux','osx','posix'):
		subprocess.call("clear")
	else:
		print('\n'*120)
