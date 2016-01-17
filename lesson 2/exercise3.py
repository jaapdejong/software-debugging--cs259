#!/usr/bin/python
# Implement checkRep on this ZIPCode class
#
# Valid zip codes are 5 digits long, where each digit
# is between 0-9


class ZIPCode:
    # US Only
    
	def __init__(self, zip):
		self._zip = zip
		self.checkRep()

	def zip(self):
		return self._zip

	def checkRep(self):
		assert len(self.zip()) == 5
		# add in your asserts to ensure this is a valid ZIP code
		assert self.zip().isdigit()
		assert "00000" <= self.zip() <= "99999"

	
# a = ZIPCode("12345")
# a = ZIPCode("00000")
# a = ZIPCode("99999")
# a = ZIPCode("12-56")
# a = ZIPCode("123456")
# a = ZIPCode("1234")
# a = ZIPCode("A")

