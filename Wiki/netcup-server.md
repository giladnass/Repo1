---
title: Netcup Server
type: wiki
tags:
- netcup
- infrastructure
- server
- ollama
created: 2026-04-20
updated: 2026-04-20
sources: []
status: active
confidence: high
permalink: ai-memory/wiki/netcup-server
---

## Summary

Ubuntu 24.04 VPS hosting always-on services: Ollama (local inference), OpenClaw/Aurora (AI agent), AnythingLLM, Open WebUI, IPTVX media server. No GPU -- all inference is CPU-bound.

## Specs

| Property | Value |
|---|---|
| OS | Ubuntu 24.04 |
| RAM | 32 GB |
| CPU | 12 shared vCPUs (AMD EPYC, KVM-based) |
| GPU | None |
| Storage | NVMe |
| Hostname | `v2202604349201447927` |
| Public IP | `152.53.244.42` |
| Tailscale IP | `100.127.32.127` |

## Access

- **SSH alias:** `Host netcup` in `~/.ssh/config`
- **Auth:** key-based with passphrase in macOS Keychain

## Running Services

| Service | Type | Endpoint | Public? |
|---|---|---|---|
| Ollama | systemd | Tailscale-accessible | No |
| OpenClaw | systemd user (`openclaw`) | Telegram, Discord, web UI | Partial |
| AnythingLLM | Docker | `127.0.0.1:3001` | No |
| Open WebUI | Docker | `0.0.0.0:3000 -> 8080` | Yes |
| IPTVX | systemd `iptvx-server` | Port 9191 | Yes |

## Ollama Configuration

**Installed models:** `qwen2.5:1.5b`, `deepseek-r1:1.5b`, `llama3.2:latest`

**Service override:** `/etc/systemd/system/ollama.service.d/override.conf`

```
OLLAMA_NUM_THREADS=8
OLLAMA_FLASH_ATTENTION=1
OLLAMA_KV_CACHE_TYPE=q8_0
OLLAMA_NUM_PARALLEL=1
OLLAMA_MAX_LOADED_MODELS=1
OLLAMA_KEEP_ALIVE=5m
OLLAMA_NUM_CTX=16384
```

**Important:** `OLLAMA_NUM_CTX=16384` is the Ollama-level default context. OpenClaw enforces a 16k minimum context per request. `qwen2.5:1.5b` performs best at ctx 2048. This tension is the root cause of the OpenClaw fallback bug (see [[000-Meta/known-issues]] KI-004).

## Role in AI-Memory Ingestion Pipeline

Per Decision D-007:

| Task | Runs Here? | Notes |
|---|---|---|
| Audio/video transcription | Yes | `faster-whisper` -- not yet installed |
| Visual extraction (SAM) | Yes | CPU-only -- no GPU, will be slow |
| URL scraping | Yes | Long-running, network-bound |
| PDF/Office/EPUB conversion | No | Runs on Mac |

**No GPU caveat:** Visual extraction using SAM (Segment Anything Model) will run on CPU only. For large video batches this will be significantly slower than estimates assuming GPU acceleration. Consider deprioritizing visual extraction or using a cloud vision API instead for high-volume cases.

## Related
- [[Wiki/openclaw-aurora]]
- [[Memory/tool-configs]]
- [[000-Meta/known-issues]]