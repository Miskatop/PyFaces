# Function Arguments generators
class call:
	def __init__(self, fun, *args):
		self.args = list(args)
		self.fun = fun

	def __call__(self, *args, **kwargs):
		args = list(args)
		args.extend(self.args)
		self.fun(*args, **kwargs)