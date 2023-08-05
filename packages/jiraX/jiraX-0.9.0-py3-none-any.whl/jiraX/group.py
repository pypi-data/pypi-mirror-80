import logging
logging.basicConfig(level=logging.INFO)

class Group(Base):

	def __init__(self):
		self.name = None
		self.self = None
		
