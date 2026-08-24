# 🩺 System Health — 2026-08-24 12:22 UTC

> Snapshot at backup time. History kept in git.

| Component | Status |
|---|---|
| Host OS | Linux 6.18.15+deb13-cloud-amd64 |
| Python | 3.11.16 |
| Uptime | ? |
| Memory | ? |
| Disk / | 1.4T used / 2.9T total (46%) |
| Load avg (1m) | 20.26 |
| Gateway | ? |

## 📜 Recent Log Tails

<details>
<summary><code>gateway.log</code> (last 15 lines)</summary>

```
2026-08-23 22:22:38,018 INFO gateway.run: Agent cache idle-TTL evict: session=agent:main:telegram:dm:7025776524 (idle=3876s)
2026-08-23 22:22:38,020 INFO gateway.run: Agent cache idle sweep: evicted 1 agent(s)
2026-08-24 01:12:31,003 WARNING hermes_plugins.telegram_platform.adapter: [Telegram] Telegram network _redact_telegram_error_text(error), scheduling reconnect: Bad Gateway
2026-08-24 01:12:31,004 WARNING hermes_plugins.telegram_platform.adapter: [Telegram] Telegram network error (attempt 1/10), reconnecting in 5s. Error: Bad Gateway
2026-08-24 01:12:40,150 WARNING hermes_plugins.telegram_platform.adapter: [Telegram] Telegram polling reconnect failed: Bad Gateway
2026-08-24 01:12:40,150 WARNING hermes_plugins.telegram_platform.adapter: [Telegram] Telegram network error (attempt 2/10), reconnecting in 10s. Error: Bad Gateway
2026-08-24 01:13:10,472 WARNING hermes_plugins.telegram_platform.adapter: [Telegram] Telegram polling reconnect failed: Timed out
2026-08-24 01:13:10,472 WARNING hermes_plugins.telegram_platform.adapter: [Telegram] Telegram network error (attempt 3/10), reconnecting in 20s. Error: Timed out
2026-08-24 01:13:42,196 INFO hermes_plugins.telegram_platform.adapter: [Telegram] Telegram polling restarted after network error (attempt 3); health pending getUpdates progress
2026-08-24 01:35:30,635 WARNING hermes_plugins.telegram_platform.adapter: [Telegram] Telegram network _redact_telegram_error_text(error), scheduling reconnect: Bad Gateway
2026-08-24 01:35:30,636 WARNING hermes_plugins.telegram_platform.adapter: [Telegram] Telegram network error (attempt 1/10), reconnecting in 5s. Error: Bad Gateway
2026-08-24 01:35:50,639 WARNING hermes_plugins.telegram_platform.adapter: [Telegram] updater.stop() timed out during network-error reconnect (likely CLOSE-WAIT socket); forcing drain and restart without clean stop
2026-08-24 01:36:00,460 INFO hermes_plugins.telegram_platform.adapter: [Telegram] Telegram polling restarted after network error (attempt 1); health pending getUpdates progress
2026-08-24 12:19:18,882 INFO hermes_plugins.telegram_platform.adapter: [Telegram] Flushing text batch agent:main:telegram:dm:7025776524 (9 chars)
2026-08-24 12:19:18,889 INFO gateway.run: inbound message: platform=telegram user=𝑹𝑬𝒁𝑨 | 𝟭𝟱:𝟰𝟳 chat=7025776524 msg='ادامه بده' reply_to_id=None reply_to_text=''
```
</details>

<details>
<summary><code>agent.log</code> (last 15 lines)</summary>

```
2026-08-24 12:19:19,337 INFO run_agent: OpenAI client created (agent_init, shared=True) thread=hermes-gateway_1:139783343412928 provider=openai-api base_url=https://9router-production-df048.up.railway.app/v1 model=X-muse
2026-08-24 12:19:19,423 INFO agent.model_metadata: Could not detect context length for model 'X-muse' at https://9router-production-df048.up.railway.app/v1 — defaulting to 256,000 tokens (probe-down). Set model.context_length in config.yaml to override.
2026-08-24 12:19:19,441 INFO [20260823_191347_4c36a95f] agent.turn_context: conversation turn: session=20260823_191347_4c36a95f model=X-muse provider=openai-api platform=telegram history=71 msg='ادامه بده'
2026-08-24 12:19:19,465 INFO [20260823_191347_4c36a95f] agent.conversation_loop: Repaired 1 message-alternation violations before request (session=20260823_191347_4c36a95f)
2026-08-24 12:19:19,479 INFO run_agent: OpenAI client created (codex_stream_request, shared=False) thread=Thread-195 (<lambda>):139783489169088 provider=openai-api base_url=https://9router-production-df048.up.railway.app/v1 model=X-muse
2026-08-24 12:19:27,471 INFO hermes_cli.mem_trim: memory trim: reason=messaging gateway housekeeping malloc_trim=1 rss_kib=317672->311764 rss_anon_kib=294676->288768 threads=19 duration_ms=196.5
2026-08-24 12:20:27,672 INFO hermes_cli.mem_trim: memory trim: reason=messaging gateway housekeeping malloc_trim=1 rss_kib=313892->313156 rss_anon_kib=289592->288856 threads=19 duration_ms=199.7
2026-08-24 12:21:06,014 INFO tools.file_tools: Creating new local environment for task default...
2026-08-24 12:21:06,028 INFO tools.environments.base: Session snapshot created (session=c43375cf2d02, cwd=/data/workspace)
2026-08-24 12:21:06,028 INFO tools.file_tools: local environment ready for task default
2026-08-24 12:21:06,095 INFO [20260823_191347_4c36a95f] agent.tool_executor: tool patch completed (0.08s, 875 chars)
2026-08-24 12:21:07,521 INFO [20260823_191347_4c36a95f] agent.tool_executor: tool terminal completed (1.42s, 25987 chars)
2026-08-24 12:21:27,868 INFO hermes_cli.mem_trim: memory trim: reason=messaging gateway housekeeping malloc_trim=1 rss_kib=316680->313824 rss_anon_kib=292320->289464 threads=19 duration_ms=195.3
2026-08-24 12:21:46,077 INFO [20260823_191347_4c36a95f] agent.tool_executor: tool terminal completed (0.12s, 203 chars)
2026-08-24 12:22:11,942 INFO [20260823_191347_4c36a95f] agent.tool_executor: tool patch completed (0.09s, 878 chars)
```
</details>

<details>
<summary><code>errors.log</code> (last 15 lines)</summary>

```
             ^^^^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.11/site-packages/telegram/request/_baserequest.py", line 198, in post
    result = await self._request_wrapper(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.11/site-packages/telegram/request/_baserequest.py", line 305, in _request_wrapper
    code, payload = await self.do_request(
                    ^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/venv/lib/python3.11/site-packages/telegram/request/_httpxrequest.py", line 296, in do_request
    raise TimedOut from err
telegram.error.TimedOut: Timed out
2026-08-24 01:13:10,472 WARNING hermes_plugins.telegram_platform.adapter: [Telegram] Telegram polling reconnect failed: Timed out
2026-08-24 01:13:10,472 WARNING hermes_plugins.telegram_platform.adapter: [Telegram] Telegram network error (attempt 3/10), reconnecting in 20s. Error: Timed out
2026-08-24 01:35:30,635 WARNING hermes_plugins.telegram_platform.adapter: [Telegram] Telegram network _redact_telegram_error_text(error), scheduling reconnect: Bad Gateway
2026-08-24 01:35:30,636 WARNING hermes_plugins.telegram_platform.adapter: [Telegram] Telegram network error (attempt 1/10), reconnecting in 5s. Error: Bad Gateway
2026-08-24 01:35:50,639 WARNING hermes_plugins.telegram_platform.adapter: [Telegram] updater.stop() timed out during network-error reconnect (likely CLOSE-WAIT socket); forcing drain and restart without clean stop
```
</details>
