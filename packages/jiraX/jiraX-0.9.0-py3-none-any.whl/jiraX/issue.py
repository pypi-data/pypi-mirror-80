import logging
logging.basicConfig(level=logging.INFO)
from .base import Base

class Issue(Base):

	def __init__(self, user, apikey, server):
		Base.__init__(self, user, apikey, server)
		
	def find_by_id(self, issue_id): 
		try:
			logging.info("Start function: find_by_id")
			return self.jira.issue(issue_id)
			logging.info("End function: find_by_id")
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

	def find_by_sprint(self, sprint_id):
		try:
			logging.info("Start function: find_by_sprint")
			return self.jira.search_issues(f"Sprint={sprint_id}")
			logging.info("End function: find_by_sprint")
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 


