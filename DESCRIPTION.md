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

## Lab Implementation Steps (PNETLab)

This project was implemented and tested on a **PNETLab server** accessed via browser and SSH.

**Step 1 — SSH into PNETLab Server**
- Opened terminal and connected via SSH:
  ssh root@192.168.247.128
- Server runs Ubuntu 18.04.5 LTS
- Verified system resources (4 Cores, ~6GB RAM, 97GB Disk)

**Step 2 — Open PNETLab in Firefox**
- Opened Firefox browser
- Navigated to: http://192.168.247.128/legacy/topology
- Logged in with admin credentials

**Step 3 — Added Network Nodes**
- Right clicked on topology canvas > Add a New Node
- Added the following devices:
  - Palo Alto (x2) — India Firewall and Dubai Firewall
  - Virtual PC (VPCS) (x2) — PC1 and PC2
  - Cisco IOL — ISP Router
  - Virtual PC (x2) — mgmt1 and mgmt2 for management access

**Step 4 — Built the Topology**
- Connected all devices with virtual links:
  PC1 (eth0) connected to PaloAlto1 (eth1/2)
  PaloAlto1 (eth1/1) connected to ISP
  ISP connected to PaloAlto2 (eth1/1)
  PaloAlto2 (eth1/2) connected to PC2 (eth0)
  Management PCs connected via eth1/3 on both firewalls

**Step 5 — Started All Devices**
- Clicked START on each device
- Waited for all nodes to become active

**Step 6 — Configured Palo Alto Firewalls**
- Accessed India PA GUI: https://192.168.10.1 (via mgmt1)
- Accessed Dubai PA GUI: https://192.168.20.1 (via mgmt2)
- Configured on both firewalls:
  - Interfaces (LAN, WAN, Tunnel)
  - Security Zones
  - Virtual Router and Static Routes
  - IKE Gateway and IKE Crypto Profile
  - IPSec Tunnel with Proxy IDs
  - Security Policies (allow VPN traffic)
  - NAT Exemption (so VPN traffic is not NATed)
- Applied Commit after each change

**Step 7 — Verified VPN Tunnel**
- Ran on Palo Alto CLI:
  show vpn ike-sa
  show vpn ipsec-sa
- Pinged from PC1 to PC2:
  ping 192.168.20.10
- Pinged from PC2 to PC1:
  ping 192.168.10.10
- Both pings successful — VPN tunnel working

---
