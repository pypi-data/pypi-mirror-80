import logging
logging.basicConfig(level=logging.INFO)

class Dashboard(Base):

	def __init__(self):
		self.id = None
		self.name = None
		self.self = None
		self.view = None
		
	
	def find_all(self): 
		try:
			logging.info("Start function: find_all")
	
			#TO DO
	
			logging.info("End function: find_all")
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
		    logging.error(e.__dict__) 
	
	def find(self,id): 
		try:
			logging.info("Start function: find")
	
			#TO DO
	
			logging.info("End function: find")
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
		    logging.error(e.__dict__) 
