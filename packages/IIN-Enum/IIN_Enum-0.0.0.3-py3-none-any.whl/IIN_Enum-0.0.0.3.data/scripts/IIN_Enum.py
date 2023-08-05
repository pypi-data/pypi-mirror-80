import sys
import os
import requests


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0 Safari/537.36'}


def pull_data(bin_num):
	try:
		req = requests.get("https://lookup.binlist.net/{}".format(bin_num))
		try:
			req = req.json()
		except:
			return 'Invalid IIN Number'
		return req
	except KeyboardInterrupt:
		sys.exit(1)
		
		
def format_data(req, bin_num):
	try:
		s_0 = "\nIssuer Identification Number: {}".format(bin_num)
		try:
			s_1 = "\nCard Type: {}".format(req['type'] + ' ' + req['scheme'])
		except:
			s_1 = "\nCard Type: N/A"
		try:
			s_2 = "\nBank: {}".format(req['bank']['name'])
		except:
			s_2 = "\nBank: N/A"
		try:
			s_3 = "\nOrigin: {}".format(req['country']['alpha2'] + ', ' + req['country']['currency'])
		except:
			s_3 = "\nOrigin: N/A"
		data = s_0+s_1+s_2+s_3
		return data
	except KeyboardInterrupt:
		sys.exit(1)


def IIN_Enum(iin_num):
	try:
		req = pull_data(iin_num)
		if req == 'Invalid IIN Number':
			return '\nInvalid IIN Number'
		else:
			data = format_data(req, iin_num)
			return data
	except KeyboardInterrupt:
		sys.exit(1)

