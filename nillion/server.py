from config import * 
from utils.utils import * 

import paramiko
import questionary
import re
import json

class Server: 

    def __init__(self, hostname, password, username = 'root', port = 22): 

        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.hostname = hostname
        self.password = password
        self.username = username
        self.port = port 

        self.server_credentials_default_path = '/root/nillion/verifier/'

        self.connection_data = {
            'hostname': hostname,
            'port': port,
            'username': username,
            'password': password
        }
        
    
    @error_handler('running list of commands', retries=1)
    def run_setup_commands(self,): 

        self.client.connect(**self.connection_data)
        
        logger.info(f'Running commands in {self.hostname}')
        for command in SETUP_COMMAND_LIST: 

            logger.info(f'>>> {command}')
            stdin, stdout, stderr = self.client.exec_command(command)
            stdout.channel.recv_exit_status() #waiting till the command completes

            output = stdout.read().decode()
            errors = stderr.read().decode()
            
            print(f'\n{output}')
            if errors and not 'WARNING' in str(errors) and not 'Warning' in (errors):
                logger.warning(f'\n{errors}')

            if command == INITIALIZE_COMMAND: 

                sftp = self.client.open_sftp()
                files = sftp.listdir(self.server_credentials_default_path)

                if 'credentials.json' in files: 
                    with sftp.file(self.server_credentials_default_path+'credentials.json', 'r') as remote_file:
                        file_content = remote_file.read().decode('utf-8')  
                        data = json.loads(file_content)

                    with open(NODES_DATA, 'a', encoding='utf-8') as file: 
                        file.write(f"{self.hostname};{data['address']};{data['pub_key']};{data['priv_key']}\n")
                    
                    logger.success(f'{self.hostname} successfully saved node data in {NODES_DATA}')
        
        self.client.close()

        return 1

    @error_handler('starting verifier')
    def start_verifier(self,): 

        self.client.connect(**self.connection_data)
        
        logger.info(f'Running command in {self.hostname}')

        logger.info(f'>>> {START_COMMAND}')
        stdin, stdout, stderr = self.client.exec_command(START_COMMAND)
        stdout.channel.recv_exit_status() #waiting till the command completes

        output = stdout.read().decode()
        errors = stderr.read().decode()
        
        print(f'\n{output}')
        if errors and not 'WARNING' in str(errors) and not 'Warning' in (errors):
            logger.warning(f'\n{errors}')
        
        self.client.close()

        return 1

    @error_handler('checking containers')
    def check_verifier(self,): 

        logger.info(f'Checking container state on {self.hostname}')
    
        self.client.connect(**self.connection_data)
        command = f'docker ps --format "{{.Names}}" --filter "name=nillion"' 
        command = f'docker ps --format "{{.Names}}" --filter "name=nillion"' 
        stdin, stdout, stderr = self.client.exec_command(command)
        containers_output = stdout.read().decode('utf-8').strip()

        if containers_output:
            containers = containers_output.splitlines()
                
            logger.info(f"Container Name: nillion last logs: ")

            # Get the last N lines of logs for each container
            stdin, stdout, stderr = self.client.exec_command(f'docker logs --tail 100 nillion-new')
            stdin, stdout, stderr = self.client.exec_command(f'docker logs --tail 100 nillion-new')
            stdout.channel.recv_exit_status()
            logs = stdout.read().decode()
            print(f"{logs}")
            print("="*40)

            match =re.findall(r"\b" + re.escape('Synced with network') + r"\b", logs)

            if match:

                logger.success(f'{self.hostname}: Nillion is synced with network')
                self.client.close()
                return 1

            else:
                match =re.findall(r"\b" + re.escape('Starting 10 minute warmup period') + r"\b", logs)

                if match: 
                    logger.debug(f'{self.hostname}: Nillion is in warmup period, check later')
                    return 1
                else:
                    logger.warning(f'{self.hostname}: Synced message not found. Check logs the container may be down')
                    self.client.close()
                    return 0
            else:
                match =re.findall(r"\b" + re.escape('Starting 10 minute warmup period') + r"\b", logs)

                if match: 
                    logger.debug(f'{self.hostname}: Nillion is in warmup period, check later')
                    return 1
                else:
                    logger.warning(f'{self.hostname}: Synced message not found. Check logs the container may be down')
                    self.client.close()
                    return 0
            
        else:
            logger.warning("No running containers found.")
            self.client.close()
            return 0
        

class ServerManager: 

    def __init__(self, servers_path = SERVERS): 

        self.servers = []

        with open(servers_path, 'r', encoding='utf-8') as f: 
            servers_raw = f.read().splitlines()

        for server_data in servers_raw: 
            self.servers.append(Server(*server_data.split(':')))

    def run(self,): 

        while True:
            print('\n')
            choice = questionary.select(
                "Select work mode:",
                choices=["setup verifiers", "run verifiers", "check verifiers", "Exit"]
            ).ask()
            
            match choice: 

                case "setup verifiers": 
                    self.run_setup()

                case "run verifiers":
                    self.run_verifiers()

                case "check verifiers": 
                    self.check_containers()
                
                case "Exit": 
                    sys.exit()
                case _:
                    pass
            

    def run_setup(self,): 

        for server in self.servers:

            try:
                assert server.run_setup_commands() == 1, 'failed to execute all commands'

            except AssertionError as e: 
                logger.error(f'{server.hostname}: {str(e)}')
                continue

        return 
        
    def run_verifiers(self,): 

        for server in self.servers:

            try:
                assert server.start_verifier() == 1, 'failed to run verifier'

            except AssertionError as e: 
                logger.error(f'{server.hostname}: {str(e)}')
                continue

        return 

    def check_containers(self,): 

        for server in self.servers:

            try:
                assert server.check_verifier() == 1, 'failed to check verifier'

            except AssertionError as e: 
                logger.error(f'{server.hostname}: {str(e)}')
                continue

        return




 

    
