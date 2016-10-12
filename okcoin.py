#!/usr/bin/env python3
# MIT License

# Copyright (c) 2016 currentsea (https://keybase.io/currentsea)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import asyncio
import websockets
import json 
import os
import re
import ticker
import elasticsearch
import orderbook
import os, time, datetime, sys, json, hashlib, zlib, base64, json, re, elasticsearch, argparse, uuid, pytz

OKCOIN_WEBSOCKETS_URL= "wss://real.okcoin.com:10440/websocket/okcoinapi"
DEFAULT_INDEX = "currentsea" 
CHANNEL_FILE = "channels.txt" 

class OkCoinSocket: 

	## Possible "To Do" - replace params with **kwargs
	def __init__(self, esHost): 
		self.esHost = esHost
		self.active = False 

	@asyncio.coroutine
	async def processMarketData(self, channelSubscriptions): 
		async with websockets.connect(OKCOIN_WEBSOCKETS_URL) as websocket:
			try: 
				for subscription in channelSubscriptions: 
					await websocket.send("{'event':'addChannel','channel':'" + subscription + "'}") 
				greeting = await websocket.recv()
				print (greeting) 
			finally: 
				while True:
					try:
						message = await websocket.recv()
						await self.consumer(message)
					except TypeError:
						pass

	def getChannelDict(self): 
		channelDict = []
		with open(CHANNEL_FILE) as channels: 
			for line in channels: 
				channelDict.append(line.strip()) 
		return channelDict

	def consumer(self, marketData): 
		connection = elasticsearch.Elasticsearch(self.esHost)
		self.ensure(connection) 
		dataSet = json.loads(marketData) 
		item = {}
		for infoPoint in dataSet: 
			try: 
				channel = str(infoPoint["channel"])
				# ticker|depth|trades|kline|ticker|index
				regex = "ok_sub_(spotusd|futureusd)_(b|l)tc_(.[A-Za-z0-9]+)"
				search = re.search(regex, channel) 
				print (infoPoint)
			except: 
				raise
	# Ensures the most up to date mappings and such are set in elasticsearch 
	def ensure(self, connection):
		if self.active == True: 
			try:
				connection.indices.create("currentsea") 
			except elasticsearch.exceptions.RequestError as e:
				print ("INDEX " + DEFAULT_INDEX + " ALREADY EXISTS")
				self.active = True 
			except:
				pass
		pass 

	def docMappings(self): 
		return self.es.indices.put_mapping(index=DEAFULT_INDEX, doc_type="orderbook", body=orderbook.orderbookMapping)

	def capture(self, knowledge, channelName, indexName=DEFAULT_INDEX): 
		newDocUploadRequest = self.es.create(index=indexName, doc_type=channelName, ignore=[400], id=uuid.uuid4(), body=dto)
		return newDocUploadRequest["created"]

	def initialize(self): 
		channels = self.getChannelDict()
		return asyncio.get_event_loop().run_until_complete(self.processMarketData(channels)) 	

if __name__ == "__main__":
	try: 
		esHost = sys.argv[1]
	except: 
		esHost = "http://localhost:9200" 
		socket = OkCoinSocket(esHost) 
	socket.initialize() 
