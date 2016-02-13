#!/usr/bin/python
# coding: utf-8

from textteaser import TextTeaser
from alchemyapi import AlchemyAPI
import json

alchemyapi = AlchemyAPI()

tt = TextTeaser()


def ifNeedTitle(input): 
  init = alchemyapi.keywords('text', input, {'sentiment': 1})
  return init['keywords'][0]['text']

def articleSummary(title, text):
  sentences = tt.summarize(title, text)
  return sentences

def groupSummary(text):
  title = ifNeedTitle(text)
  sentences = tt.summarize(title, text)
  return sentences

def sent(str):
  init = alchemyapi.sentiment('text', str)
  return init['docSentiment']['score']

def sentimenter(str):
  return [str, sent(str)]

def sentimentize(list):
  return map(sentimenter, list)

def removeNonAscii(list): 
  return map(lambda s: "".join(filter(lambda x: ord(x)<128, s)), list)