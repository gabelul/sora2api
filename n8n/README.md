# Viral AI Video Generator - n8n Workflow

Complete workflow for automated viral video creation using Sora2API.

## Pipeline

```
Topic/Idea → GPT-4o Script → Generate Images → Generate Videos → Output
```

## Setup

### 1. Import Workflow

1. Open n8n
2. Click **Settings** (gear icon) → **Import from File**
3. Select `viral_video_workflow.json`

### 2. Configure Credentials

Edit the **Config** node and update:

| Field | Value |
|-------|-------|
| `sora2api_url` | Your Sora2API server (e.g., `http://192.168.1.100:8000`) |
| `sora2api_key` | Your API key |
| `openai_key` | OpenAI API key for GPT-4o script generation |
| `topic` | Your video concept |
| `num_scenes` | Number of scenes (1-5 recommended) |

## How It Works

### Step 1: Script Generation
GPT-4o generates scene descriptions with:
- `image_prompt` - Static frame description
- `video_prompt` - Motion/action description

### Step 2: Image Generation (Per Scene)
- Submits to `/v1/chat/completions` with `X-Sora2-Async: true`
- Polls `/v1/tasks/{task_id}` every 15 seconds
- Uses `gpt-image-landscape` model

### Step 3: Video Generation (Per Scene)
- Takes the generated image URL
- Submits image-to-video request with `X-Sora2-Async: true`
- Polls `/v1/tasks/{task_id}` every 30 seconds
- Uses `sora2-landscape-10s` model

### Step 4: Output
Each scene outputs:
```json
{
  "scene_number": 1,
  "image_url": "https://...",
  "video_url": "https://...",
  "image_prompt": "...",
  "video_prompt": "..."
}
```

## Timing

| Stage | Estimated Time |
|-------|----------------|
| Script | ~5 seconds |
| Image (per scene) | 30-120 seconds |
| Video (per scene) | 3-10 minutes |
| **Total (3 scenes)** | **15-35 minutes** |

## Tips

1. **Keep prompts visual** - Focus on what can be seen, not abstract concepts
2. **Consistent style** - Add style keywords to all scenes (e.g., "cinematic, 4K, dramatic lighting")
3. **Simple motion** - Video AI works best with clear, single actions

## Example Topics

- "A robot discovering emotions in a futuristic city"
- "A magical forest coming to life at sunset"
- "An astronaut finding ancient ruins on Mars"
- "A cat becoming king of a medieval kingdom"

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Timeout errors | Increase poll limits in Code nodes |
| CORS errors | Make sure `local_proxy_server.py` is running |
| Empty image URL | Check Sora2API logs for content policy violations |
