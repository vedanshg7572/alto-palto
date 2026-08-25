## Project Description

This project demonstrates how to set up a **Site-to-Site VPN** between two office networks using IPSec (strongSwan). Site-A acts as the headquarters and Site-B is the branch office. The goal is to allow both sites to securely communicate over the internet as if they are on the same private network. It includes real config files, firewall scripts, a Python-based simulation, and a simple browser dashboard to monitor tunnel status.

---

## Synopsis

**Title:** Site-to-Site VPN Configuration using IPSec (strongSwan)

**Objective:** To establish a secure, encrypted communication tunnel between two geographically separate networks (Site-A and Site-B) using IPSec protocol so that hosts on both LANs can communicate with each other over the public internet.

**Technology Used:**
- Protocol: IPSec (IKEv2)
- Tool: strongSwan (Linux)
- Encryption: AES-256
- Integrity: SHA-256
- Key Exchange: Diffie-Hellman (modp2048)
- Firewall: iptables
- Simulation: Python 3

**Site-A Details:**
- LAN: 192.168.1.0/24
- Public IP: 203.0.113.1

**Site-B Details:**
- LAN: 192.168.2.0/24
- Public IP: 203.0.113.2

**How it works:**
1. Both routers authenticate each other using a Pre-Shared Key (PSK)
2. IKE Phase 1 creates a secure control channel (IKE SA)
3. IKE Phase 2 creates the actual data tunnel (IPSec SA)
4. All traffic between 192.168.1.x and 192.168.2.x goes through the encrypted tunnel
5. iptables rules ensure only VPN traffic is forwarded, rest goes to internet normally

**Result:** Any host on Site-A can ping or connect to any host on Site-B and vice versa, securely through the VPN tunnel.

---
