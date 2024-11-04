from nillion.faucet import Faucet
from nillion.deposit import Deposit
import questionary
import asyncio
import sys 
from loguru import logger
from utils.constants import logo

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
                        "Stake to nillion nodes",
                        "Fill nodes with faucet", 
                        "Exit"
                    ]
                ).ask()
                
    match choice: 

        case "Stake to nillion nodes":
            deposit = Deposit()
            deposit.run()

        case "Fill nodes with faucet": 
            faucet = Faucet()
            asyncio.run(faucet.run())
            
        case "Exit": 
            sys.exit()

if __name__ == '__main__': 
    logger.opt(raw=True).info(logo)
    print('\n\n')
    main()

