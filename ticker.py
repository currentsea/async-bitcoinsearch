
class Ticker:

	def __init__(self): 
		pass

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
