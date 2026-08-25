# Setup Guide - Site-to-Site VPN

## Requirements

- 2 Linux machines (Ubuntu 22.04 recommended) with public IPs
- Root/sudo access
- Internet connectivity on both machines

## Step 1 - Install strongSwan

Run this on both machines:

  apt update
  apt install strongswan strongswan-pki -y

## Step 2 - Copy Config Files

On Site-A machine:

  cp site-a/ipsec.conf /etc/ipsec.conf
  cp site-a/ipsec.secrets /etc/ipsec.secrets
  chmod 600 /etc/ipsec.secrets

On Site-B machine:

  cp site-b/ipsec.conf /etc/ipsec.conf
  cp site-b/ipsec.secrets /etc/ipsec.secrets
  chmod 600 /etc/ipsec.secrets

## Step 3 - Apply Firewall Rules

On Site-A:  bash site-a/firewall_rules.sh
On Site-B:  bash site-b/firewall_rules.sh

## Step 4 - Start IPSec

On both machines:
  ipsec start
  ipsec reload

Or if using systemd:
  systemctl restart strongswan

## Step 5 - Verify

  ipsec status
  ipsec statusall

You should see: site-a-to-site-b[1]: ESTABLISHED

Try pinging a host on the other site:
  ping 192.168.2.10

## Notes

- Make sure UDP 500 and 4500 are open in your firewall/security group
- PSK must be identical on both sides
- Firewall rules may need reapplying after ipsec restart
