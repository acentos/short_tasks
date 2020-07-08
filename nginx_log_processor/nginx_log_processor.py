import os
import datetime
import re
import subprocess
import csv
from multiprocessing import Pool


NGINX_LOG_DIR = os.path.join(os.getcwd(), 'nginx_log_dir')
RESULT_FILE = os.path.join(os.getcwd(), 'nginx_log.csv')
LOG_FILE_SIZE = 1024
MP_POOL_NUM = 18


def get_access_log_list(nginx_log_dir):
	access_log_list = []
	ip_pattern = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
	for nld_file in os.listdir(nginx_log_dir):
		nld_file_path = os.path.join(nginx_log_dir, nld_file)

		fsize = int(os.path.getsize(nld_file_path) / 1024)
		if fsize < int(LOG_FILE_SIZE):

			with open(nld_file_path, 'r') as nld_file_obj:
				nld_file_fl = nld_file_obj.readline()

			if ((nld_file.endswith('.log')) and (ip_pattern.match(nld_file_fl.split(' ')[0]))):
				access_log_list.append(nld_file_path)

		else:
			print(f"Ignoring big file: {nld_file_path}")

	access_log_list.sort(key=os.path.getctime)
	return access_log_list

def get_short_country_name(uniq_ip):
	short_country = ""
	whois_cmd = [f"/usr/bin/whois {uniq_ip} | grep -i 'country' | head -1"]
	process_whois = subprocess.Popen(whois_cmd, stdout=subprocess.PIPE, shell=True)
	short_country = process_whois.communicate()[0].decode('utf-8').rsplit(' ', 1)[-1]
	
	if ( (re.search("^network:Country-Code:", short_country)) or 
		(re.search("^network:Country:", short_country)) or 
		(re.search("^contact:Country-Code:", short_country)) ):
		short_country = short_country.split(":")[-1]
	
	process_whois.stdout.close()
	
	return uniq_ip, str(short_country).rstrip("\n") if short_country else "NONE"

def get_nmap_open_port_by_ip(uniq_ip):
	nmap_cmd = [f"/usr/bin/nmap -Pn -F {uniq_ip} | grep -i 'open'"]
	process_nmap = subprocess.Popen(nmap_cmd, stdout=subprocess.PIPE, shell=True)
	open_port = ["".join(op.split(' ')[0]) for op in process_nmap.communicate()[0].decode('utf-8').split('\n') if op]
	process_nmap.stdout.close()

	return uniq_ip, str(open_port) if open_port else "NONE"

def read_access_log_file(access_log_file, num_count=0):
	ipaddress_list = []
	user_agent = []
	data_combain = {}

	with open(access_log_file, 'r') as alf:
		alf_data = alf.readlines()
		ipaddress_list = set([ alfr.split(' ')[0] for alfr in alf_data ])

		for uil in ipaddress_list:

			num_count +=1

			try:
			
			    user_agent = [" ".join(alfr.split(' ')[11:-1]) for alfr in alf_data if uil == alfr.split(' ')[0]]
			    request_url = [alfr.split(' ')[6] + ', ' for alfr in alf_data if uil == alfr.split(' ')[0]]
			
			except Exception as e:
				print(e)

			data_combain[uil] = {
			    '#': num_count,
			    'ipaddress': uil,
			    'user_agent': " ".join((set(user_agent))) if " ".join((set(user_agent))) else "NONE",
			    'total_user_agent': len(user_agent),
			    'request_url': "".join((set(request_url))) if "".join((set(request_url))) else "NONE",
			    'total_request_url': len(request_url),
			    'open_port': '',
			    'client_country': ''
			    }

	return data_combain

def get_num_count():

	if os.path.isfile(RESULT_FILE):
		with open(RESULT_FILE, 'r') as alf:
			reader = csv.DictReader(alf)
			last_row = [r for r in reader]

			if last_row:
				row_last_element = list(last_row[-1].values())[0]
				num_count = row_last_element.split(' ')[0]

				if num_count.isdigit():
					return int(num_count)

def writerow_to_csv(access_log_file, all_ip, all_port):
	with open(RESULT_FILE, "a") as alf:
		fieldnames = ['#', 'ipaddress', 'user_agent', 'total_user_agent', 'request_url', 'total_request_url', 'open_port', 'client_country']
		alf_writer = csv.DictWriter(alf, delimiter=' ', fieldnames=fieldnames)

		if get_num_count():
			num_count = get_num_count()

			for ralfv in read_access_log_file(access_log_file, num_count).values():
				ralfv['client_country'] = [
				    "".join(aip[1].replace('\r', '')).upper() for aip in all_ip[0] if aip[0] == ralfv.get('ipaddress')]
				ralfv['open_port'] = [
				    "".join(apo[1]) for apo in all_port[0] if apo[0] == ralfv.get('ipaddress')]
				alf_writer.writerow(ralfv)
		else:
			alf_writer.writeheader()
			for ralfv in read_access_log_file(access_log_file).values():
				ralfv['client_country'] = [
				    "".join(aip[1].replace('\r', '')).upper() for aip in all_ip[0] if aip[0] == ralfv.get('ipaddress')]
				ralfv['open_port'] = [
				    "".join(apo[1]) for apo in all_port[0] if apo[0] == ralfv.get('ipaddress')]
				alf_writer.writerow(ralfv)


def main():


	print(f"start: {datetime.datetime.now()}")
	

	pool_to_ip = Pool(MP_POOL_NUM)
	pool_to_port = Pool(MP_POOL_NUM)
	all_ip = []
	all_port = []
	for access_log_file in get_access_log_list(NGINX_LOG_DIR):
		with open(access_log_file, 'r') as alf:
			alf_data = alf.readlines()
			ipaddress_list = set([ alfr.split(' ')[0] for alfr in alf_data ])
			all_ip.append(pool_to_ip.map(get_short_country_name, ipaddress_list))
			all_port.append(pool_to_port.map(get_nmap_open_port_by_ip, ipaddress_list))
		
		print(f"run for: {access_log_file}")
		writerow_to_csv(access_log_file, all_ip, all_port)

	print(f"stop: {datetime.datetime.now()}")


if __name__ == '__main__':
	main()