import logging
logging.basicConfig(level=logging.INFO)
from jira import JIRA

class Base():

	def __init__(self, user, apikey, server):
		
		options = {
		'server': server,
		'agile_rest_path': 'agile'
		}
		self.jira = JIRA(options, basic_auth=(user,apikey))
