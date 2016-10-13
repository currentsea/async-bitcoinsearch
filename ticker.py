
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

class Ticker:

	def __init__(self): 
		self.tickerMapping = {
			"ticker": {
				"properties": {
					"uuid": { "type": "string", "index": "no"},
					"date": {"type": "date"},
					"last_price": {"type": "float"},
					"timestamp": {"type": "string", "index": "no"},
					"volume": {"type": "float"},
					"high": {"type": "float"},
					"ask": {"type": "float"},
					"low": {"type": "float"},
					"daily_change": {"type": "float"},
					"daily_delta": {"type" : "float"},
					"ask_volume": {"type": "float"},
					"bid_volume": {"type": "float"},
					"bid": {"type": "float"},
					"currency_pair": {"type":"string"}, 
					"websocket_name": { "type": "string" }, 
					"is_future" : { "type": "string"}, 
					"exchange": { "type": "string"}
				}
			}
		}
		self.futureTickerMapping = {
			"future_ticker" : {
				"properties": {
					"uuid": { "type": "string", "index": "no"},
					"date": {"type": "date"},
					"timestamp": {"type": "string", "index": "no"},
					"buy_price": {"type": "float"},
					"high_price": {"type": "float"},
					"last_price": {"type": "float"},
					"low_price": {"type": "float"},
					"sell_price": {"type": "float"},
					"unit_amount": {"type": "float"},
					"volume": {"type": "float"},
					"contract_type": {"type": "string"},
					"contract_id": {"type": "string", "index": "no"},
					"currency_pair": {"type": "string"}, 
					"exchange": { "type": "string" } 
				}
			}
		}

	def getFutureTickerDto(self, data, channelName, currencyPair):
		futureDto = {}
		uniqueId = uuid.uuid4()
		futureDto["uuid"] = str(uniqueId)
		recordDate = datetime.datetime.now(TIMEZONE)
		futureRegex = re.search("ok_sub_futureusd_(b|l)tc_ticker_(.+)", channelName)
		futureType = futureRegex.group(2)
		currencySymbol = futureRegex.group(1)
		futureDto["date"] = recordDate
		futureDto["buy_price"] = float(data["data"]["buy"])
		futureDto["contract_id"] = str(data["data"]["contractId"])
		futureDto["high_price"] = float(data["data"]["high"])
		futureDto["last_price"] = float(data["data"]["last"])
		futureDto["low_price"] = float(data["data"]["low"])
		futureDto["sell_price"] = float(data["data"]["sell"])
		futureDto["unit_amount"] = float(data["data"]["unitAmount"])
		futureDto["volume"] = float(data["data"]["vol"])
		futureDto["currency_pair"] = str(currencyPair)
		futureDto["contract_type"] = str(futureType)
		return futureDto

	def getTickerDto(self, dataSet, currencyPair):
		dto = {}
		if "data" in dataSet: 
			dto["uuid"] = str(uuid.uuid4())
			dto["date"] = datetime.datetime.now(TIMEZONE)
			dataObj = dataSet["data"] 

			dto["volume"] = float(str(dataObj["vol"].replace(",","")))
			dto["timestamp"] = str(dataSet["data"]["timestamp"])
			dto["last_price"] = float(dataSet["data"]["last"])
			dto["low_price"] = float(dataSet["data"]["low"])
			dto["ask"] = float(dataSet["data"]["sell"])
			dto["bid"] = float(dataSet["data"]["buy"])
			dto["high"] = float(dataSet["data"]["high"])
			dto["currency_pair"] = str(currencyPair)
		return dto
