#!/bin/bash
# Firewall rules for Site-B
# Run this script after ipsec starts

echo 1 > /proc/sys/net/ipv4/ip_forward

iptables -F
iptables -t nat -F
iptables -t mangle -F

iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT

# allow IKE/ESP from Site-A
iptables -A INPUT -s 203.0.113.1 -p udp --dport 500 -j ACCEPT
iptables -A INPUT -s 203.0.113.1 -p udp --dport 4500 -j ACCEPT
iptables -A INPUT -s 203.0.113.1 -p esp -j ACCEPT

# allow cross-site traffic
iptables -A FORWARD -s 192.168.1.0/24 -d 192.168.2.0/24 -j ACCEPT
iptables -A FORWARD -s 192.168.2.0/24 -d 192.168.1.0/24 -j ACCEPT

# internet NAT (excluding VPN subnet)
iptables -t nat -A POSTROUTING -s 192.168.2.0/24 ! -d 192.168.1.0/24 -o eth0 -j MASQUERADE

echo "Firewall rules applied for Site-B"
