#!/usr/bin/env python

import asyncio
import websockets

OKCOIN_WEBSOCKETS_URL= "wss://real.okcoin.com:10440/websocket/okcoinapi"

@asyncio.coroutine
async def hello(): 
	async with websockets.connect(OKCOIN_WEBSOCKETS_URL) as websocket:
		try: 
			substr = "{'event':'addChannel','channel':'ok_sub_spotusd_btc_ticker'}"
			await websocket.send(substr)

			greeting = await websocket.recv()
			print(greeting)
			print ("connected to subscription")
		finally: 
			while True:
				try:
					message = await websocket.recv()
					await consumer(message)
				except TypeError:
					pass

def consumer(message): 
	print (message)
# async def processor():
# 	async with websockets.connect(OKCOIN_WEBSOCKETS_URL) as websocket:
# 		substr = "{'event':'addChannel','channel':'ok_sub_spotusd_btc_ticker'}"
# 		await websocket.send(substr)

# 		greeting = await websocket.recv()]

asyncio.get_event_loop().run_until_complete(hello()) 	
