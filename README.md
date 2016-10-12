# Bitcoin Elasticsearch V2 

## About
This is a tool for collecting bitcoin data and storing it into an elasticsearch cluster 

## Pre-requisites
* Homebrew (not required, but will help a lot) - `https://brew.sh` has instructions on how to install 
* Elasticsearch (2.4.1) (can be installed with `brew install elasticsearch` if you're on a mac and have homebrew installed)  
* Kibana (4.5.1) (can be installed with `brew install kibana` if you're on a mac with homebrew installed) 

## API Source
* The channels used in the websockets connector are from the OkCoin Public Websockets API which can be read about in detail at this URL: `https://www.okcoin.com/about/ws_api.do`