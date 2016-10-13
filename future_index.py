# for the future index price feed from the websocket API for okcoin 

import asyncio
import websockets
import json 
import os
import re
import ticker
import elasticsearch
import os, time, datetime, sys, json, hashlib, zlib, base64, json, re, elasticsearch, argparse, uuid, pytz
TIMEZONE = pytz.timezone('UTC')

class FutureIndex(): 
	def __init__(self): 
		self.futurePriceIndexMapping = { 
			"future_price_index": { 
				"properties": { 
					"currency_pair": { "type": "string" }, 
					"uuid": { "type": "string", "index": "no"},
					"date": { "type": "date" }, 
					"timestamp": { "type": "string", "index": "no"}, 
					"websocket_name": { "type": "string" }, 
					"price": { "type": "float" }
				}	
			}	
		}

	def getFutureIndexDto(self, dataSet, currencyPair): 
		dto = {}
		if "data" in dataSet: 
			uniqueId = uuid.uuid4()
			dto["currency_pair"] = currencyPair 
			dto["uuid"] = str(uniqueId)
			recordDate = datetime.datetime.now(TIMEZONE)
			dto["date"] = recordDate
			futureIndexPrice = float(dataSet["data"]["futureIndex"])
			futureIndexTimestamp = str(dataSet["data"]["timestamp"]) 
			dto["websocket_name"] = str(dataSet["channel"]) 
			dto["timestamp"] = str(futureIndexTimestamp) 
			dto["price"] = futureIndexPrice
		return dto 