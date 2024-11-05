RPC = 'https://rpc.ankr.com/eth'
TWO_CAPTCHA_API_KEY = ''

SLEEP = [100, 900]
AMOUNT_TO_DEPOSIT = 0.05

ERR_ATTEMPTS = 1
MAX_GAS_PRICE = 6.2
ETH_GAS_MULT = 1.1
MAX_TX_WAIT = 500

INITIALIZE_COMMAND = 'docker run -v ./nillion/verifier:/var/tmp nillion/verifier:v1.0.1 initialise'
START_COMMAND = 'docker run -d --name nillion -v ./nillion/verifier:/var/tmp nillion/verifier:v1.0.1 verify --rpc-endpoint "https://testnet-nillion-rpc.lavenderfive.com"'

SETUP_COMMAND_LIST = [

    'sudo apt update ',
    'sudo apt install apt-transport-https ca-certificates curl gnupg2 software-properties-common -y',
    'curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -',
    'sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"',
    'sudo apt update ',
    'apt-cache policy docker-ce ',
    'sudo apt install docker-ce -y',
    'docker pull nillion/verifier:v1.0.1',
    'mkdir -p nillion/verifier',
    INITIALIZE_COMMAND
]
