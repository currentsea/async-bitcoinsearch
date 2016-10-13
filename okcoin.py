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
import sys 
import elasticsearch
import time 
import datetime 
import hashlib, zlib, base64, json, re, elasticsearch, argparse, uuid, pytz

from trades import Trade
from ticker import Ticker
from orderbook import Orderbook
from kline import KlineCandle
from future_index import FutureIndex

OKCOIN_WEBSOCKETS_URL= "wss://real.okcoin.com:10440/websocket/okcoinapi"
DEFAULT_INDEX = "currentsea" 
CHANNEL_FILE = "channels.txt" 
TIMEZONE = pytz.timezone('UTC')

class OkCoinSocket: 

	## Possible "To Do" - replace params with **kwargs
	def __init__(self, esHost): 
		self.esHost = esHost
		self.active = False 
		self.count = 0

	@asyncio.coroutine
	async def processMarketData(self, channelSubscriptions): 
		async with websockets.connect(OKCOIN_WEBSOCKETS_URL) as websocket:
			try: 
				for subscription in channelSubscriptions: 
					await websocket.send("{'event':'addChannel','channel':'" + subscription + "'}") 
				greeting = await websocket.recv()
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
		self.docMappings(connection) 
		dataSet = json.loads(marketData) 
		item = {}
		for infoPoint in dataSet: 
			try: 
				channel = str(infoPoint["channel"])
				regex = "ok_sub_(spotusd|futureusd)_(b|l)tc_(.[A-Za-z0-9_]+)"
				search = re.search(regex, channel) 
				if search.group(1) == "futureusd": 
					isFuture = True
				else: 
					isFuture = False 
				currencyPair = str(search.group(2)) + "tc_usd"
				self.count = self.count + 1
				if self.count % 100 == 0: 
					print ("PROCESSED " + str(self.count) + " DATA POINTS SO FAR...") 
				if search.group(3) == "index": 
					myindex = FutureIndex()
					dto = myindex.getFutureIndexDto(infoPoint, currencyPair)
					dto["exchange"] = "OKCOIN"
					self.postDto(dto, connection, "future_price_index")
				elif "depth" in channel: 
					mybook = Orderbook()
					dto = mybook.getDepthDtoList(infoPoint, currencyPair, isFuture)
					for item in dto: 
						item["websocket_name"] = channel
						item["is_future"] = isFuture
						if isFuture == True: 
							check = re.search("depth_(this_week|next_week|quarter)_(20|60)", search.group(3).strip())
							item["contract_type"] = str(check.group(1))
							item["depth"] = str(check.group(2))
						else: 
							item["contract_type"] = "spot"
							depthSearch = re.search("depth_(20|60)", search.group(3).strip()) 
							item["depth"] = depthSearch.group(1) 
						item["exchange"] = "OKCOIN"	
						self.postDto(item, connection, "orderbook")
				elif "ticker" in channel and "data" in infoPoint: 
					myticker = Ticker() 
					if isFuture == False: 
						dto = myticker.getTickerDto(infoPoint, currencyPair) 
						self.postDto(dto, connection, "ticker")
					elif isFuture == True: 
						dto = myticker.getFutureTickerDto(infoPoint, channel, currencyPair)
						dto["exchange"] = "OKCOIN"
						self.postDto(dto, connection, "future_ticker") 
				elif "trades" in channel: 
					mytrade = Trade() 
					if "data" in infoPoint: 
						dtoList = mytrade.getCompletedTradeDtoList(infoPoint["data"], currencyPair)
						for item in dtoList: 
							item["is_future"] = "futureusd" in channel
							item["websocket_name"] = channel 	
							item["exchange"] = "OKCOIN" 	
							self.postDto(item, connection, "completed_trades") 
				elif "kline" in channel: 
					myklein = KlineCandle() 
					if "data" in infoPoint: 
						if len(infoPoint["data"]) > 1: 
							for klineData in infoPoint["data"]: 
								if type(klineData) is list: 
									klineDto = myklein.getKlineDto(klineData, currencyPair, channel) 
									klineDto["exchange"] = "OKCOIN" 
									klineDto["is_future"] = isFuture 
									klineDto["websocket_name"] = channel
								else: 
									klineDto = myklein.getKlineDto(infoPoint["data"], currencyPair, channel) 
							self.postDto(klineDto, connection, "kline_candles")
			except: 
				raise

	# Ensures the most up to date mappings and such are set in elasticsearch 
	def ensure(self, connection):
		if connection.indices.exists("currentsea") == False: 
			try:
				connection.indices.create("currentsea") 
			except elasticsearch.exceptions.RequestError as e:
				print ("INDEX " + DEFAULT_INDEX + " ALREADY EXISTS")
				self.active = True 
			except:
				pass
		pass 

	def docMappings(self, connection, indexName=DEFAULT_INDEX): 
		try: 
			connection.indices.put_mapping(index=indexName, doc_type="orderbook", body=Orderbook().orderbookMapping)
			connection.indices.put_mapping(index=indexName, doc_type="ticker", body=Ticker().tickerMapping)
			connection.indices.put_mapping(index=indexName, doc_type="completed_trades", body=Trade().completedTradeMapping)
			connection.indices.put_mapping(index=indexName, doc_type="future_ticker", body=Ticker().futureTickerMapping)
			connection.indices.put_mapping(index=indexName, doc_type="future_price_index", body=FutureIndex().futurePriceIndexMapping) 
			connection.indices.put_mapping(index=indexName, doc_type="kline_candles", body=KlineCandle().klineMapping) 
		except: 
			raise 
		pass

	def capture(self, knowledge, channelName, indexName=DEFAULT_INDEX): 
		newDocUploadRequest = self.es.create(index=indexName, doc_type=channelName, ignore=[400], id=uuid.uuid4(), body=dto)
		return newDocUploadRequest["created"]

	def initialize(self): 
		channels = self.getChannelDict()
		return asyncio.get_event_loop().run_until_complete(self.processMarketData(channels)) 	
	
	def postDto(self, dto, conn, docType="orderbook", indexName="currentsea"):
		newDocUploadRequest = conn.create(index=indexName, doc_type=docType, ignore=[400], id=uuid.uuid4(), body=dto)
		return newDocUploadRequest["created"]

if __name__ == "__main__":
	try: 
		esHost = sys.argv[1]
	except: 
		esHost = "http://localhost:9200"  
		socket = OkCoinSocket(esHost) 
	socket.initialize() 
