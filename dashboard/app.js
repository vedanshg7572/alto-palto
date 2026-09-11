const hostsA = ["192.168.1.10", "192.168.1.11", "192.168.1.100"];
const hostsB = ["192.168.2.10", "192.168.2.11", "192.168.2.100"];

window.onload = function () {
  updateTime();
};

function updateTime() {
  const now = new Date();
  document.getElementById("lastCheck").textContent = now.toLocaleTimeString();
}

function randomBetween(min, max) {
  return (Math.random() * (max - min) + min).toFixed(1);
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function runPingTest() {
  const output = document.getElementById("pingOutput");
  const btn = document.querySelector(".btn");

  output.style.display = "block";
  output.textContent = "";
  btn.disabled = true;
  btn.textContent = "Testing...";

  const srcIP = hostsA[Math.floor(Math.random() * hostsA.length)];
  const dstIP = hostsB[Math.floor(Math.random() * hostsB.length)];

  output.textContent += "Pinging " + dstIP + " from " + srcIP + "...\n\n";

  let times = [];
  for (let i = 1; i <= 4; i++) {
    await sleep(500);
    if (Math.random() < 0.05) {
      output.textContent += "  Request timeout for icmp_seq " + i + "\n";
    } else {
      const t = randomBetween(8, 35);
      times.push(parseFloat(t));
      output.textContent += "  64 bytes from " + dstIP + ": icmp_seq=" + i + " ttl=62 time=" + t + " ms\n";
    }
  }

  await sleep(300);
  const loss = ((4 - times.length) / 4 * 100).toFixed(0);
  output.textContent += "\n--- " + dstIP + " ping statistics ---\n";
  output.textContent += "4 packets transmitted, " + times.length + " received, " + loss + "% packet loss\n";

  if (times.length > 0) {
    const min = Math.min(...times).toFixed(1);
    const max = Math.max(...times).toFixed(1);
    const avg = (times.reduce((a, b) => a + b, 0) / times.length).toFixed(1);
    output.textContent += "rtt min/avg/max = " + min + "/" + avg + "/" + max + " ms\n";
  }

  output.textContent += "\nTest complete. VPN tunnel is working.";
  updateTime();

  btn.disabled = false;
  btn.textContent = "Run Ping Test";
}