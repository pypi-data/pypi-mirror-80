import logging
logging.basicConfig(level=logging.INFO)

class User(Base):

	def __init__(self):
		self.self = None
		self.name = None
		self.emailAddress = None
		self.displayName = None
		self.active = None
		self.timeZone = None
		
	
	def find(self,id_or_key): 
		try:
			logging.info("Start function: find")
	
			#TO DO
	
			logging.info("End function: find")
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
		    logging.error(e.__dict__) 
