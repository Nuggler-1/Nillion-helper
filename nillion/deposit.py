from config import *
from utils.utils import *
from utils.constants import *

class Deposit():

    def __init__(self,):

        self.web3 = Web3(Web3.HTTPProvider(RPC))

    def deposit_to_nillion(self, private_key): 


        account = self.web3.eth.account.from_key(private_key)
        nillion_node_address = get_deposit_wallet(private_key)
        contract = self.web3.eth.contract(address=DEPOSIT_CONTRACT, abi=DEPOSIT_CONTRACT_ABI) 
        
        tx = contract.functions.deposit(nillion_node_address)

        logger.info(f'{account.address}: Deposit to Nillion Node - {nillion_node_address}')

        wait_for_gas(self.web3)

        sent_tx = build_and_send_tx(self.web3, account, tx, value=Web3.to_wei(AMOUNT_TO_DEPOSIT, 'ether'))

    def run(self): 

        with open(PRIVATE_KEYS, 'r', encoding='utf-8') as file: 
            private_keys = file.read().splitlines()

        for private_key in private_keys: 
            self.deposit_to_nillion(private_key)
            time.sleep(random.randint(*SLEEP))


