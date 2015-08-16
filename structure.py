#!/usr/bin/python
import configparser
import os

BASE_PATH = "./"
SCHEMA_PATH = os.path.join(BASE_PATH, "schema/")

"""
"""
class AgreementSchema(object):
	"""
	"""
	def __init__(self):
		pass

	"""	
	Loads schema information from schema/*.ini. 
	"""
	def load_schema(self, schema_type):
		config = configparser.ConfigParser()
		config.read(SCHEMA_PATH + schema_type)
		sections = config.sections()
		self.version = config['general']['version']
		self.agreement_type = config['general']['agreement_type']
		self.provisions = config.items('provisions')
		self.concepts = config.items('concepts')

	"""
	Returns a list of tuples which contain (name, path_to_training_file).  The 
	name corresponds to the name of a provision.  The path_to_training_file is
	a used for bootstrapping the provision classifier.  	
	"""
	def get_provisions(self):
		return self.provisions

	"""	
	Returns a list of tuples which correspond to the concepts expected in this 
	agreement type.  Tuples contain information in form of (provision_source, 
	concepts).  'concepts might be a comma-delimited string.'
	"""
	def get_concepts(self):
		return self.concepts

	"""	
	Returns the version of the schema being used.
	"""
	def get_version(self):
		return self.version

	"""	
	Returns a string corresponding to the agreement_type.
	"""
	def get_agreement_type(self):
		return self.agreement_type

"""
init loads schema definitions into files.
"""
def init(): 
	# ##################################
	# Create the convertible debt schema
	config = configparser.ConfigParser()
	config['general'] = {
		'agreement_type': 'convertible_debt',
		'version': '1.0',
	}

	config['provisions'] = {
		'recitals': 'train/train_recitals',
		'severability': 'train/train_severability',
		'interest_rate': 'train/train_interest_rate',
		'principal_amount': 'train/train_principal_amount',
		'notices': 'train/train_notices_and_notifications',
		'registration_rights': 'train/train_registration_rights',
	}

	config['concepts'] = {
		'interest_rate'	: 'interest_rate',
		'recitals' : 'interest_rate, maturity_date',
		'intro' : 'party, counterparty',
	}

	with open(SCHEMA_PATH + 'convertible_debt.ini', 'w') as configfile:
		config.write(configfile)
	# ##################################

def main():
	pass

"""
Bypass main() function when loading module.
"""
if __name__ == "__main__":
    pass