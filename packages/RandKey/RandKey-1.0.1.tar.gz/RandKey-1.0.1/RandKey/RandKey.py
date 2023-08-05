import string, random

def GenKey(size=64):
	letters = string.ascii_letters + "1234567890"
	s = ""
	for i in range(size):
		s += random.choice(letters)
	return s