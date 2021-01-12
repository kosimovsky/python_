#!/usr/bin/env python3
from proxmoxer import ProxmoxAPI
from hurry.filesize import size, iec
from argparse import ArgumentParser
from termcolor import colored
import sys
import configparser


def parse_args():
	parser = ArgumentParser()
	parser.add_argument("-c", "--cluster", dest="cluster", help="Enter the CLUSTER name", metavar="CLUSTER")
	args = parser.parse_args()
	if not len(sys.argv) > 1:
		parser.print_help(sys.stderr)
		sys.exit(1)
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


def get_all_nodes(api):
	nodes = []
	for node in api.cluster.resources.get(type='node'):
		nodes.append(node['node'])
	print("There are nodes in this cluster:")
	for node in api.cluster.resources.get(type='node'):
		print("\t{0} --- {1} CPU --- {2}".format(colored(node['node'], 'green'), size(node['maxcpu'], system=iec),
		                                         size(node['maxmem'], system=iec)))
	return nodes


def get_all_vms_cpu(api, nodes):
	for node in nodes:
		cpu = 0
		for vm in api.cluster.resources.get(type='vm'):
			if node == vm['node'] and vm['status'] == 'running':
				cpu += vm['maxcpu']
		print("All allocated CPU on node {0} is: {1}".format(colored(node, 'green'), colored(size(cpu, system=iec), 'red')))


def get_all_vms_ram(api, nodes):
	for node in nodes:
		ram = 0
		for vm in api.cluster.resources.get(type='vm'):
			if node == vm['node'] and vm['status'] == 'running':
				ram += vm['maxmem']
		print("All allocated RAM on node {0} is: {1}".format(colored(node, 'green'), colored(size(ram, system=iec), 'red')))


def main():
	args = parse_args()
	api = get_api(args.cluster)
	nodes = get_all_nodes(api)
	print(colored('\n##############################################\n', 'yellow'))
	get_all_vms_cpu(api, nodes)
	print(colored('\n##############################################\n', 'yellow'))
	get_all_vms_ram(api, nodes)


if __name__ == '__main__':
	main()

# vim: ft=python
