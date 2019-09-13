import sys

class ColoredText(object):
	_state = []

	@staticmethod
	def builder(colorCode):
		return lambda *args: ColoredText(colorCode, *args)

	def __init__(self, colorCode, args=None):
		self.colorCode = colorCode
		self.text = args

	def __call__(self, *args):
		return ColoredText(self.colorCode, list(args))

	def __str__(self):
		ColoredText._state.append(self.colorCode)
		out = self.colorCode + u''.join(map(unicode, self.text))
		ColoredText._state.pop()
		out += u'\033[0m' # END
		for elem in ColoredText._state:
			out += elem
		return out

	def __enter__(self):
		ColoredText._state.append(self.colorCode)
		sys.stdout.write(self.colorCode)

	def __exit__(self, type, value, traceback):
		ColoredText._state.pop()
		out = u'\033[0m' # END
		for elem in ColoredText._state:
			out += elem
		sys.stdout.write(out)

	@staticmethod
	def add(left, right):
		left = left if isinstance(left, ColoredText) else ColoredText(u'', [left])
		right = right if isinstance(right, ColoredText) else ColoredText(u'', [right])

		if left.text is None:
			return ColoredText(left.colorCode + right.colorCode)
		elif left.colorCode == right.colorCode:
			return ColoredText(left.colorCode, left.text + right.text)
		else:
			return ColoredText(u'', [left, right])

	def __add__(left, right):
		return ColoredText.add(left, right)
	def __radd__(right, left):
		return ColoredText.add(left, right)

	def strip(self):
		return ColoredText(self.colorCode, [elem.strip() for elem in self.text])

Regular = ColoredText(u'')
Purple = ColoredText(u'\033[95m')
Cyan = ColoredText(u'\033[96m')
DarkCyan = ColoredText(u'\033[36m')
Blue = ColoredText(u'\033[94m')
Green = ColoredText(u'\033[92m')
Yellow = ColoredText(u'\033[93m')
Red = ColoredText(u'\033[91m')
Bold = ColoredText(u'\033[1m')
Underline = ColoredText(u'\033[4m')
