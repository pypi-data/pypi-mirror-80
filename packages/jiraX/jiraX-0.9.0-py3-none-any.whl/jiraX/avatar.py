import logging
logging.basicConfig(level=logging.INFO)

class Avatar(Base):

	def __init__(self):
		self.size = None
		self.url = None
		
