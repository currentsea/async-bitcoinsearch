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
	channels  = ["ok_sub_spotusd_btc_ticker", "ok_sub_spotusd_ltc_ticker", "ok_sub_spotusd_btc_depth_20", "ok_sub_spotusd_ltc_depth_20", "ok_sub_spotusd_btc_depth_60", "ok_sub_spotusd_ltc_depth_60", "ok_sub_spotusd_btc_trades", "ok_sub_spotusd_ltc_trades", "ok_sub_spotusd_btc_kline_1min", "ok_sub_spotusd_btc_kline_3min", "ok_sub_spotusd_btc_kline_5min", "ok_sub_spotusd_btc_kline_15min", "ok_sub_spotusd_btc_kline_30min", "ok_sub_spotusd_btc_kline_1hour", "ok_sub_spotusd_btc_kline_2hour", "ok_sub_spotusd_btc_kline_4hour", "ok_sub_spotusd_btc_kline_6hour", "ok_sub_spotusd_btc_kline_12hour", "ok_sub_spotusd_btc_kline_day", "ok_sub_spotusd_btc_kline_3day", "ok_sub_spotusd_btc_kline_week", "ok_sub_spotusd_ltc_kline_1min", "ok_sub_spotusd_ltc_kline_3min", "ok_sub_spotusd_ltc_kline_5min", "ok_sub_spotusd_ltc_kline_15min", "ok_sub_spotusd_ltc_kline_30min", "ok_sub_spotusd_ltc_kline_1hour", "ok_sub_spotusd_ltc_kline_2hour", "ok_sub_spotusd_ltc_kline_4hour", "ok_sub_spotusd_ltc_kline_6hour", "ok_sub_spotusd_ltc_kline_12hour", "ok_sub_spotusd_ltc_kline_day", "ok_sub_spotusd_ltc_kline_3day", "ok_sub_spotusd_ltc_kline_week", "ok_sub_futureusd_btc_ticker_this_week","ok_sub_futureusd_btc_ticker_next_week", "ok_sub_futureusd_btc_ticker_quarter", "ok_sub_futureusd_ltc_ticker_this_week", "ok_sub_futureusd_ltc_ticker_next_week", "ok_sub_futureusd_ltc_ticker_quarter"]
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
