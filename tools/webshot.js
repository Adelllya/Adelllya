#!/usr/bin/env node
// Screenshots a live page after it has settled. Needs Node 22+ and Google Chrome.
//   node tools/webshot.js https://example.com out.png [width] [height] [waitMs] [scrollY] [scriptToRunFirst]
const { spawn } = require("child_process");
const fs = require("fs");
const os = require("os");
const path = require("path");

const [url, out, w = "1280", h = "800", wait = "7000", scroll = "0", inject = ""] = process.argv.slice(2);
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const port = 9300 + Math.floor(Math.random() * 400);
const profile = fs.mkdtempSync(path.join(os.tmpdir(), "webshot-"));
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function main() {
  const chrome = spawn(CHROME, ["--headless=new", "--hide-scrollbars", `--remote-debugging-port=${port}`,
    `--user-data-dir=${profile}`, `--window-size=${w},${h}`, "about:blank"], { stdio: "ignore" });
  try {
    let target;
    for (let i = 0; i < 40 && !target; i++) {
      await sleep(250);
      try {
        const list = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
        target = list.find((t) => t.type === "page");
      } catch (e) { /* not up yet */ }
    }
    if (!target) throw new Error("chrome did not start");
    const ws = new WebSocket(target.webSocketDebuggerUrl);
    await new Promise((r) => (ws.onopen = r));
    let id = 0;
    const pending = new Map();
    ws.onmessage = (m) => {
      const msg = JSON.parse(m.data);
      if (pending.has(msg.id)) { pending.get(msg.id)(msg.result); pending.delete(msg.id); }
    };
    const send = (method, params = {}) => new Promise((r) => { pending.set(++id, r); ws.send(JSON.stringify({ id, method, params })); });
    await send("Emulation.setDeviceMetricsOverride", { width: +w, height: +h, deviceScaleFactor: 1, mobile: false });
    if (inject) { await send("Page.enable"); await send("Page.addScriptToEvaluateOnNewDocument", { source: inject }); }
    await send("Page.navigate", { url });
    await sleep(+wait);
    if (+scroll) { await send("Runtime.evaluate", { expression: `window.scrollTo(0, ${+scroll})` }); await sleep(1500); }
    const shot = await send("Page.captureScreenshot", { format: "png" });
    fs.writeFileSync(out, Buffer.from(shot.data, "base64"));
    console.log(out);
    ws.close();
  } finally {
    chrome.kill();
    await sleep(300);
    fs.rmSync(profile, { recursive: true, force: true });
  }
}
main().catch((e) => { console.error(e.message); process.exit(1); });
