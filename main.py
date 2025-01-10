from nillion.faucet import Faucet
from nillion.deposit import Deposit
from nillion.server import ServerManager
from nillion.withdraw import Withdraw
from utils.constants import logo

import questionary
import asyncio
import sys 
from loguru import logger


logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> |  <level>{message}</level>",
    colorize=True
)


def main(): 

    choice = questionary.select(
                    "Select work mode:",
                    choices=[
                        "Unstake from nillion nodes",
                        "Stake to nillion nodes",
                        "Fill nodes with faucet", 
                        "Manage servers",
                        "Exit"
                    ]
                ).ask()
                
    match choice: 

        case "Stake to nillion nodes":
            deposit = Deposit()
            deposit.run()

        case "Unstake from nillion nodes": 
            withdraw = Withdraw()
            withdraw.run()

        case "Fill nodes with faucet": 
            faucet = Faucet()
            asyncio.run(faucet.run())
            
        case "Manage servers": 
            manager = ServerManager()
            manager.run()
            
        case "Exit": 
            sys.exit()

if __name__ == '__main__': 
    logger.opt(raw=True).info(logo)
    print('\n\n')
    main()

