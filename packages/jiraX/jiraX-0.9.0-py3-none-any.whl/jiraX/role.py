import logging
logging.basicConfig(level=logging.INFO)
from .base import Base

class Role(Base):

	def __init__(self, user, apikey, server):
		Base.__init__(self, user, apikey, server)

	def find_by_proj_and_id(self, project_key, id):
		try:
			logging.info("Start function: find_by_proj_and_id")
			return self.jira.project_role(project_key, id)	
			logging.info("End function: find_by_proj_and_id")
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

