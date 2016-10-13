# kline candle placeholder class
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

class KlineCandle: 
	def __init__(self): 
		self.klineMapping = {
			"kline_candles": {
				"properties": {
					"uuid": { "type": "string", "index": "no"},
					"date": {"type": "date"},
					"timestamp": {"type": "string", "index": "no"},
					"open_price": {"type": "float"},
					"highest_price": {"type": "float"},
					"lowest_price": {"type": "float"},
					"close_price": {"type": "float"},
					"volume": {"type": "float"},
					"currency_pair": {"type": "string"},
					"contract_type": {"type": "string"}, 
					"websocket_name": { "type": "string" },
					"exchange": { "type": "string" }, 
					"candle_type": { "type": "string" }, 
					"is_future": { "type": "string" } 
				}
			}
		}

	def getKlineDto(self, dataSet, currencyPair, channel): 
		dto = {}
		uniqueId = uuid.uuid4()
		dto["uuid"] = str(uniqueId)
		recordDate = datetime.datetime.now(TIMEZONE)
		dto["date"] = recordDate
		dto["currency_pair"] = str(currencyPair) 
		try:
			if "spotusd" in channel: 
				futureRegex = re.search("ok_sub_spotusd_(b|l)tc_kline_(.+)", channel)
				candleType = futureRegex.group(2)
				dto["candle_type"] = str(candleType)
				dto["contract_type"] = "spotusd" 
			elif "futureusd" in channel: 
				futureRegex = re.search("ok_sub_futureusd_(b|l)tc_kline_(this_week|next_week|quarter)_([0-9a-z])")
				candleType = futureRegex.group(3)
				contractType = futureRegex.group(2) 
				dto["contract_type"] = contractType
				dto["candle_type"] = candleType
			dto["timestamp"] = str(dataSet[0])
			dto["open_price"] = float(dataSet[1])
			dto["highest_price"] = float(dataSet[2])
			dto["lowest_price"] = float(dataSet[3])
			dto["close_price"] = float(dataSet[4])
			theVol = str(dataSet[5])
			theVol = theVol.replace(",", "")
			theVolFloat = float(theVol)
			dto["volume"] = float(theVolFloat)
		except:
			raise
		return dto 