
from loguru import logger
from math import ceil
from config import *
from .constants import *
import utils.eip1559 as eip1559
from web3 import Web3
import asyncio
import time
import random
import sys
import config

def intToDecimal(qty, decimal):
    return int(qty * int("".join(["1"] + ["0"]*decimal)))

def decimalToInt(price, decimal):
    return price/ int("".join((["1"]+ ["0"]*decimal)))


def error_handler(error_msg):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(0, ERR_ATTEMPTS):
                try: 
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"{error_msg}: {str(e)}")
                    logger.info(f'Retrying in 10 sec. Attempts left: {ERR_ATTEMPTS-i}')
                    time.sleep(10)
                    if i == ERR_ATTEMPTS-1: 
                        raise Exception(str(e))
        return wrapper
    return decorator

def async_error_handler(error_msg):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            for i in range(0, ERR_ATTEMPTS):
                try: 
                    return await func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"{error_msg}: {str(e)}")
                    logger.info(f'Retrying in 10 sec. Attempts left: {ERR_ATTEMPTS-i}')
                    await asyncio.sleep(10)
                    if i == ERR_ATTEMPTS-1: 
                        raise Exception(str(e))
        return wrapper
    return decorator

@error_handler('check tx')
def check_transaction(web3, hash_tx):

    tx_data = web3.eth.wait_for_transaction_receipt(hash_tx, timeout=MAX_TX_WAIT)

    if (tx_data['status'])== 1:
        logger.success(f'Transaction  {Web3.to_hex(tx_data["transactionHash"])}')
        return 1

    elif (tx_data['status'])== 0: 
        logger.success(f'Transaction  {Web3.to_hex(tx_data["transactionHash"])}')
        return 0

def build_and_send_tx(web3, account, tx, value = 0, return_hash: bool = False, custom_gas = 0, custom_gasprice=0):
    
    try:
        gas = tx.estimate_gas({'value':value, 'from':account.address, 'gas': custom_gas})

        gas = int(gas*1.2)

        nonce = web3.eth.get_transaction_count(account.address)

        tx_dict = {
                    'from':account.address,
                    'value':value,
                    'nonce':nonce,
                    'gas':gas,
                }

        tx_dict = eip1559.get_gas_prices(CHAIN_ID_TO_NAME[web3.eth.chain_id], tx_dict)

        built_tx = tx.build_transaction(
                tx_dict
            )

        signed_tx = account.sign_transaction(built_tx)
        hash_tx = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        logger.info(f'{account.address}: Transaction was sent')
        tx_passed = check_transaction(web3, hash_tx)

        if return_hash == False:
            return tx_passed
        else: 
            return hash_tx.hex()
        
    except Exception as e: 

        logger.error(f'{account.address}: {str(e)}')
        return 0

error_handler('gas waiter')
def wait_for_gas(web3): 

    while True: 
        
        try: 
            if web3.eth.gas_price < Web3.to_wei(MAX_GAS_PRICE, 'gwei'): 
                return  
            logger.info(f'Waiting for gas to drop. Current {Web3.from_wei(web3.eth.gas_price, "gwei")}')

        except: 
            pass 

        time.sleep(20)

def get_deposit_wallet(private_key, deposit_addresses=NILLION_ADDRESSES):

    with open(deposit_addresses, 'r') as f: 
        OKX_addresses = f.read().splitlines()

    with open(PRIVATE_KEYS, 'r') as f: 
       privates = f.read().splitlines()
            
    if len(OKX_addresses) != len(privates): 
        logger.error('privates don\'t match nillion addresses')
        sys.exit()

    n = privates.index(str(private_key))
    okx_address = OKX_addresses[n]

    return okx_address

def get_proxy(stark_private, privates=PRIVATE_KEYS): 

    with open(PROXIES, 'r') as f: 
        proxies = f.read().splitlines()
        if len(proxies) == 0:
            return None
        
    with open(privates, 'r') as f: 
        stark_privates = f.read().splitlines()
            
    n = stark_privates.index(str(stark_private))
    proxy = proxies[n]
    proxy = f'http://{proxy}'
    return proxy

def check_proxy():

    with open(PROXIES, 'r') as f: 
        proxies = f.read().splitlines()
    with open(PRIVATE_KEYS, 'r') as f: 
        keys = f.read().splitlines()
        private_keys = []
        for key in keys: 
            private_keys.append(key.split(':')[0])

    if len(proxies) < len(private_keys) and len(proxies) != 0:
        logger.error('Proxies do not match private keys')
        sys.exit()

def split_list_into_chunks(lst, n):
  
  size = ceil(len(lst) / n)

  return list(
    map(lambda x: lst[x * size:x * size + size],
    list(range(n)))
  )
