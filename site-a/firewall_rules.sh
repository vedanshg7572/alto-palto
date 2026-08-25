#!/bin/bash
# Firewall rules for Site-A
# Run this after ipsec starts

# allow forwarding between LAN and VPN tunnel
echo 1 > /proc/sys/net/ipv4/ip_forward

# flush old rules first
iptables -F
iptables -t nat -F
iptables -t mangle -F

# allow established connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT

# allow IKE and ESP from Site-B
iptables -A INPUT -s 203.0.113.2 -p udp --dport 500 -j ACCEPT
iptables -A INPUT -s 203.0.113.2 -p udp --dport 4500 -j ACCEPT
iptables -A INPUT -s 203.0.113.2 -p esp -j ACCEPT

# allow traffic from Site-B LAN to Site-A LAN
iptables -A FORWARD -s 192.168.2.0/24 -d 192.168.1.0/24 -j ACCEPT
iptables -A FORWARD -s 192.168.1.0/24 -d 192.168.2.0/24 -j ACCEPT

# NAT for outbound internet (not VPN traffic)
iptables -t nat -A POSTROUTING -s 192.168.1.0/24 ! -d 192.168.2.0/24 -o eth0 -j MASQUERADE

echo "Firewall rules applied for Site-A"
