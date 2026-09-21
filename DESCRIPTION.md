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

This project was implemented and tested on a PNETLab server running on a local Ubuntu machine, accessed via Firefox browser and SSH terminal.

---

**Step 1 — SSH into PNETLab Server**

Opened terminal (PuTTY / Windows Terminal) and connected to the PNETLab server:

    ssh root@192.168.247.128

After successful login, the server showed:
- OS: Ubuntu 18.04.5 LTS
- IP address for pnet0: 192.168.247.128
- System Load: 3.09
- Memory Usage: 14% of 5949MB
- Disk: 97GB total, 9% used
- CPU: 4 Cores

This confirmed the server was healthy and ready to run virtual network devices.

---

**Step 2 — Open PNETLab in Firefox Browser**

Opened Firefox browser on the host machine and navigated to:

    http://192.168.247.128/legacy/topology

Logged in with PNETLab admin credentials. The topology canvas opened where we can build virtual network labs.

---

**Step 3 — Checked System Status**

Before adding devices, checked system resources:
- Went to More > System Status in PNETLab
- Confirmed sufficient RAM and CPU available
- Total Nodes running: 0 (fresh start)

---

**Step 4 — Added Network Nodes to Topology**

Right-clicked on topology canvas and selected Add a New Node. Added the following devices one by one:

    Device 1:  PaloAlto1   (Template: Palo Alto)   — India Firewall
    Device 2:  PaloAlto2   (Template: Palo Alto)   — Dubai Firewall
    Device 3:  PC1         (Template: Virtual PC)  — India Client PC
    Device 4:  PC2         (Template: Virtual PC)  — Dubai Client PC
    Device 5:  ISP         (Template: Cisco IOL)   — Internet/ISP Router
    Device 6:  mgmt1       (Template: Virtual PC)  — Management PC for India PA
    Device 7:  mgmt2       (Template: Virtual PC)  — Management PC for Dubai PA

---

**Step 5 — Connected Devices and Built Topology**

Connected all devices using virtual links in PNETLab canvas:

    PC1 (eth0)        ----->  PaloAlto1 (eth1/2)   [India LAN link]
    PaloAlto1 (eth1/1) ----->  ISP                  [India WAN link]
    ISP               ----->  PaloAlto2 (eth1/1)   [Dubai WAN link]
    PaloAlto2 (eth1/2) ----->  PC2 (eth0)           [Dubai LAN link]
    PaloAlto1 (eth1/3) ----->  mgmt1 (eth0)         [India Management]
    PaloAlto2 (eth1/3) ----->  mgmt2 (eth0)         [Dubai Management]

Final topology: PC1 -- PaloAlto1 -- ISP -- PaloAlto2 -- PC2

---

**Step 6 — Started All Devices**

Clicked START button on all nodes from the topology canvas. Waited for all devices to become active (green status). Both Palo Alto firewalls take 3-5 minutes to fully boot up.

---

**Step 7 — Configured PC1 and PC2 IP Addresses**

On PC1 (VPCS):

    ip 192.168.10.10 192.168.10.1 24
    (IP: 192.168.10.10, Gateway: 192.168.10.1, Mask: /24)

On PC2 (VPCS):

    ip 192.168.20.10 192.168.20.1 24
    (IP: 192.168.20.10, Gateway: 192.168.20.1, Mask: /24)

---

**Step 8 — Configured ISP Router**

On ISP (Cisco IOL), configured two interfaces to connect both firewalls:

    interface e0/0
     ip address 100.1.1.2 255.255.255.0
     no shutdown

    interface e0/1
     ip address 200.1.1.2 255.255.255.0
     no shutdown

---

**Step 9 — Configured India Palo Alto Firewall**

Accessed India PA GUI via mgmt1 browser: https://192.168.10.1
Login: admin / admin

a) Interfaces:
    ethernet1/1 (WAN): IP 100.1.1.1/24, Zone: WAN
    ethernet1/2 (LAN): IP 192.168.10.1/24, Zone: LAN
    tunnel.1: no IP, Zone: VPN-Zone

b) Virtual Router — Static Routes:
    Default route: 0.0.0.0/0 via 100.1.1.2
    Dubai LAN:     192.168.20.0/24 via tunnel.1

c) IKE Crypto Profile:
    Name: IKE-Crypto
    DH Group: group2, Encryption: aes-128-cbc, Auth: sha1
    Lifetime: 8 hours

d) IKE Gateway:
    Name: IKE-GW-India
    Interface: ethernet1/1, Local IP: 100.1.1.1
    Peer IP: 200.1.1.1, PSK: Test@1234
    IKE Version: IKEv1

e) IPSec Crypto Profile:
    Name: IPSEC-Crypto
    ESP Encryption: aes-128-cbc, Auth: sha1
    DH Group: group2, Lifetime: 1 hour

f) IPSec Tunnel:
    Name: VPN-To-Dubai
    Tunnel Interface: tunnel.1
    IKE Gateway: IKE-GW-India
    Proxy ID — Local: 192.168.10.0/24, Remote: 192.168.20.0/24

g) Security Policies:
    Rule 1 (India to Dubai): LAN zone -> VPN zone, Action: Allow
    Rule 2 (Dubai to India): VPN zone -> LAN zone, Action: Allow

h) NAT Exemption:
    Source: 192.168.10.0/24, Destination: 192.168.20.0/24
    Action: No Source NAT (so VPN traffic is not translated)

Clicked Commit to save all changes.

---

**Step 10 — Configured Dubai Palo Alto Firewall**

Accessed Dubai PA GUI via mgmt2 browser: https://192.168.20.1
Login: admin / admin

Same steps as India PA but with mirrored IPs:
    ethernet1/1 (WAN): IP 200.1.1.1/24, Zone: WAN
    ethernet1/2 (LAN): IP 192.168.20.1/24, Zone: LAN
    tunnel.1: Zone: VPN-Zone

    IKE Gateway Peer IP: 100.1.1.1 (India WAN)
    PSK: Test@1234 (same as India)
    Proxy ID Local: 192.168.20.0/24, Remote: 192.168.10.0/24

Clicked Commit to save all changes.

---

**Step 11 — Verified VPN Tunnel Status**

On Palo Alto CLI (both firewalls):

    show vpn ike-sa          (should show IKE SA as active)
    show vpn ipsec-sa        (should show IPSec SA as active)
    show vpn flow name VPN-To-Dubai

---

**Step 12 — End-to-End Ping Test**

On PC1:

    ping 192.168.20.10       (ping to PC2 via VPN tunnel)

On PC2:

    ping 192.168.10.10       (ping back to PC1)

Both pings were successful — confirming that the Site-to-Site IPSec VPN tunnel between India Site and Dubai Site is fully working.

---
