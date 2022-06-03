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
		output = {
			'_time': time.time()
			}
		for attr, value in self._metadata.searchinfo.__dict__.items():
			output[attr] = value
		yield output

dispatch(RESTPostCommand, sys.argv, sys.stdin, sys.stdout, __name__)
