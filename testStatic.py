class A:
	def __init__(self):
		self.a = 1
		self.b = 2

	def call_static(self):
		B.static_me()

class B:
	def static_me():
		print("fu")

a = A()
a.call_static()