#!/usr/bin/env python3
from proxmoxer import ProxmoxAPI
from hurry.filesize import size, iec
from argparse import ArgumentParser
import configparser

def parse_args():
	parser = ArgumentParser()
	parser.add_argument("-c", "--cluster", dest="cluster", help="Enter the CLUSTER name", metavar="CLUSTER")
	args = parser.parse_args()
	return args

def read_config():
	config = configparser.ConfigParser()
	config.read('.config.ini', encoding='UTF-8')
	return config

def get_api(cluster_name):
	c = read_config()
	proxmox_host = c.get(cluster_name, 'host')
	proxmox_user = c.get(cluster_name, 'user')
	passw = c.get(cluster_name, 'pass')
	proxmox = ProxmoxAPI(host=proxmox_host, user=proxmox_user, password=passw, verify_ssl=False)
	return proxmox

def main():
	args = parse_args()
	# if args == 1:
	# 	args.help
	cluster_name = args.cluster
	api = get_api(cluster_name)
	for node in api.cluster.resources.get(type='node'):
		print("{0} --- {1} CPU --- {2}" .format(node['node'], size(node['maxcpu'], system=iec), size(node['maxmem'], system=iec)))

	for vm in api.cluster.resources.get(type='vm'):
		print("{0} --- {1} CPU --- {2}" .format(vm['id'], size(vm['maxdisk']), size(vm['maxmem'], system=iec)))

if __name__ == '__main__':
	main()

# vim: ft=python
