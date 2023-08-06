from cimpy.cgmes_v2_4_15.Base import Base


class AngleDegrees(Base):
	'''
	Measurement of angle in degrees.

	:value:  Default: 0.0
	:unit:  Default: None
	:multiplier:  Default: None
		'''

	cgmesProfile = Base.cgmesProfile

	possibleProfileList = {'class': [cgmesProfile.DI.value, cgmesProfile.DY.value, cgmesProfile.EQ.value, cgmesProfile.SV.value, cgmesProfile.SSH.value, ],
						'value': [cgmesProfile.DI.value, cgmesProfile.DY.value, cgmesProfile.EQ.value, cgmesProfile.SV.value, cgmesProfile.SSH.value, ],
						'unit': [cgmesProfile.DI.value, cgmesProfile.DY.value, cgmesProfile.EQ.value, cgmesProfile.SV.value, cgmesProfile.SSH.value, ],
						'multiplier': [cgmesProfile.DI.value, cgmesProfile.DY.value, cgmesProfile.EQ.value, cgmesProfile.SV.value, cgmesProfile.SSH.value, ],
						 }

	serializationProfile = {}

	

	def __init__(self, value = 0.0, unit = None, multiplier = None,  ):
	
		self.value = value
		self.unit = unit
		self.multiplier = multiplier
		
	def __str__(self):
		str = 'class=AngleDegrees\n'
		attributes = self.__dict__
		for key in attributes.keys():
			str = str + key + '={}\n'.format(attributes[key])
		return str
