import logging
logging.basicConfig(level=logging.INFO)
from .base import Base

class Project(Base):

	def __init__(self, user, apikey, server):
		Base.__init__(self, user, apikey, server)
		
	def find_all(self): 
		try:
			logging.info("Start function: find_all")
			return self.jira.projects()	
			self.jira.__init__
			logging.info("End function: find_all")
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 
	
	def find_issue(self, project_key):
		try:
			logging.info("Start function: find_issue")
			return self.jira.search_issues('project='+project_key)
			logging.info("End function: find_issue")
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

	def find_user(self, project_key):
		try:
			logging.info("Start function: find_user")
			return self.jira.search_assignable_users_for_projects("",project_key)
			logging.info("End function: find_user")
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

	def find_role(self, project_key):
		try:
			logging.info("Start function: find_role")
			return self.jira.project_roles(project_key)
			logging.info("End function: find_role")
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

	# Function to take a project by key
	def find_project(self, project_key):
		try:
			logging.info("Start function: find_project")
			return self.jira.project(project_key)
			logging.info("End funcion: find_project")
		except Exception as e:
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__)

	def find_board(self, project_key):
		try:
			logging.info("Start function: find_board")
			return self.jira.boards(projectKeyOrID=project_key)
			logging.info("End funcion: find_board")
		except Exception as e:
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__)

	def find_sprint(self, board_id):
		try:
			logging.info("Start function: find_sprint")
			return self.jira.sprints(board_id)
			logging.info("End funcion: find_sprint")
		except Exception as e:
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__)

	def find_epic(self, project_key):
		try:
			logging.info("Start function: find_epic")
			return self.jira.search_issues(f'project = {project_key} AND issuetype = Epic')
			logging.info("End function: find_epic")
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 
