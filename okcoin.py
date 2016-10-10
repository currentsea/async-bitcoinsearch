#!/usr/bin/env python

import asyncio
import websockets
import json 
OKCOIN_WEBSOCKETS_URL= "wss://real.okcoin.com:10440/websocket/okcoinapi"

@asyncio.coroutine
async def processMarketData(channelSubscriptions): 
	async with websockets.connect(OKCOIN_WEBSOCKETS_URL) as websocket:
		try: 
			for subscription in channelSubscriptions: 
				print ("subscription: " + subscription)
				await websocket.send("{'event':'addChannel','channel':'" + subscription + "'}") 
			greeting = await websocket.recv()
		finally: 
			while True:
				try:
					message = await websocket.recv()
					await consumer(message)
				except TypeError:
					pass

# def getTickerMapping(): 
# 	mapping = "okcoin_ticker": {
# 		"properties": {
# 			"uuid": { "type": "string", "index": "no"},
# 			"date": {"type": "date"},
# 			"last_price": {"type": "float"},
# 			"timestamp": {"type": "string", "index": "no"},
# 			"volume": {"type": "float"},
# 			"high": {"type": "float"},
# 			"ask": {"type": "float"},
# 			"low": {"type": "float"},
# 			"daily_change": {"type": "float"},
# 			"daily_delta": {"type" : "float"},
# 			"ask_volume": {"type": "float"},
# 			"bid_volume": {"type": "float"},
# 			"bid": {"type": "float"},
# 			"currency_pair": {"type":"string"}
# 		}
# 	}
# 	return mapping

def getChannelDict(): 
	channels  = ["ok_sub_spotusd_btc_ticker", "ok_sub_spotusd_ltc_ticker", "ok_sub_spotusd_btc_depth_20", "ok_sub_spotusd_ltc_depth_20", "ok_sub_spotusd_btc_depth_60", "ok_sub_spotusd_ltc_depth_60"]
	return channels

def consumer(marketData): 
	jsonData = json.loads(marketData) 
	print (jsonData)
	# print (list(marketData)) 
	# for blip in marketData: 
	# 	print (blip["channel"])
		# if blip["channel"] = "ok_sub_spotusd_ltc_ticker" 
	# print (message)
# async def processor():
# 	async with websockets.connect(OKCOIN_WEBSOCKETS_URL) as websocket:
# 		substr = "{'event':'addChannel','channel':'ok_sub_spotusd_btc_ticker'}"
# 		await websocket.send(substr)

# 		greeting = await websocket.recv()]
channels = getChannelDict()
# print (dictShit) 
asyncio.get_event_loop().run_until_complete(processMarketData(channels)) 	
