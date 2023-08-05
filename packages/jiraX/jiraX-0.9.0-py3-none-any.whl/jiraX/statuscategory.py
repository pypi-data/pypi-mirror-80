import logging
logging.basicConfig(level=logging.INFO)

class StatusCategory(Base):

	def __init__(self):
		self.self = None
		self.id = None
		self.key = None
		self.colorName = None
		
