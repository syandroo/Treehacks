#!/usr/bin/python
# coding: utf-8

import re


def sanitize_text(text):
	# remove non-alphanumeric characters
	clean_text = re.sub("[^a-zA-Z0-9\s]", " ", text).lower()
	return clean_text