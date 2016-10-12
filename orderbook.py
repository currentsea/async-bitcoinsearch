
class Orderbook: 
	def __init__(self): 
		self.orderbookMapping = {
			"okcoin": {
				"properties": {
					"currency_pair": { "type": "string"},
					"uuid": { "type": "string", "index": "no"},
					"date": {"type": "date"},
					"price": {"type": "float"},
					"count": {"type": "float"},
					"volume": {"type" : "float"},
					"absolute_volume": { "type": "float"},
					"order_type": { "type": "string"}, 
					"websocket_name": { "type": "string" }, 
					"depth": { "type": "string" }
				}
			}
		}


	def getDepthDtoList(self, dataSet, currencyPair):
		dtoList = []
		print ("------")
		for bid in dataSet["bids"]:
			dto = {}
			if len(bid) == 2:
				dto["uuid"] = str(uuid.uuid4())
				dto["date"] = datetime.datetime.now(TIMEZONE)
				dto["currency_pair"] = str(currencyPair)
				dto["timestamp"] = str(dataSet["timestamp"])
				dto["price"] = float(bid[0])
				volumeVal = float(bid[1])
				dto["volume"] = float(volumeVal)
				dto["absolute_volume"] = float(volumeVal)
				dto["order_type"] = "BID"
				dto["count"] = float(1)
				dtoList.append(dto)
		for ask in dataSet["asks"]:
			dto = {}
			if len(ask) == 2:
				dto["uuid"] = str(uuid.uuid4())
				dto["date"] = datetime.datetime.now(TIMEZONE)
				dto["currency_pair"] = str(currencyPair)
				dto["timestamp"] = str(dataSet["timestamp"])
				dto["price"] = float(ask[0])
				volumeVal = float(ask[1])
				volumeVal = volumeVal * -1
				dto["volume"] = float()
				dto["absolute_volume"] = float(volumeVal)
				dto["order_type"] = "ASK"
				dto["count"] = float(1)
				dtoList.append(dto)
		print ("------")
		return dtoList