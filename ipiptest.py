#!/usr/bin/env python3

import argparse
import ipaddress
import os
import random
from scapy.all import *
import socket
import sys


class IPAddrAction(argparse.Action):
    """Validates IP argument parsing"""

    def __call__(self, parser, namespace, value, option_string=None):
        ip = str(ipaddress.IPv4Address(value))
        setattr(namespace, self.dest, ip)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('10.255.255.255', 1))
    return s.getsockname()[0]

def setup_args():
    parser = argparse.ArgumentParser(description='Creates an basic IPIP packet with a SYN and sends it')
    parser.add_argument('--outter_dst_ip', required=True, type=str, action=IPAddrAction)
    parser.add_argument('--inner_dst_ip', required=True, type=str, action=IPAddrAction)
    parser.add_argument('--dst_port', required=True, type=int)
    parser.add_argument('--src_port', type=int)
    parser.add_argument('--outter_src_ip', default=get_local_ip(), type=str, action=IPAddrAction)
    parser.add_argument('--inner_src_ip', default=get_local_ip(), type=str, action=IPAddrAction)
    return parser.parse_args()


def setup_ipip_packet(outter_dst_ip, inner_dst_ip, dst_port, outter_src_ip, inner_src_ip=None, src_port=None):
    if inner_src_ip is None:
        inner_src_ip = outter_src_ip
    if src_port is None:
        src_port = random.randint(1024,65535)
    outter = IP(src=outter_src_ip, dst=outter_dst_ip)
    inner = IP(src=inner_src_ip, dst=inner_dst_ip)
    syn = TCP(sport=src_port, dport=dst_port, flags='S', seq=1000)
    return outter/inner/syn

def send_packet(packet):
    sr1(packet, timeout=5)

if __name__ == '__main__':
    # check if we are running as root
    if os.geteuid() != 0:
        sys.exit("This script needs to be ran as root")
    args = setup_args()
    packet = setup_ipip_packet(args.outter_dst_ip,
                               args.inner_dst_ip,
                               args.dst_port,
                               args.outter_src_ip,
                               args.inner_src_ip,
                               args.src_port)
    send_packet(packet)

