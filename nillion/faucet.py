import aiohttp
import asyncio
from eth_account import Account
from eth_account.messages import encode_defunct
from fake_useragent import UserAgent
from twocaptcha import TwoCaptcha
from utils.utils import *
from utils.constants import *
from config import *

class Faucet(): 

    def __init__(self,): 

        self.two_captcha_api = TWO_CAPTCHA_API_KEY
            
    @error_handler('get captcha')
    def _get_captcha(self,): 

        solver = TwoCaptcha(self.two_captcha_api)

        ua=UserAgent().random
        result = solver.recaptcha(sitekey='6Le0TNUpAAAAAF6PF4LfeVBm56WbgdcPVV8Id6LF',
            url='https://faucet.testnet.nillion.com/',
            useragent=ua,
            #version='v3'
        )

        return result['code'],ua

    async def _ask_faucet(self,nil_address,token, user_agent): 

        data = {
            'address': nil_address,
            'denom': 'unil',
            'recaptcha': token
        }

        url = 'https://faucet.testnet.blockchain-cluster.nilogy.xyz/credit'

        headers = {
            'User-Agent': user_agent,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        } 

        proxy = get_proxy(nil_address, privates=NILLION_ADDRESSES)
        
        async with aiohttp.ClientSession() as session: 
            await self._post(session, url, headers=headers, data=data, proxy=proxy)



    @async_error_handler('get request')
    async def _get(self,session, url,headers = None, data = None, proxy = None):
        async with session.get(url,headers = headers, json = data, proxy = proxy) as response:
            assert response.status >199 and response.status <300, f'failed: status code: {response.status}: reason: {response.text()}'
            return await response.json()

    @async_error_handler('post request')
    async def _post(self,session, url,headers = None, data=None, proxy = None, get_json = False): 
        async with session.post(url,headers = headers, json=data, proxy = proxy) as response:
            if response.status <200 or response.status >299:
                logger.error( f'failed: status code: {response.status}: reason: {await response.text()}')
            else: 
                logger.success(f'request successful: {await response.text()}')

            if get_json == True:
                return await response.json()

    async def run(self,):

        with open(NILLION_ADDRESSES, 'r', encoding='utf-8') as file: 
            nil_addresses = file.read().splitlines()

        for nil_address in nil_addresses: 
            logger.info(f'solving captcha for {nil_address}')
            token, user_agent = self._get_captcha()
            logger.info(f'asking faucet for {nil_address}')
            await self._ask_faucet(nil_address, token, user_agent)
            logger.info(f'sleeping for {random.randint(*SLEEP)} seconds')
            await asyncio.sleep(random.randint(*SLEEP))


