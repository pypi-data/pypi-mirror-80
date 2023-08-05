import logging
logging.basicConfig(level=logging.INFO)

class Priority(Base):

	def __init__(self):
		self.self = None
		self.statusColor = None
		self.description = None
		self.iconUrl = None
		self.name = None
		
