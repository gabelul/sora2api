---
description: How to use async video generation with n8n automation
---

# Async Video Generation Workflow

This workflow allows automated video generation using Sora2API's async task mode.

## Prerequisites
1. Sora2API server running with async task mode enabled
2. API key configured
3. n8n instance (or similar automation tool)

## Async API Usage

### Step 1: Submit Task
```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "X-Sora2-Async: true" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sora2-landscape-10s",
    "messages": [{"role": "user", "content": "Your prompt here"}]
  }'
```

Response includes `task_id` for polling.

### Step 2: Poll Status
```bash
curl http://localhost:8000/v1/tasks/{task_id} \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Poll every 15-30 seconds until `status` is `completed`.

### Step 3: Get Result
When completed, `result_urls` contains the video URL(s).

## n8n Integration

Import `n8n/viral_video_workflow.json` for complete automation:
1. Topic → GPT-4o script generation
2. Image generation (async)
3. Video from image (async)  
4. Final output URLs

Configure the **Config** node with:
- `sora2api_url`: Your server URL
- `sora2api_key`: Your API key
- `openai_key`: For GPT-4o script generation

## Available Models

### Image Models
- `gpt-image` (360x360)
- `gpt-image-landscape` (540x360)
- `gpt-image-portrait` (360x540)

### Video Models  
- `sora2-landscape-10s` / `sora2-portrait-10s`
- `sora2-landscape-15s` / `sora2-portrait-15s`
- `sora2-landscape-25s` / `sora2-portrait-25s` (Pro)
- `sora2pro-*` variants (Pro subscription required)
