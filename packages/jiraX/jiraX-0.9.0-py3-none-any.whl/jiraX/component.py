import logging
logging.basicConfig(level=logging.INFO)

class Component(Base):

	def __init__(self):
		self.self = None
		self.name = None
		self.description = None
		self.assigneeType = None
		self.realAssigneeType = None
		self.isAssigneeTypeValid = None
		
