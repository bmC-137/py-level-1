import json
import string
import random
import requests
from pprint import pprint

base_url = 'https://api.....'
empty = ''
emptyspace = ' '


string_pool = [x for x in string.ascii_uppercase + string.ascii_lowercase]

def genString(max_len):
		# random_string = ''.join([random.choice(string.ascii_lowercase + string.ascii_uppercase) for n in range(size)])
		l = toInt(max_len)
		s = []
		for i in range l:
			_index = random.randint(0, len())

		return random_string
# randomString = genString(10)

def toInt(val):
	try:
		v = int(varl)
		return v
	except (ValueError, TypeError):
		return 0

def genInteger(min, max):
		random_int = [random.randint(min,max)]
		return random_int
# randomInt = genInteger(-180,180)

def genIntStr(size):
		random_string = ''.join([random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase) for n in range(size)])
		return random_string
# randomIntStr = genIntStr(10):

def genFloat(min, max):
	_base = random.randint(min, max)
	_rem =  random.randint(0, 99) / 100
	return _base + _rem


def extract_dataType(parameters):
	datatype = str()
	for param in parameters:
		if 'dataType' in param:
			datatype = param['dataType']
	return datatype

def extract_default_values(parameters):
	result = dict()
	for param in parameters:
		if 'defaultValue' in param:
			result[param['name']] = param['defaultValue']
	return result

class makePost:
	def __init__(self):
		self.payload = {}
		self.propertiesList = []
		self.listErrors = []
		self.listNoErrors = []
		self.listNoDataType = []
		self.newPayload = {}
	def printInfo(self):
		print(self.listErrors)
		print(self.listNoErrors)
		print(self.listNoDataType)
	def randomDataGenerator(self, type, min, max):
		pass
	def assignNewData(self):
		pass
	def getInfo(self):
		global resource
		resources = requests.get(base_url + '/resources').json()['apis']
		for resource in resources:
			apis = requests.get(base_url + resource['path']).json()['apis']
			for api in apis:
				post_url = base_url + api['path']
				post_element = post_url.split('/')
				url_description = base_url + '/resources/' + post_element[6]
				for operation in api['operations']:
					if (operation['httpMethod'] == 'POST' and operation['nickname'] == 'create'):
					# if (operation['httpMethod'] == 'POST'):
						if '/delete/' in api['path'] or \
								'oversizes' in api['path'] or \
								'quotation' in api['path'] or \
								'vcard' in api['path'] or \
								'copy' in api['path'] or \
								'files' in api['path'] or \
								'documentation' in api['path']:
							continue
						try:
							# default_parameters = extract_default_values(operation['parameters'])
							dataType = extract_dataType(operation['parameters'])
							if (dataType == 'none' or dataType == 'null'or dataType == empty or dataType == emptyspace):
								print(post_element[6])
								self.listNoDataType.append(post_element[6])
								continue
							# pprint(default_parameters)
							# print(dataType)
							get_dataType = requests.get(url_description).json()['models'][dataType]
							# print(get_dataType, end='\n')
							self.propertiesList = []
							for prop in get_dataType['properties']:
								self.propertiesList.append(prop)
							# none = ''
							self.payload = { prop: empty for prop in self.propertiesList }
							# self.randomDataGenerator()
							for k in self.payload:
								self.newPayload[k] = 'randomData'
							pprint(self.newPayload)
							self.listNoErrors.append(post_element[6])
							print('POST to: ' + base_url + api['path'] + ': ')
							print('URL parameters:' + url_description)
							################################## Testing random values.
							# randomString = genString(10)
							# print(randomString)
							# randomInt = genInteger(-180,180)
							# print(randomInt)
							# randomIntStr = genIntStr(10)
							# print(randomIntStr)
							self.clearData()
						except KeyError:
							self.listErrors.append(post_element[6])
							pass
						except ValueError:
							print('ValueError...')
		# self.randomDataGenerator()
			exit()
	def clearData(self):
		self.payload = {}
		self.propertiesList = []


runMe = makePost()

# print('List with errors: ', list_errors)
# print('List that will be Posted to: ', list_noerrors)
# print('List with no datatype: ', list_noDataType)


if __name__ == '__main__':
	runMe.getInfo()
	# runMe.printInfo()
	# runMe.randomDataGenerator()

