VODI WALKER project: single-file Python Telegram bot (bot.py) on Railway, polling only (no webhook/DB/Cloudflare for the bot itself); it deploys the admin-uploaded worker.js to each user's own Cloudflare account via their API token + account ID; user tokens must never be stored, logged, or echoed. Work dir: /data/workspace/vodi-py.
§
Reza only accepts a feature as done after live end-to-end verification against the real API with real credentials; mocked/passing unit tests alone are not sufficient proof.
§
Reza's preferred tech stack and project requirements:
- Prefers Single-File Workers (worker.js) for Cloudflare Workers.
- Architecture: VLESS/Trojan over WebSocket using `cloudflare:sockets`.
- UI/Design: High-end Cyber-Glassmorphism, Vazirmatn font, Dark/Light modes, component-based SPA-style dashboards (though often struggles with the implementation, prefers robustness).
- Key Feature: Clean IP scanner that dynamically injects IP lists into subscription configurations.
- Deployment: Requires robust, bug-free, fully integrated professional panels (like BPB-Worker-Panel inspired).
- Documentation: Prefers files to be provided in full, complete, and syntax-checked states rather than snippets.
§
RixPanel is an independent VPN/proxy control-plane project. The first deliverable is a real config-generation panel (VLESS/WS or XHTTP, UUID, subscription, QR) backed by working API/UI/tests; later goals include 150 tested features, multi-location, one-time join tokens, multi-hop, and failover. Railway is tentatively for control plane only; proxy exits need a compliant provider and live verification.