from config import *
from utils.utils import *
from utils.constants import *

class Withdraw():

    def __init__(self,):

        self.web3 = Web3(Web3.HTTPProvider(RPC))

    def deposit_to_nillion(self, private_key): 


        account = self.web3.eth.account.from_key(private_key)

        contract = self.web3.eth.contract(address=DEPOSIT_CONTRACT, abi=DEPOSIT_CONTRACT_ABI) 
        
        balance = contract.functions.balanceOf(account.address).call()
        if balance < 1: 
            logger.warning(f'{account.address}: has no eth staked to nillion')
            return 0
        
        tx = contract.functions.withdraw(balance)

        logger.info(f'{account.address}: withdrawing {decimalToInt(balance, 18)} ETH')

        wait_for_gas(self.web3)

        sent_tx = build_and_send_tx(self.web3, account, tx)

    def run(self): 

        with open(PRIVATE_KEYS, 'r', encoding='utf-8') as file: 
            private_keys = file.read().splitlines()

        for private_key in private_keys: 
            self.deposit_to_nillion(private_key)
            time.sleep(random.randint(*SLEEP))

