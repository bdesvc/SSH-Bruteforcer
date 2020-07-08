import random,sys

for i in range(int(sys.argv[1])):
	i1 = str(random.randint(1,255))
	i2 = str(random.randint(1,255))
	i3 = str(random.randint(1,255))
	i4 = str(random.randint(1,255))

	ip = f'{i1}.{i2}.{i3}.{i4}'
	with open('ips.txt','a') as fp:
		fp.write(ip+'\n')
		print(f'Added IP -> {ip}')