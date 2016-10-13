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

class Kline: 
	def __init__(self): 
		self.klineMapping = {
			"okcoin": {
				"properties": {
					"uuid": { "type": "string", "index": "no"},
					"date": {"type": "date"},
					"timestamp": {"type": "string", "index": "no"},
					"open_price": {"type": "float"},
					"highest_price": {"type": "float"},
					"lowest_price": {"type": "float"},
					"close_price": {"type": "float"},
					"volume": {"type": "float"},
					"currency_symbol": {"type": "string"},
					"contract_type": {"type": "string"}
				}
			}
		}

	def getKlineDto(self): 
		