import logging
logging.basicConfig(level=logging.INFO)

class Attachment(Base):

	def __init__(self):
		self.self = None
		self.filename = None
		self.created = None
		self.size = None
		self.mimeType = None
		self.content = None
		self.thumbnail = None
		
