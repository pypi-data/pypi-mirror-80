import logging
logging.basicConfig(level=logging.INFO)
from .base import Base

class Comment(Base):

	def __init__(self, user, apikey, server):
		Base.__init__(self, user, apikey, server)
		
	def find_by_issue(self, issue_object): 
		try:
			logging.info("Start function: find_by_id")
			comments = self.jira.comments(issue_object)
			if comments is not None:
				return comments
			return []
			logging.info("End function: find_by_id")
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 
		
