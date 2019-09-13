import math, sys
from rooms import rooms
from multicolor import *

roomMap = file('map.txt', 'r').read().decode('utf-8').split('\n')

#sortedRooms = sorted([(name, coords, size) for name, (type, _, coords, size) in rooms.items()], key=lambda x: x[1][::-1])

def drawMap(roomStyle):
	roomChunks = []
	for y, line in enumerate(roomMap):
		y += 1
		for x, c in enumerate(line):
			x += 1
			found = None
			border = False
			for name, (_, _, coords, size) in rooms.items():
				if x >= coords[0] and y >= coords[1] and x < coords[0] + size[0] and y < coords[1] + size[1]:
					found = name
					if x == coords[0] or y == coords[1] or x == coords[0] + size[0] - 1 or y == coords[1] + size[1] - 1:
						border = True
					break
			if not found or found not in roomStyle:
				sys.stdout.write(c.encode('utf-8'))
				continue
			_, _, coords, size = rooms[found]
			bs, fs, text = roomStyle[found]
			to = (int(math.ceil(size[0] / 2.0 - len(text) / 2.0)) + coords[0]) if text is not None else 0
			if border:
				val = bs(c)
			elif text is not None and y == coords[1] + 2 and to <= x < to + len(text):
				val = fs(unicode(text[x - to]))
			else:
				val = fs(c)
			sys.stdout.write(unicode(val).encode('utf-8'))

		sys.stdout.write('\n')
