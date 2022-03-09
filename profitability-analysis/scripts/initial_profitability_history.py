from brownie import Contract, web3, REXOneWayMarket, RicochetLaunchpadHelper
from pycoingecko import CoinGeckoAPI
import pandas as pd
from .constants import *
from time import sleep

cg = CoinGeckoAPI()

def get_price_from_timestamp(token, timestamp):
    # To prevent rate limit
    sleep(1)
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

def get_timestamp(block_number):
    return web3.eth.get_block(block_number).timestamp

def calculate_fees(market_name, token_name, event_args, timestamp):
    if market_name not in ["UsdcToRexslpEthUsdc", "UsdcToRexslpEthIdle"]:
        fee_collected = event_args['feeCollected']
    else: 
        fee_collected = event_args['totalAmount'] * .02
    return float(web3.fromWei(fee_collected, 'ether')) * get_price_from_timestamp(token_name, timestamp)

def calculate_gas(txn_hash, timestamp):
    txn = web3.eth.get_transaction_receipt(txn_hash)
    return float(web3.fromWei(txn['gasUsed'] * txn['effectiveGasPrice'], 'ether')) * get_price_from_timestamp('matic-network', timestamp)

def grab_market_data(restarted):
    event_signature_hash = web3.sha3(text="Distribution(uint256,uint256,address)").hex()
    # Table to generate CSV
    profitability_df = pd.read_csv('reports/profitability_analysis.csv')

    batch_size = 2000
    total_end = web3.eth.get_block_number()

    last_market_name = profitability_df.iloc[-1]['marketName']
    last_market_address = profitability_df.iloc[-1]['marketAddress']
    last_block = profitability_df.iloc[-1]['blockNumber']

    last_market_index = list(REX_MARKETS.items()).index((last_market_name, last_market_address))

    # For standard markets
    for market_name, market_address in list(REX_MARKETS.items())[last_market_index:]:
        if restarted:
            start = last_block
            restarted = False
        else:
            start = REX_MARKET_BLOCK_START[market_name]
        if market_name == 'UsdcToRic':
            market = get_contract(market_name, market_address, RicochetLaunchpadHelper.abi, False)
        else:
            market = get_contract(market_name, market_address, REXOneWayMarket.abi, False)
        for page in range(start, total_end, batch_size):
            sleep(1)
            print(f"Market Name: {market_name}")
            event_filter = market.events.Distribution.createFilter(fromBlock=page, toBlock=page+batch_size, topics=event_signature_hash)
            events = event_filter.get_all_entries()
            for event in events:
                timestamp = get_timestamp(event['blockNumber'])
                print(f"Block Number: {event['blockNumber']}")
                if (event['transactionHash'].hex() not in profitability_df.values):

                    if REX_MARKET_NATIVE_TOKEN[market_name] == 'richochet':
                        token_address = "0x263026E7e53DBFDce5ae55Ade22493f828922965"
                    else:
                        token_address = event['args']['token']

                    if ((token_address == '0x3aD736904E9e65189c3000c7DD2c8AC8bB7cD4e3') or (token_address == '0x263026E7e53DBFDce5ae55Ade22493f828922965')) and ((market_name == 'UsdcToRexslpEthUsdc') or (market_name == 'UsdcToRexslpEthIdle')):
                        native_token = REX_MARKET_NATIVE_TOKEN[market_name][1]
                    elif ((token_address == '0xDaB943C03f9e84795DC7BF51DdC71DaF0033382b') or (token_address == '0x263026E7e53DBFDce5ae55Ade22493f828922965')) and ((market_name == 'UsdcToRexslpEthUsdc') or (market_name == 'UsdcToRexslpEthIdle')):
                        native_token = REX_MARKET_NATIVE_TOKEN[market_name][0]
                    else:
                        native_token = REX_MARKET_NATIVE_TOKEN[market_name]

                    if NATIVE_TOKEN_ADDRESSES[native_token] == token_address:
                        print('Adding Info....')
                        fees_collected = calculate_fees(market_name, native_token, event['args'], timestamp)
                        gas_spent = calculate_gas(event['transactionHash'].hex(), timestamp)
                        to_append = pd.DataFrame([[
                            event['transactionHash'].hex(),
                            event['blockNumber'],
                            timestamp,
                            market_name,
                            market_address,
                            token_address,
                            REX_MARKET_NATIVE_TOKEN[market_name],
                            fees_collected,
                            gas_spent,
                            fees_collected - gas_spent
                        ]], columns=[
                            'transactionHash',
                            'blockNumber',
                            'timestamp',
                            'marketName',
                            'marketAddress',
                            'nativeTokenAddress',
                            'nativeTokenID',
                            'feeCollected[USD]',
                            'gasSpent[USD]',
                            'overallPL'
                        ])
                        profitability_df = pd.concat([profitability_df, to_append])
                        profitability_df.to_csv("reports/profitability_analysis.csv", index=False)

    return profitability_df

def main(restarted):
    try:
        df = grab_market_data(restarted)
        df.to_csv('reports/profitability_analysis.csv', index=False)
    except Exception as e:
        print(f"Exception: {e}")
        if(KeyboardInterrupt):
            pass
        print("---Restarting Program---")
        main(True)

# The event to watch
# event Distribution(
#         uint256 totalAmount,
#         uint256 feeCollected,
#         address token
#     );

# Event response
# AttributeDict(
#     {'args': AttributeDict(
#         {'totalAmount': 69779196182345,
#          'feeCollected': 1424065228211, 
#          'token': '0x27e1e4E6BC79D93032abef01025811B7E4727e85'}
#          ), 
#          'event': 'Distribution', 
#          'logIndex': 149, 
#          'transactionIndex': 21, 
#          'transactionHash': HexBytes('0x2171e7a9ff147afb3aad2856e52b0e5e706fc90bd7569f6018c97a930c2782bf'), 
#          'address': '0x9BEf427fa1fF5269b824eeD9415F7622b81244f5', 
#          'blockHash': HexBytes('0xb9a9ea4cc528da5efad0d542f62d18cde4fce1c38c86de4b035262a99a3e788c'), 
#          'blockNumber': 19391461})

