import time
import random
import sys
import os

sys.path.append(os.path.dirname(__file__))
from network_nodes import SITE_A, SITE_B


def fake_ping(src_ip, dst_ip, count=4):
    """simulates a ping between two IPs across the VPN tunnel"""
    print(f"Pinging {dst_ip} from {src_ip} ({count} packets)")
    print()

    success = 0
    times = []

    for i in range(1, count + 1):
        # add some randomness to make it feel real
        delay = random.uniform(8.0, 35.0)

        # very small chance of packet loss to make it realistic
        if random.random() < 0.05:
            print(f"  Request timeout for icmp_seq {i}")
        else:
            print(f"  64 bytes from {dst_ip}: icmp_seq={i} ttl=62 time={delay:.1f} ms")
            success += 1
            times.append(delay)

        time.sleep(0.4)

    print()
    loss = count - success
    loss_pct = (loss / count) * 100
    print(f"--- {dst_ip} ping statistics ---")
    print(f"{count} packets transmitted, {success} received, {loss_pct:.0f}% packet loss")

    if times:
        print(f"rtt min/avg/max = {min(times):.1f}/{sum(times)/len(times):.1f}/{max(times):.1f} ms")

    return success > 0


def test_connectivity():
    print("=" * 55)
    print("  VPN Connectivity Test")
    print("=" * 55)
    print()

    # pick a random host from each site for testing
    host_a = random.choice(SITE_A['hosts'])
    host_b = random.choice(SITE_B['hosts'])

    print(f"Testing: {host_a['name']} ({host_a['ip']}) --> {host_b['name']} ({host_b['ip']})")
    print()

    # Test 1: ping from Site-A host to Site-B host
    result1 = fake_ping(host_a['ip'], host_b['ip'])
    print()

    # Test 2: ping reverse
    print(f"Testing reverse: {host_b['name']} ({host_b['ip']}) --> {host_a['name']} ({host_a['ip']})")
    print()
    result2 = fake_ping(host_b['ip'], host_a['ip'])
    print()

    # Test 3: gateway reachability
    print(f"Testing: {host_a['name']} ({host_a['ip']}) --> Site-B Gateway (192.168.2.1)")
    print()
    result3 = fake_ping(host_a['ip'], SITE_B['gateway'], count=2)
    print()

    # summary
    print("=" * 55)
    print("Test Results:")
    print(f"  Site-A -> Site-B : {'PASS' if result1 else 'FAIL'}")
    print(f"  Site-B -> Site-A : {'PASS' if result2 else 'FAIL'}")
    print(f"  Gateway reach    : {'PASS' if result3 else 'FAIL'}")
    print("=" * 55)

    all_ok = result1 and result2 and result3
    print()
    if all_ok:
        print("All tests passed. VPN tunnel is working correctly.")
    else:
        print("Some tests failed. Check your tunnel and firewall rules.")


if __name__ == "__main__":
    test_connectivity()
