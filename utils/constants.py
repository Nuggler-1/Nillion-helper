DEPOSIT_CONTRACT = '0x2E258DBb253b7e1c0846f212b9B36a2F783bA436'
DEPOSIT_CONTRACT_ABI = '[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"dst","type":"address"},{"indexed":false,"internalType":"uint256","name":"wad","type":"uint256"},{"indexed":false,"internalType":"string","name":"verifierAddress","type":"string"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"src","type":"address"},{"indexed":false,"internalType":"uint256","name":"wad","type":"uint256"},{"indexed":false,"internalType":"string","name":"verifierAddress","type":"string"}],"name":"Withdrawal","type":"event"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_verifierAddress","type":"string"}],"name":"deposit","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"_address","type":"address"}],"name":"getBalanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_address","type":"address"}],"name":"getVerifierAddress","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"verifierAddress","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"wad","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'

CHAIN_ID_TO_NAME = {

    42161:'ARBITRUM',
    10: 'OPTIMISM',
    56: 'BSC', 
    43114: 'AVAX',
    137: 'POLYGON',
    1116: 'CORE',
    8453: 'BASE', 
    1: 'Ethereum',
    167000: 'TAIKO'

}

USER_DATA = 'user_data/'
NILLION_ADDRESSES = USER_DATA + 'nillion_node_addresses.txt'
PRIVATE_KEYS = USER_DATA + 'private_keys.txt'
PROXIES = USER_DATA + "proxies.txt"

logo = r"""
_______ _______ _______ _______ _    _ _     _     
|______    |       |    |_____|  \  /  |____/      
|          |       |    |     |   \/   |    \_     
"""