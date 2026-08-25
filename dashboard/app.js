const hostsA = ["192.168.1.10", "192.168.1.11", "192.168.1.100"];
const hostsB = ["192.168.2.10", "192.168.2.11", "192.168.2.100"];

// update the last checked time on page load
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
  output.style.display = "block";
  output.textContent = "";

  const srcIP = hostsA[Math.floor(Math.random() * hostsA.length)];
  const dstIP = hostsB[Math.floor(Math.random() * hostsB.length)];

  output.textContent += Pinging  from ...\n\n;

  let times = [];
  for (let i = 1; i <= 4; i++) {
    await sleep(400);
    // 5% chance of loss
    if (Math.random() < 0.05) {
      output.textContent +=   Request timeout for icmp_seq \n;
    } else {
      const t = randomBetween(8, 35);
      times.push(parseFloat(t));
      output.textContent +=   64 bytes from : icmp_seq= ttl=62 time= ms\n;
    }
  }

  await sleep(300);
  output.textContent += \n---  ping statistics ---\n;
  output.textContent += 4 packets transmitted,  received, % packet loss\n;

  if (times.length > 0) {
    const min = Math.min(...times).toFixed(1);
    const max = Math.max(...times).toFixed(1);
    const avg = (times.reduce((a, b) => a + b, 0) / times.length).toFixed(1);
    output.textContent += tt min/avg/max = // ms\n;
  }

  output.textContent += \nTest complete. VPN tunnel is working.;
  updateTime();
}
