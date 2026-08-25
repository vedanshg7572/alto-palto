# network node definitions for both sites
# used by the simulator and packet tester

SITE_A = {
    "name": "Site-A (HQ)",
    "public_ip": "203.0.113.1",
    "lan_network": "192.168.1.0/24",
    "gateway": "192.168.1.1",
    "hosts": [
        {"name": "PC-A1", "ip": "192.168.1.10"},
        {"name": "PC-A2", "ip": "192.168.1.11"},
        {"name": "Server-A", "ip": "192.168.1.100"},
    ]
}

SITE_B = {
    "name": "Site-B (Branch)",
    "public_ip": "203.0.113.2",
    "lan_network": "192.168.2.0/24",
    "gateway": "192.168.2.1",
    "hosts": [
        {"name": "PC-B1", "ip": "192.168.2.10"},
        {"name": "PC-B2", "ip": "192.168.2.11"},
        {"name": "Server-B", "ip": "192.168.2.100"},
    ]
}

VPN_CONFIG = {
    "psk": "MyS3cur3VPN@Key#2024",
    "ike_version": "IKEv2",
    "encryption": "AES-256",
    "integrity": "SHA-256",
    "dh_group": "modp2048",
    "ike_lifetime": 28800,   # seconds
    "esp_lifetime": 3600,    # seconds
}
