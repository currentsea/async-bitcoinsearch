# Bitcoin ElasticsearchV2 (Working Name)  

## About
This is a tool for collecting bitcoin data and storing it into an elasticsearch cluster 

## NOTICE 
This project has been tested on `3.5.2` and _will not work_  `Python 2.X.X` 

## Pre-requisites
* Homebrew (not required, but will help a lot) - `https://brew.sh` has instructions on how to install 
* Elasticsearch (2.4.1) (can be installed with `brew install elasticsearch` if you're on a mac and have homebrew installed)  
* Kibana (4.5.1) (can be installed with `brew install kibana` if you're on a mac with homebrew installed) 

## API Source
* The channels used in the websockets connector are from the OkCoin Public Websockets API which can be read about in detail at this URL: `https://www.okcoin.com/about/ws_api.do`

## Python 3 Modules
* This project requires `pip3` which can be acquired by running the following command 
`sudo easy_install 

## Like My Work? 
* Feel free to donate to the BTC Address shown below :) 
`1AUr1JGVHc5VXozb2B2iJeqaW4v9SUhvQD`
*_Your Donations are much appreciated and keep projects like this alive and well._*

## Keybase
* Check me out on keybase. https://keybase.io/currentsea 

## IMPLEMENTED SOCKETS
The following list of OkCoin Websocket Channels has been implemented successfully
* ok_sub_spotusd_btc_depth_20
* ok_sub_spotusd_ltc_depth_20
* ok_sub_spotusd_btc_depth_60
* ok_sub_spotusd_ltc_depth_60
* ok_sub_futureusd_btc_depth_this_week_20
* ok_sub_futureusd_btc_depth_next_week_20
* ok_sub_futureusd_btc_depth_quarter_20
* ok_sub_futureusd_btc_depth_this_week_60
* ok_sub_futureusd_btc_depth_next_week_60
* ok_sub_futureusd_btc_depth_quarter_60
* ok_sub_futureusd_ltc_depth_this_week_20
* ok_sub_futureusd_ltc_depth_next_week_20
* ok_sub_futureusd_ltc_depth_quarter_20
* ok_sub_futureusd_ltc_depth_this_week_60
* ok_sub_futureusd_ltc_depth_next_week_60
* ok_sub_futureusd_ltc_depth_quarter_60
