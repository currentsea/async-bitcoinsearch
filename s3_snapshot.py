import requests, argparse

def getSnapshotMetadata(): 
	snapshotMetadata = {
	  "type": "s3",
	  "settings": {
	    "bucket": "zeus33",
	    "region": "us-west-2"
	  }
	}
	return snapshotMetadata

def getArgs(): 
	parser = argparse.ArgumentParser(description="Parses snapshot args") 
	parser.add_argument("--es-url", default="http://data.btcdata.org", help="The elasticsearch host URL") 
	return parser.parse_args() 

if __name__ == "__main__": 
	args = getArgs()
	print (args.es_url)
	metadata = getSnapshotMetadata()
	print (metadata) 
