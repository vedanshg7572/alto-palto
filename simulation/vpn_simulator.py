import time
import random
import hashlib
from network_nodes import SITE_A, SITE_B, VPN_CONFIG


def print_banner():
    print("=" * 60)
    print("   Site-to-Site VPN Simulator")
    print("=" * 60)
    print()


def simulate_phase1(site_a, site_b, config):
    """IKE Phase 1 - establishes a secure channel between the two gateways"""
    print("[Phase 1] Starting IKE negotiation...")
    print(f"  Initiator: {site_a['public_ip']} ({site_a['name']})")
    print(f"  Responder: {site_b['public_ip']} ({site_b['name']})")
    print()

    time.sleep(0.5)
    print(f"  [*] Sending IKE_SA_INIT from {site_a['public_ip']} -> {site_b['public_ip']}")
    time.sleep(0.3)
    print(f"  [*] Proposed algorithms: {config['encryption']}, {config['integrity']}, {config['dh_group']}")
    time.sleep(0.4)

    print(f"  [*] {site_b['public_ip']} accepted the proposal")
    time.sleep(0.3)

    # fake DH key exchange
    nonce_a = random.randint(100000, 999999)
    nonce_b = random.randint(100000, 999999)
    print(f"  [*] Diffie-Hellman key exchange...")
    print(f"      Nonce-A: {nonce_a}")
    print(f"      Nonce-B: {nonce_b}")
    time.sleep(0.5)

    # verify PSK
    psk_hash = hashlib.sha256(config['psk'].encode()).hexdigest()[:16]
    print(f"  [*] Authenticating with PSK (hash: {psk_hash}...)")
    time.sleep(0.4)
    print(f"  [OK] IKE Phase 1 complete - IKE SA established")
    print()

    return True


def simulate_phase2(site_a, site_b, config):
    """IKE Phase 2 - negotiates the actual IPSec SA for data encryption"""
    print("[Phase 2] Negotiating IPSec SA (Quick Mode)...")

    time.sleep(0.3)
    print(f"  [*] Initiating CHILD_SA for:")
    print(f"      Local subnet:  {site_a['lan_network']}")
    print(f"      Remote subnet: {site_b['lan_network']}")
    time.sleep(0.4)

    print(f"  [*] Proposing ESP with {config['encryption']} + {config['integrity']}")
    time.sleep(0.3)
    print(f"  [*] Generating SPI values...")

    # make up some SPI values
    spi_in  = hex(random.randint(0x10000000, 0xFFFFFFFF))
    spi_out = hex(random.randint(0x10000000, 0xFFFFFFFF))
    print(f"      SPI inbound:  {spi_in}")
    print(f"      SPI outbound: {spi_out}")

    time.sleep(0.5)
    print(f"  [OK] IKE Phase 2 complete - IPSec SA established")
    print()

    return True


def show_tunnel_status(site_a, site_b, config):
    print("[Tunnel Status]")
    print(f"  Connection: {site_a['name']} <===> {site_b['name']}")
    print(f"  Status: CONNECTED (UP)")
    print(f"  Mode: Tunnel (ESP)")
    print(f"  Encryption: {config['encryption']}")
    print(f"  Integrity: {config['integrity']}")
    print(f"  IKE Version: {config['ike_version']}")
    print(f"  Tunnel: {site_a['lan_network']} <-> {site_b['lan_network']}")
    print(f"  IKE SA Lifetime: {config['ike_lifetime'] // 3600}h")
    print(f"  IPSec SA Lifetime: {config['esp_lifetime'] // 60}m")
    print()


def main():
    print_banner()

    print("Initializing VPN tunnel between:")
    print(f"  {SITE_A['name']} -- {SITE_A['public_ip']}")
    print(f"  {SITE_B['name']} -- {SITE_B['public_ip']}")
    print()

    phase1_ok = simulate_phase1(SITE_A, SITE_B, VPN_CONFIG)
    if not phase1_ok:
        print("[ERROR] Phase 1 failed. Check your PSK and IKE settings.")
        return

    phase2_ok = simulate_phase2(SITE_A, SITE_B, VPN_CONFIG)
    if not phase2_ok:
        print("[ERROR] Phase 2 failed. Check your ESP proposals.")
        return

    show_tunnel_status(SITE_A, SITE_B, VPN_CONFIG)
    print("VPN tunnel is UP. Both sites can now communicate securely.")


if __name__ == "__main__":
    main()
