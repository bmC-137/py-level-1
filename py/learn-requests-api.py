import string
import random
import requests
import multiprocessing
import datetime
import argparse
# from pprint import pprint
import re
import json

'''
	run with random generated properties
	python post.py  

	run with defaultValue properties
	python post.py --with-defaults
'''

base_url = 'https://api.example.com/dev/index.php'
empty = ''


def genDate():
	sdate = datetime.date(1753, 1, 1)
	edate = datetime.date(2020, 1, 1)
	time_between_dates = edate - sdate
	days_between_dates = time_between_dates.days
	random_number_of_days = random.randrange(days_between_dates)
	random_date = sdate + datetime.timedelta(days=random_number_of_days)
	return random_date


def genString(size):
	strPool = [x for x in string.ascii_uppercase + string.ascii_lowercase]
	m = toInt(size)
	s = []
	for i in range(m):
		y = random.randint(0, len(strPool) - 1)
		s.append(strPool[y])
	return ''.join(s)


def genIntStr(max_):
	random_string = ''.join([random.choice(string.ascii_lowercase + string.ascii_uppercase) for n in range(max_)])
	return random_string


def genFloat(min_, max_):
	b = random.randint(min_, max_)
	r = random.randint(0, 99) / 100
	return b + r


def genInt(min_, max_):
	random_int = int(random.randint(min_, max_))
	return random_int


def toInt(val):
	try:
		v = int(val)
		return v
	except (ValueError, TypeError) as e:
		print('error in toInt: ', e)
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
	result_ = dict()
	for param in parameters:
		if 'defaultValue' in param:
			result[param['name']] = param['defaultValue']
	for key in result.keys():
		result[key] = result[key].replace('\n', '')
		result[key] = re.sub('[ \' ]', '', result[key])
		result_ = json.loads(result[key])
	return result_


def data_gen(type_, min_, max_):
	# global val_
	min_ = int(min_)
	max_ = int(max_)
	try:
		if 'empty_string' in type_:
			val_ = empty
		elif type_ == 'int':
			val_ = genInt(min_, max_)
		elif type_ == 'string' or type_ == 'string|int' or type_ == 'Array' or type_ == 'array|string':
			val_ = genString(max_)
		elif type_ == 'float':
			val_ = genFloat(min_, max_)
		elif type_ == 'boolean':
			tORf = ['True', 'False']
			val_ = random.choice(tORf)
		elif type_ == 'date':
			val_ = genDate()
		elif type_:
			print('Type: ', type_, 'is not set. Generating random string, if max not set is 5')
			val_ = genString(max_)
		else:
			pass
	except (ValueError, UnboundLocalError) as e:
		print('Error in data_gen function: ', e)
		pass
	return val_


def makePostReq(url, payload, addr):
	def func1(u_, p_):
		r = requests.post(u_, json=p_)
		print(r.text)
	try:
		if url and payload:
			u = url
			p = payload
			func1(u, p)
	except:
		print('Error in makePostReq: ', addr)
		pass


class makePost:
	def __init__(self):
		manager = multiprocessing.Manager()
		self.l1 = manager.list([])
		self.l2 = manager.list([])
		self.payload = {}
		self.propertiesList = []
		self.allowValues = []
		self.newPayload = {}
		self.uniq_values = []

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
			self.uniqValues()

	def makeJob(self, resource):
		apis = requests.get(base_url + resource['path']).json()['apis']
		namespace_arg = vars(defaults)
		for api in apis:
			post_url = base_url + api['path']
			post_element = post_url.split('/')
			url_description = base_url + '/resources/' + post_element[6]
			for operation in api['operations']:
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
						get_dataType = requests.get(url_description).json()['models'][dataType]
						self.propertiesList = []
						for prop in get_dataType['properties']:
							self.propertiesList.append(prop)
						self.payload = {prop: empty for prop in self.propertiesList}

						self.cleanUniqValues()
						self.l1.append(post_element[6])
						self.findValues(post_element[6])
						if namespace_arg['with_defaults'] == 42:
							try:
								# default_values = dict()
								default_values = extract_default_values(operation['parameters'])
								self.newPayload = default_values
							except KeyError as e:
								print('default_values KeyError', e)
						else:
							for k in self.payload:
								element = post_element[6]
								url_gen = \
									requests.get(base_url + '/resources' + '/' + element).json()['models'][dataType][
										'properties'][k]
								min_ = 1
								max_ = 5
								type_ = empty
								try:
									type_ = url_gen['type']
									max_ = url_gen['maximum']
									min_ = url_gen['minimum']
									# if url_gen['type'] == 'Array' or \
									# 		url_gen['type'] == 'boolean' or \
									# 		url_gen['type'] == 'Parameter' or \
									# 		url_gen['type'] == 'ApprovalMsg' or \
									# 		url_gen['type'] == 'ReminderMsg' or \
									# 		url_gen['type'] == 'UpdateQRMsg':
									# 	continue
									try:
										setDescription = url_gen['description']
										if '@max 10' in url_gen['description']:
											max_ = 10
										searchDate = "date"
										if searchDate.lower() in setDescription.lower():
											type_ = searchDate
									except:
										pass
								except:
									pass
								pp = data_gen(type_, min_, max_)
								self.newPayload[k] = pp
								if 'actionType' in k or 'action' in k:
									self.newPayload[k] = empty
						if len(self.uniq_values) == 0:
							url_ = base_url + api['path']
							makePostReq(url_, self.newPayload, api['path'])
						else:
							for u_ in self.uniq_values:
								url_ = base_url + api['path'].format(type=u_)
								print(url_)
								makePostReq(url_, self.newPayload, api['path'])
						print('request.POST to: ' + base_url + api['path'] + ': ')
						print('URL parameters:' + url_description)
					except (KeyError, ValueError) as e:
						self.l2.append(post_element[6])
						print('Error in ', post_element[6], e)
						pass
					print('\n')

	def getInfo(self):
		resources = requests.get(base_url + '/resources').json()['apis']
		with multiprocessing.Pool() as pool:
			pool.map(self.makeJob, resources)

	def printInfo(self):
		print('POSTed: ', self.l1, end='\n')
		print('Errors: ', self.l2)

	def clearData(self):
		self.payload = {}
		self.propertiesList = []


runMe = makePost()

if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument('--with-defaults', action='store_const', required=False, const=42, default='')
	defaults = ap.parse_args()
	start_time = datetime.datetime.now()
	runMe.getInfo()
	duration = datetime.datetime.now() - start_time
	print(f'For {len(runMe.l1)} POST requests it took {duration} seconds for gathering all the resrouces properties')
	runMe.printInfo()
