
import asyncio
import websockets
import json 
import os
import re
import ticker
import elasticsearch
import orderbook
import os, time, datetime, sys, json, hashlib, zlib, base64, json, re, elasticsearch, argparse, uuid, pytz
TIMEZONE = pytz.timezone('UTC')

class Orderbook: 
	def __init__(self): 
		self.orderbookMapping = {
			"okcoin": {
				"properties": {
					"currency_pair": { "type": "string"},
					"uuid": { "type": "string", "index": "no"},
					"date": {"type": "date"},
					"price": {"type": "float"},
					"count": {"type": "float"},
					"volume": {"type" : "float"},
					"absolute_volume": { "type": "float"},
					"order_type": { "type": "string"}, 
					"websocket_name": { "type": "string" }, 
					"depth": { "type": "string" }, 
					"is_future": {"type": "boolean"} 
				}
			}
		}


	def getEntry(self, entry, entryType, currencyPair, timestamp): 
		dto = {}
		if len(entry) == 2:
			dto["uuid"] = str(uuid.uuid4())
			dto["date"] = datetime.datetime.now(TIMEZONE)
			dto["currency_pair"] = str(currencyPair)
			dto["timestamp"] = str(timestamp)
			dto["price"] = float(entry[0])
			volumeVal = float(entry[1])
			dto["volume"] = float(volumeVal)
			dto["absolute_volume"] = float(volumeVal)
			dto["order_type"] = entryType
			dto["count"] = float(1)
		return dto 

	def getDepthDtoList(self, dataSet, currencyPair, isFuture):
		dtoList = []
		if "data" in dataSet: 
			timestamp = dataSet["data"]["timestamp"]
			for bidEntry in dataSet["data"]["bids"]: 
				curDto = self.getEntry(bidEntry, "BID", currencyPair, timestamp)
				dtoList.append(curDto) 
				curDto["is_future"] = isFuture
			for askEntry in dataSet["data"]["asks"]: 
				curDto = self.getEntry(askEntry, "ASK", currencyPair, timestamp) 
				curDto["is_future"] = isFuture
				dtoList.append(curDto) 
		return dtoList