#!/usr/bin/env python

import fcntl
import json
import re
import socket
import struct
import sys


# from sockios.h file
SIOCGIFNAME     = 0x8910  # get iface name
SIOCSIFLINK     = 0x8911  # set iface channel
SIOCGIFCONF     = 0x8912  # get iface list
SIOCGIFFLAGS    = 0x8913  # get flags
SIOCSIFFLAGS    = 0x8914  # set flags
SIOCGIFADDR     = 0x8915  # get PA address
SIOCSIFADDR     = 0x8916  # set PA address
SIOCGIFDSTADDR  = 0x8917  # get remote PA address
SIOCSIFDSTADDR  = 0x8918  # set remote PA address
SIOCGIFBRDADDR  = 0x8919  # get broadcast PA address
SIOCSIFBRDADDR  = 0x891a  # set broadcast PA address
SIOCGIFNETMASK  = 0x891b  # get network PA mask
SIOCSIFNETMASK  = 0x891c  # set network PA mask
SIOCGIFMETRIC   = 0x891d  # get metric
SIOCSIFMETRIC   = 0x891e  # set metric
SIOCGIFMEM      = 0x891f  # get memory address (BSD)
SIOCSIFMEM      = 0x8920  # set memory address (BSD)
SIOCGIFMTU      = 0x8921  # get MTU size
SIOCSIFMTU      = 0x8922  # set MTU size
SIOCSIFNAME     = 0x8923  # set interface name
SIOCSIFHWADDR   = 0x8924  # set hardware address
SIOCGIFENCAP    = 0x8925  # get/set encapsulations
SIOCSIFENCAP    = 0x8926  #
SIOCGIFHWADDR   = 0x8927  # Get hardware address
SIOCGIFSLAVE    = 0x8929  # Driver slaving support
SIOCSIFSLAVE    = 0x8930  #


def get_hardware_address(ifname):
    """ Return the MAC (hardware) Address of a given Interface. """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ifreq = struct.pack("256s", ifname[:15])
    try:
        pack = fcntl.ioctl(sock.fileno(), SIOCGIFHWADDR, ifreq)
        return ":".join(["%02x" % ord(char) for char in pack[18:24]])
    except IOError:
        pack = None

    return ""


def get_ipv4_address(ifname):
    """ Return the IP Address of a given Interface. """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ifreq = struct.pack("256s", ifname[:15])
    try:
        pack = fcntl.ioctl(sock.fileno(), SIOCGIFADDR, ifreq)
        return socket.inet_ntoa(pack[20:24])
    except IOError:
        pack = None

    return ""


def get_network_info():
    """
    Find the Network Interfaces and Return a list of them
    with Addresses and Information of Usage.
    """
    interfaces = []

    validate_interface = re.compile("^\\s*(\\S+):(.*)$")
    split_values = re.compile("(\\S+)")

    for line in open("/proc/net/dev", "r"):
        interface = validate_interface.match(line)
        if interface:
            ifname = interface.groups()[0]
            values = map(int, split_values.findall(interface.groups()[1]))
            interfaces.append({
                'name' : ifname,
                'ipv4' : get_ipv4_address(ifname),
                'hwaddr' : get_hardware_address(ifname),
                'receive' : {
                    'bytes'      : values[ 0],
                    'packets'    : values[ 1],
                    'drop'       : values[ 2],
                    'errs'       : values[ 3],
                    'fifo'       : values[ 4],
                    'frame'      : values[ 5],
                    'compressed' : values[ 6],
                    'multicast'  : values[ 7]
                },
                'transmit' : {
                    'bytes'      : values[ 8],
                    'packets'    : values[ 9],
                    'errs'       : values[10],
                    'drop'       : values[11],
                    'fifo'       : values[12],
                    'frame'      : values[13],
                    'compressed' : values[14],
                    'multicast'  : values[15]
                }
            })

    return interfaces


def main(argv):
    """
    The function to be executed on a standalone call of the program.
    Used to test the function of the script.
    """
    print json.dumps(get_network_info(), indent=4)


if __name__ == "__main__":
    main(sys.argv[1:])
