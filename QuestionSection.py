class QuestionSection{
	def _init_(self, qName, qType):
		self.qName = qName
		self.qType = 1
	def _str_(self):
		return "Question Material %s, %d"(self.qName, self.qType)
	def _repr_(self):
		return str(self)
}