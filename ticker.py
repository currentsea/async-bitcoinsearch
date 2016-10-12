
class Ticker:

	def __init__(self): 
		self.tickerMapping = {
			"okcoin": {
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
					"currency_pair": {"type":"string"}
				}
			}
		}
		
	def getTickerDto(self, dataSet, currencyPair):
		dto = {}
		dto["uuid"] = str(uuid.uuid4())
		dto["date"] = datetime.datetime.now(TIMEZONE)
		dto["volume"] = float(str(dataSet["vol"].replace(",","")))
		dto["timestamp"] = str(dataSet["timestamp"])
		dto["last_price"] = float(dataSet["last"])
		dto["low_price"] = float(dataSet["low"])
		dto["ask"] = float(dataSet["sell"])
		dto["bid"] = float(dataSet["buy"])
		dto["high"] = float(dataSet["high"])
		dto["currency_pair"] = str(currencyPair)
		return dto

		