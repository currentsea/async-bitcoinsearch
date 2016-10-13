# trades.py placeholder

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

class Trade: 

	def __init__(self): 
		self.completedTradeMapping = {
			"completed_trades": {
				"properties": {
					"uuid": { "type": "string", "index": "no" },
					"date" : { "type": "date" },
					"sequence_id": { "type" : "string", "index":"no"},
					"order_id":{  "type" : "string", "index":"no"},
					"price": {"type": "float"},
					"volume": {"type": "float"},
					"order_type" : { "type": "string"},
					"absolute_volume" : {"type":"float"},
					"currency_pair": {"type":"string"},
					"timestamp": { "type": "string", "index": "no"}, 
					"websocket_name": { "type": "string" }, 
					"is_future": { "type": "string" } 
				}
			}
		}

	def getCompletedTradeDtoList(self, dataSet, currencyPair):
		dtoList = []
		print (dataSet) 
		# for completedTrade in dataSet:
		# 	dto = {}
		# 	dto["order_id"] = str(completedTrade[0])
		# 	dto["price"] = float(completedTrade[1])
		# 	dto["uuid"] = str(uuid.uuid4())
		# 	dto["date"] = datetime.datetime.now(TIMEZONE)
		# 	dto["currency_pair"] = str(currencyPair)
		# 	absVol = float(completedTrade[2])
		# 	dto["absolute_volume"] = float(absVol)
		# 	timestamp = str(completedTrade[3])
		# 	orderType = str(completedTrade[4])
		# 	orderType = orderType.upper()
		# 	dto["order_type"] = orderType
		# 	if orderType == "BID":
		# 		volumeVal = absVol * -1
		# 		dto["volume"] = float(volumeVal)
		# 	elif orderType == "ASK":
		# 		volumeVal = absVol
		# 		dto["volume"] = float(volumeVal)
		# 	else:
		# 		raise IOError("Order type is not ask or bid for completed trade (wtf?)")
		# 	dto["timestamp"] = str(timestamp)
		# 	dto["is_future"] = isFuture
		# 	dto["websocket_name"] = str(channel)
		# 	dtoList.append(dto)
		return dtoList		