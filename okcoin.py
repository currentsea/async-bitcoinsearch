#!/usr/bin/env python

import asyncio
import websockets
import json 
OKCOIN_WEBSOCKETS_URL= "wss://real.okcoin.com:10440/websocket/okcoinapi"

class OkCoinSocket: 
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

	def getChannelDict(): 
		channelDict = []
		with open("channels.txt") as channels: 
			for line in channels: 
				channelDict.append(line.strip()) 
		return channelDict

	def consumer(marketData): 
		jsonData = json.loads(marketData) 
		print (jsonData)


# async def processor():
# 	async with websockets.connect(OKCOIN_WEBSOCKETS_URL) as websocket:
# 		substr = "{'event':'addChannel','channel':'ok_sub_spotusd_btc_ticker'}"
# 		await websocket.send(substr)

# 		greeting = await websocket.recv()]
if __name__ == "__main__":
	channels = getChannelDict()
	# print (dictShit) 
	asyncio.get_event_loop().run_until_complete(processMarketData(channels)) 	
