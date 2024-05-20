#!/usr/bin/env python

# Allows a POST to be sent to Splunk rest endpoints

# Author: J.R. Murray <jr.murray@deductiv.net>
# Version: 1.0.0

import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lib'))
from splunklib.searchcommands import \
	dispatch, GeneratingCommand, Configuration, Option

@Configuration()
class RESTPostCommand(GeneratingCommand):
	
	endpoint = Option(require=True)

	def generate(self):
		args = [val for val in self._metadata.searchinfo.args[2:] if '=' not in val]

		logger.debug("Arguments: " + str(self._metadata.searchinfo.args[2:]))
		arg_count = len(args)
		arg_index = 0

		# Parse the arguments to the command
		if arg_count >= 3:
			while arg_index < arg_count:
				# Process the lookup name, lookup field, search field
				if self.lookup == '':
					self.lookup = args[arg_index]
					arg_index += 1
				if self.lookupfield == '':
					self.lookupfield = args[arg_index]
					if len(args) >= arg_index + 2:
						if args[arg_index + 1].upper() == 'AS':
							self.searchfield = args[arg_index + 2]
							arg_index += 3
						else:
							self.searchfield = self.lookupfield
							arg_index += 1
					else:
						self.searchfield = self.lookupfield
						arg_index += 1
						
				if arg_index < len(args) and None not in [self.lookup, self.lookupfield, self.searchfield]:
					if args[arg_index].upper() == 'OUTPUT':
						self.output_overwrite = True
					elif args[arg_index].upper() == 'OUTPUTNEW':
						self.output_overwrite = False
					else:
						# Add field to output fields list
						output_field_name = args[arg_index].strip(',')
						if len(args) >= arg_index + 2:
							if args[arg_index + 1].upper() == 'AS':
								self.output_aliases[output_field_name] = args[arg_index + 2]
								arg_index += 2
							else:
								self.output_aliases[output_field_name] = output_field_name
						else:
							self.output_aliases[output_field_name] = output_field_name
					arg_index += 1
		else: 
			logger.critical("Not enough parameters specified to execute.")
			print("Not enough parameters specified to execute.")
			exit(1957)
		
		output = {
			'_time': time.time()
			}
		for attr, value in self._metadata.searchinfo.__dict__.items():
			output[attr] = value
		yield output

dispatch(RESTPostCommand, sys.argv, sys.stdin, sys.stdout, __name__)
