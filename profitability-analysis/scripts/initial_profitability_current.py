import re
from brownie import Contract, web3, REXOneWayMarket
from pycoingecko import CoinGeckoAPI
from scripts.constants import AVERAGE_GAS_PER_CONTRACT, FEE, REX_MARKETS
from datetime import datetime, timedelta
from time import sleep
from flask import Flask, request

app = Flask(__name__)
cg = CoinGeckoAPI()

def get_price_from_timestamp(token, timestamp):
    # To prevent rate limit
    print(f"This is the Timestamp: {timestamp}")
    try:
        return cg.get_coin_market_chart_range_by_id(token, vs_currency='usd', from_timestamp=timestamp, to_timestamp=timestamp + 2*3600)['prices'][0][1]
    except Exception as e:
        print(f"Exception: {e}")
        if token == 'richochet':
            return 1.00
        else:
            sleep(1)
            return cg.get_coin_market_chart_range_by_id(token, vs_currency='usd', from_timestamp=timestamp, to_timestamp=timestamp + 20*3600)['prices'][0][1]

def get_contract(name, address, abi, is_token):
    # "Token" contract instantiation doesnt have event data
    if(is_token):
        return Contract.from_abi(name, address, abi)
    else:
        return web3.eth.contract(address=address, abi=abi)

def get_name_from_address(address_to_find):
    for name, address in REX_MARKETS.items():
            if address_to_find == address:
                return name
    return "There is no such Key"

def calculate_revenue(address):
    market = get_contract(get_name_from_address(address), address, REXOneWayMarket.abi, False)

    total_streamed = web3.fromWei(market.functions.getTotalInflow().call(), 'ether')

    return tvs * FEE

def calculate_gas():
    end_day = datetime.now() - timedelta(hours=6)
    start_day = end_day - timedelta(days=30)
    total = 0

    for day in range((end_day - start_day).days):
        total += (get_price_from_timestamp('matic-network', (end_day - timedelta(days=day)).timestamp()) * AVERAGE_GAS_PER_CONTRACT)

    return total / 30

@app.route("/profitability")
def get_PL():
    contract_address = request.args['contract'] or ""

    if contract_address:
        total_pl = calculate_revenue(contract_address) - calculate_gas()
        return f"<h1>Your total P/L would be {total_pl}</h1>"
    else:
        return f"<h1>Please Input a Contract Address</h1>"

app.run(port=8080)
