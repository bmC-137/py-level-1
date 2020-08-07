import string
import random
import requests
from pprint import pprint
import time
import multiprocessing


# To.Do


# 3. Fix end Types of URL for better Posts
# 4. Try to clean... and structure it
# 5. make menu, with options.... whyyy... for training.

base_url = 'https://api.exmaple.com/dev/index.php'
empty = ''
emptyspace = ' '


def genString(size):
	strPool = [x for x in string.ascii_uppercase + string.ascii_lowercase]
	m = toInt(size)
	s = []
	for i in range(m):
		y = random.randint(0, len(strPool) - 1)
		s.append(strPool[y])
	return ''.join(s)


def genIntStr(max):
	random_string = ''.join([random.choice(string.ascii_lowercase + string.ascii_uppercase) for n in range(max)])
	return random_string


def genFloat(min, max):
	b = random.randint(min, max)
	r = random.randint(0, 99) / 100
	return b + r


def genInt(min, max):
	random_int = int(random.randint(min, max))
	return random_int


def toInt(val):
	try:
		v = int(val)
		return v
	except (ValueError, TypeError):
		print('errurr')
		return 0


def extract_dataType(parameters):
	datatype = str()
	for param in parameters:
		if 'dataType' in param:
			datatype = param['dataType']
	return datatype


def extract_urlType(parameters):
	urlType = list()
	for param in parameters:
		if 'allowableValues' in param:
			urlType = param['allowableValues']
		return urlType


def extract_default_values(parameters):
	result = dict()
	for param in parameters:
		if 'defaultValue' in param:
			result[param['name']] = param['defaultValue']
	return result


def data_gen(type_, min_, max_):
	# global val_
	min_ = int(min_)
	max_ = int(max_)
	# print(type_, min_, max_)
	try:
		if 'empty_string' in type_:
			val_ = empty
		elif type_ == 'int':
			val_ = genInt(min_, max_)
		elif type_ == 'string':
			val_ = genString(max_)
		elif type_ == 'string|int':
			try:
				val_ = genString(max_)
			except:
				val_ = int(10)
		elif type_ == 'float':
			val_ = genFloat(min_, max_)
		elif type_ == 'Array':
			val_ = genString(max_)
		elif type_ == 'array|string':
			val_ = genString(max_)
		elif type_:
			print('Generating random string for type: ', type_)
			val_ = genString(max_)
		else:
			pass
	except (ValueError, UnboundLocalError):
		# print(e)
		pass
	return val_


def makePostReq(url, payload, addr):
	def func1(u, p):
		r = requests.post(u, json=p)
		print(r.text)

	try:
		if url and payload and addr:
			u = url
			p = payload
			a = addr
			func1(u, p)
	except:
		pass


class makePost:
	def __init__(self):
		self.payload = {}
		self.propertiesList = []
		self.allowValues = []
		self.newPayload = {}
		self.uniq_values = []
		#### junk lists
		self.listErrors = []
		self.listNoErrors = []
		self.listNoDataType = []

	def printInfo(self):
		print('List with Errors, or addresses the script wasnt able to send POST request:', self.listErrors)
		print('POST List: ', self.listNoErrors)
		print('Missing dataType List: ', self.listNoDataType)

	def uniqValues(self):
		l = set(self.allowValues)
		self.uniq_values = list(l)
		return self.uniq_values

	def cleanUniqValues(self):
		self.allowValues = []
		self.uniq_values = []

	def clearPayload(self):
		self.newPayload = {}

	def showNewPayload(self):
		print(self.newPayload)

	def findValues(self, postelement):
		url_des = requests.get(base_url + '/resources/' + postelement).json()['apis']
		for des in url_des:
			for operation in des['operations']:
				if operation['httpMethod'] == 'POST':
					for o in operation['parameters']:
						try:
							if o['allowableValues']['valueType'] == 'LIST':
								for u in o['allowableValues']['values']:
									if u:
										self.allowValues.append(u)
									else:
										continue
						except:
							continue
		if len(self.allowValues) == 0:
			pass
		else:
			print('POST Value types : ', self.uniqValues())

	def makeJob(self, resource):
		apis = requests.get(base_url + resource['path']).json()['apis']
		for api in apis:
			post_url = base_url + api['path']
			post_element = post_url.split('/')
			url_description = base_url + '/resources/' + post_element[6]
			for operation in api['operations']:
				# if (operation['httpMethod'] == 'POST' and operation['nickname'] == 'create'):
				# start_time = time.time()
				if operation['httpMethod'] == 'POST':
					if '/delete/' in api['path'] or \
							'oversizes' in api['path'] or \
							'quotation' in api['path'] or \
							'vcard' in api['path'] or \
							'copy' in api['path'] or \
							'files' in api['path'] or \
							'incomingdeliverynotes' in api['path'] or \
							'documentation' in api['path']:
						continue
					try:
						dataType = extract_dataType(operation['parameters'])
						# url_type = extract_urlType(operation['parameters'])
						# pprint(url_type)
						if dataType == 'none' or dataType == 'null' or dataType == empty or dataType == emptyspace:
							print(post_element[6])
							self.listNoDataType.append(post_element[6])
							continue
						get_dataType = requests.get(url_description).json()['models'][dataType]
						self.propertiesList = []
						for prop in get_dataType['properties']:
							self.propertiesList.append(prop)
						self.payload = {prop: empty for prop in self.propertiesList}
						print('POST to: ' + base_url + api['path'] + ': ')
						print('URL parameters:' + url_description)
						# POST Value Types:
						self.cleanUniqValues()
						self.findValues(post_element[6])
						for k in self.payload:
							element = post_element[6]
							url_gen = \
								requests.get(base_url + '/resources' + '/' + element).json()['models'][dataType][
									'properties'][k]
							# print(url_gen)
							min_ = 1
							max_ = 5
							type_ = empty
							try:
								# if url_gen['type'] == 'Array' or \
								# 		url_gen['type'] == 'boolean' or \
								# 		url_gen['type'] == 'Parameter' or \
								# 		url_gen['type'] == 'ApprovalMsg' or \
								# 		url_gen['type'] == 'ReminderMsg' or \
								# 		url_gen['type'] == 'UpdateQRMsg':
								# 	continue
								type_ = url_gen['type']
								max_ = url_gen['maximum']
								min_ = url_gen['minimum']
								# print(randomInt)
								if '@max 10' in url_gen['description']:
									max_ = 10
							except:
								pass
							pp = data_gen(type_, min_, max_)
							# print(k, pp)
							self.newPayload[k] = pp
						# print(pp)
						# print(len(self.uniq_values))
						pprint(self.newPayload)
						if len(self.uniq_values) == 0:
							url_ = base_url + api['path']
							makePostReq(url_, self.newPayload, api['path'])
						else:
							# print(self.uniq_values)
							for u_ in self.uniq_values:
								# print(u_)
								url_ = base_url + api['path'].format(type=u_)
								print(url_)
								makePostReq(url_, self.newPayload, api['path'])
						self.listNoErrors.append(post_element[6])
						# self.clearData()
						# self.cleanUniqValues()
					except KeyError:
						self.listErrors.append(post_element[6])
						pass
					except ValueError:
						print('ValueError...')
						pass
					print('\n')
					self.cleanUniqValues()
					self.clearPayload()
					# duration = time.time() - start_time
					# print(f"It took {duration} seconds")
	# exit()


	# def getInfo(self):
	# 	# global resource
	# 	resources = requests.get(base_url + '/resources').json()['apis']
	# 	for resource in resources:
	# 		self.makeJob(resource)

	def getInfo(self):
		# global resource
		resources = requests.get(base_url + '/resources').json()['apis']
		with multiprocessing.Pool() as pool:
			pool.map(self.makeJob, resources)

	def clearData(self):
		self.payload = {}
		self.propertiesList = []


runMe = makePost()



if __name__ == '__main__':
	start_time = time.time()
	runMe.getInfo()
	runMe.printInfo()
	duration = time.time() - start_time
	print(f'For {len(runMe.listNoErrors)} POST requests it took {duration} seconds for gathering all the resrouces properties')
