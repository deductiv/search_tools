#!/usr/bin/env python

# Appends the search metadata to each row of the events

# Author: J.R. Murray <jr.murray@deductiv.net>
# Version: 1.0.0

import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lib'))
from splunklib.searchcommands import \
	dispatch, StreamingCommand, Configuration, Option

@Configuration()
class AddSearchInfoCommand(StreamingCommand):
	
	def stream(self, events):
		for event in events:
			for attr, value in self._metadata.searchinfo.__dict__.items():
				event[attr] = value
			yield event

dispatch(AddSearchInfoCommand, sys.argv, sys.stdin, sys.stdout, __name__)
