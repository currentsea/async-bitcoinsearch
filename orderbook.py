
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
					"websocket_name": { "type": "string" }
				}
			}
		}
