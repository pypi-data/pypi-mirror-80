import logging
logging.basicConfig(level=logging.INFO)

class Resolution(Base):

	def __init__(self):
		self.self = None
		self.description = None
		self.iconUrl = None
		self.name = None
		
