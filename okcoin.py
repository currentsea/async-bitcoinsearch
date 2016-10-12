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
OKCOIN_WEBSOCKETS_URL= "wss://real.okcoin.com:10440/websocket/okcoinapi"

class OkCoinSocket: 

	## Possible "To Do" - replace params with **kwargs
	def __init__(self, esHost): 
		pass 

	@asyncio.coroutine
	async def processMarketData(self, channelSubscriptions): 
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
						await self.consumer(message)
					except TypeError:
						pass

	def getChannelDict(self): 
		channelDict = []
		with open("channels.txt") as channels: 
			for line in channels: 
				channelDict.append(line.strip()) 
		return channelDict

	def consumer(self, marketData): 
		jsonData = json.loads(marketData) 
		print (jsonData)

	def initialize(self): 
		channels = self.getChannelDict()
		asyncio.get_event_loop().run_until_complete(self.processMarketData(channels)) 	

# async def processor():
# 	async with websockets.connect(OKCOIN_WEBSOCKETS_URL) as websocket:
# 		substr = "{'event':'addChannel','channel':'ok_sub_spotusd_btc_ticker'}"
# 		await websocket.send(substr)

# 		greeting = await websocket.recv()]
if __name__ == "__main__":
	socket = OkCoinSocket("http://localhost:9200") 
	socket.initialize() 
	# print (dictShit) 
