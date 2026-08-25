# Troubleshooting

## Tunnel not coming up

First check logs:
  journalctl -u strongswan -f
  ipsec statusall

Common issues:

Wrong PSK - both sides must have exact same key in ipsec.secrets

Firewall blocking - make sure UDP 500 (IKE) and 4500 (NAT-T) are open, also allow ESP protocol

Mismatched proposals - if unsure remove the ! from ike= and esp= lines to allow fallback

IP mismatch - double check left/right values match actual public IPs

## Tunnel up but cant ping across sites

1. Check ip_forward:
   cat /proc/sys/net/ipv4/ip_forward
   (should say 1)

2. Check FORWARD rules:
   iptables -L FORWARD -n -v

3. Check route on client - it needs to route through gateway

## Tunnel drops frequently

Increase DPD timeout in ipsec.conf or adjust dpddelay/dpdtimeout values.

## Restarting cleanly

  ipsec stop
  iptables -F
  iptables -t nat -F
  bash firewall_rules.sh
  ipsec start
