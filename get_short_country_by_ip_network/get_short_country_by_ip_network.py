import subprocess
import time
import re

from multiprocessing import Pool

all_ip_network_list = []
ip_range = range(1, 256)
ip_range_file = 'ip_range_file.txt'
result_file = 'ip_network_countires.txt'

start_time = time.time()

for ip_o in ip_range:
	for ip_t in ip_range:
		for ip_r in ip_range:
			all_ip_network_list.append(f"{ip_o}.{ip_t}.{ip_r}.0")

print("Total IP networks: {0}".format(len(all_ip_network_list)))

with open(ip_range_file, 'a') as f_obj:
	f_obj.write(str(all_ip_network_list))

def get_short_country_name(uniq_ip_network):
	short_country = ""
	whois_cmd = [f"/usr/bin/whois {uniq_ip_network} | grep -i 'country' | head -1"]
	process_whois = subprocess.Popen(whois_cmd, stdout=subprocess.PIPE, shell=True)
	short_country = process_whois.communicate()[0].decode('utf-8').rsplit(' ', 1)[-1]
	
	if ( (re.search("^network:Country-Code:", short_country)) or 
		(re.search("^network:Country:", short_country)) or 
		(re.search("^contact:Country-Code:", short_country)) ):
		short_country = short_country.split(":")[-1]
	
	
	with open(result_file, 'a') as f_obj:
		f_obj.write(
			str(uniq_ip_network) + " : " + str(short_country))
	process_whois.stdout.close()


if __name__ == '__main__':

	if all_ip_network_list:
		with Pool(100) as p:
			p.map(get_short_country_name, all_ip_network_list)

	print("Total time: {0}s".format(int(time.time() - start_time)))