# Router quirks observed with OpenAI-compatible gateways

## Quirk 1 — JSON body served as SSE (9router, seen 2026-08-25)
`POST /v1/chat/completions` returned HTTP 200 with `content-type: text/event-stream`
but a RAW JSON completion object as the body, plus a literal trailing chunk:

```
{"id":"...","object":"chat.completion",...}data: [DONE]
```

Symptom: `json.loads(body)` raises `JSONDecodeError: Extra data`.
Fix: take only the first JSON value:

```python
obj, _ = json.JSONDecoder().raw_decode(text.strip())
content = obj["choices"][0]["message"]["content"]
```

Note some models also return `reasoning_content` alongside `content` — always read
`message.content`, never concatenate reasoning into the answer.

## Quirk 2 — Intermittent 503 from upstream
The gateway proxies to upstream providers; single requests randomly fail with
`503 {"error":{"message":"[500]: ... Internal server error"}}`. A retry loop
(3 attempts, backoff 3s/6s/9s on 429/500/502/503/504) turned flaky smoke tests green.
Design load tests around retries or expect ~5% noise.

## Quirk 3 — Model id aliases
`GET /v1/models` listed 391 ids including near-duplicates of the requested model
(e.g. `X-muse` vs `Reza/meta-ai/muse-glimmer-30b`). Always resolve the exact id the
user named; the actual served model is echoed back in the response's `model` field
(`x-preview-f-free`) — log it when debugging quality issues.

## Test-runner pattern that worked
Mixed verifiable prompts cycled across N requests (math=391, fr=bonjour,
json={"status":"ok"}, count letters=4, de=Gute Nacht), ThreadPoolExecutor(8),
per-request PASS/FAIL with content assertions, aggregate pass-rate + avg latency +
failure samples into a JSON report. See `/data/workspace/test_xmuse.py`.
