class HeaderSection{
	def _init_(self, iD, qR, opCODE, rd, qDCOUNT):
		self.iD = iD
		self.qR = qR
		self.opCODE = opCODE
		self.rd = rd
		self.qDCOUNT = qDCOUNT
	def _str_(self):
		return "Header Material %d, %d, %d, %d, %d"(self.iD, self.qR, self.opCODE, self.rd, self.qDCOUNT)
	def _repr_(self):
		return str(self)
}